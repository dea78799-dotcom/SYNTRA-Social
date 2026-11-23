# SYNTRA Social — RLS Test Matrix 1.9B

**Date:** 2026-11-23  
**Environment:** Existing SYNTRA-Social Supabase project  
**Mode:** Design and static policy/grant inspection only. This document does not apply SQL or create test accounts.

## 1. Goal

Define repeatable authorization tests before the browser client is connected. Every test must use separate test identities and run through the same API role and JWT claims used by the client. A successful SQL-editor query as the database owner is not evidence that a client policy works.

## 2. Test identities

Create isolated test users in a dedicated staging environment before runtime testing:

| Alias | Relationship |
|---|---|
| A | Content owner / profile owner |
| B | Unrelated signed-in user |
| C | Accepted follower of A |
| D | Pending follower request to A |
| E | Account blocked by A |
| F | Anonymous visitor (no Auth session) |
| M | Moderator identity, only after a server-controlled moderator role is designed |

Do not use a real personal account as the only test identity. Do not create test identities in production merely to perform this plan.

## 3. Current baseline observed

- Nine public application tables have RLS enabled.
- Current policies are owner/participant scoped; there is no shared feed/profile read policy.
- Authenticated grants are present on most tables.
- `follows` has SELECT, INSERT and DELETE table grants, but no UPDATE grant and no UPDATE RLS policy. Its status constraint permits only `pending` and `accepted`; the consistency constraint requires `accepted_at` to be null/non-null accordingly.
- `notifications` has table-level SELECT only, plus a column-level UPDATE grant on `read_at` only. Its existing UPDATE RLS policy is recipient-only with matching `USING` and `WITH CHECK`; no UPDATE privilege exists for `payload` or other columns. This read-state permission is already narrowly scoped and must not be broadened.
- Notification creation has no client INSERT policy.
- No community tables were found in the current application schema.
- Storage bucket and object policies were not verified as part of this matrix.

## 4. Required authorization matrix

The table below describes the intended product contract after the required policy work. It is not a claim that these permissions work today.

| Resource / action | F | A (owner) | B (unrelated) | C (accepted follower) | D (pending) | E (blocked by A) |
|---|---:|---:|---:|---:|---:|---:|
| Read A private profile | Deny | Allow | Deny | Allow only if A's privacy rules permit accepted followers | Deny | Deny |
| Read A public profile | Deny until public profile projection is implemented | Allow | Allow safe public fields | Allow safe public fields | Allow safe public fields | Deny |
| Read A private post | Deny | Allow | Deny | Allow only if A's follower policy permits | Deny | Deny |
| Read A public published post | Deny until anonymous access is deliberately designed | Allow | Allow | Allow | Allow | Deny |
| Read A draft post | Deny | Allow | Deny | Deny | Deny | Deny |
| Create post as self | Deny | Allow | Allow | Allow | Allow | Allow, unless user-level suspension applies |
| Insert post with another author's ID | Deny | Deny | Deny | Deny | Deny | Deny |
| Read comments on a readable post | Deny until guest read is designed | Allow | Allow | Allow | Allow | Deny |
| Read likes/reaction totals for a readable post | Deny until guest read is designed | Allow | Allow | Allow | Allow | Deny |
| Create own like/comment on a readable post | Deny | Allow | Allow | Allow | Allow | Deny when interaction with A is blocked |
| Read own notifications | Deny | Allow | Allow | Allow | Allow | Allow |
| Read another user's notifications | Deny | Deny | Deny | Deny | Deny | Deny |
| Mark own notification read | Deny | Allow via narrowly scoped update | Allow via narrowly scoped update | Allow via narrowly scoped update | Allow via narrowly scoped update | Allow via narrowly scoped update |
| Create report as self | Deny | Allow | Allow | Allow | Allow | Allow |
| Read another user's reports | Deny | Deny | Deny | Deny | Deny | Deny |
| Read A's block list | Deny | Allow | Deny | Deny | Deny | Deny |

**Privacy decision required:** public profile discovery and public post reads must not be conflated. Decide whether anonymous visitors may see public content. Until that is explicitly approved and tested, keep the current authenticated-only grants.

**Block semantics:** for a block relationship A → E, deny E access to A's protected profile/content and deny both accounts from interacting with each other. The final policy should evaluate both directions to avoid asymmetric leaks. Block checks must apply to posts, comments, likes, follows, community membership, and future messaging.

## 5. Table-by-table test cases

### profiles
- Owner can select and update own profile.
- Owner cannot change `id` to another Auth user's ID.
- Other authenticated users receive only explicitly approved public fields once a safe profile-read path exists.
- Private profile is invisible to unrelated and pending-follower accounts.
- Blocked relationship denies access regardless of discoverability.
- Email, phone, birth date and Auth metadata are never stored in or exposed through the public profile row.

### posts
- Author can create, read, update and delete own posts.
- Author cannot transfer `author_id`.
- Draft posts are visible only to their author.
- Published posts obey the visibility setting and private-profile rules.
- Accepted follower access works only where the owner has permitted it.
- Pending followers and blocked accounts cannot read protected posts.
- A public-read policy must not accidentally reveal draft, private or scheduled content.

### follows
- A can create only a request where `follower_id = auth.uid()`.
- Self-follow is rejected.
- Only the target account can accept or reject a pending request.
- Acceptance must be a constrained transition: `pending → accepted`; requester cannot accept their own request.
- A user cannot change either participant ID.
- Deletion may be initiated by either participant if product behavior explicitly allows unfollow/removal.
- Both accounts' block relationship must prevent follow creation and acceptance.

**Known blocker:** current schema has no UPDATE privilege or UPDATE RLS policy for `follows`. The acceptance flow is not implemented. The 1.9C candidate grants UPDATE only on `status` and `accepted_at`, and allows only the recipient to transition a pending row to accepted. The requester cannot accept their own request or modify participant IDs.

### comments and likes
- Users can insert/delete only their own rows.
- A user cannot forge `author_id` / `user_id`.
- Reads inherit the parent post's visibility and block rules.
- Comment updates cannot transfer ownership or change the parent post to an unreadable post.
- Enforce one like per (post, user) at the database constraint level.
- Verify deletion and counts after block/unblock and post deletion.

### notifications
- Recipient can select only own notifications.
- Client cannot insert, reassign, or forge notification rows.
- Client can update only `read_at`, not `recipient_id`, `actor_id`, `notification_type`, `entity_id`, or `payload`.
- Notification generation is performed by a trusted server-side function/trigger with a reviewed privilege boundary.

**Verified state:** authenticated has table-level SELECT and a column-level UPDATE grant on `read_at` only. The existing UPDATE policy is recipient-only with matching USING and WITH CHECK. No notification migration is needed in 1.9C; regression-test the real API path and preserve this narrow grant. Do not grant unrestricted UPDATE.

### reports and moderation
- Reporter can insert a report only as self.
- Reporter can read only own submitted reports.
- Reporter cannot set moderation status or access the moderation queue.
- Moderator actions must use a server-controlled role/claim that ordinary users cannot assign to themselves.
- Audit status changes and restrict report details to authorized reviewers.

### post_media and Storage
- Metadata owner must match the authenticated user and the parent post author.
- Storage path must be namespaced by the authenticated user and must not be user-selectable across owners.
- Test upload, download, overwrite, move and delete separately.
- Private objects must not be retrievable through guessed public URLs.
- Validate MIME type, byte size, media dimensions/duration and orphan cleanup on a trusted boundary.

## 6. Test execution protocol

1. Use a dedicated staging Supabase project or an isolated staging database. Do not use production identities or production content for negative tests.
2. Seed only synthetic users and synthetic records through a controlled setup script.
3. Run tests using the actual `anon` and `authenticated` API roles with valid test JWTs. Do not rely only on SQL Editor owner-role queries.
4. For each identity, test SELECT, INSERT, UPDATE and DELETE independently.
5. Include ownership-forgery attempts, cross-account reads, pending/accepted follow states, and block relationships in both directions.
6. Record expected result, actual result, HTTP/PostgREST status, and the policy/grant responsible.
7. Re-run the entire matrix after every RLS/grant migration.
8. Run Security Advisor and inspect table grants after the migration.
9. Keep the public prototype local-only until all critical cases pass.

## 7. Acceptance criteria

- [ ] Anonymous role cannot access private application rows.
- [ ] Owner can manage only their own rows.
- [ ] Another account cannot read private profile, draft, or private post content.
- [ ] Public content policy (if enabled) exposes only published, explicitly public content.
- [ ] Accepted followers can access only the content the owner permits.
- [ ] Pending followers cannot access follower-only content.
- [ ] Block relationship denies protected reads and interactions in both directions.
- [ ] Follow acceptance is possible only for the target account and only from pending state.
- [ ] Notification recipient can update only `read_at`.
- [ ] Client cannot forge notifications or moderation outcomes.
- [ ] Comments, likes and media inherit parent-post access controls.
- [ ] No email, phone, birth date, Auth metadata or secret is exposed.
- [ ] Security Advisor has no unresolved critical/high finding.
- [ ] All tests pass through the client API using separate staging identities.

## 8. Next implementation order

1. Add the reviewed least-privilege follow-acceptance migration in staging and run the API tests.
2. Regression-test notification read-state through the API; its column grant and recipient policy already exist.
3. Design a reusable, block-aware post visibility rule.
4. Add shared profile/post/comment/like reads only after the above rules are tested.
5. Design community tables and Storage policies as separate reviewed migrations.

**Safety boundary:** do not paste or execute an unreviewed policy bundle on the live project. This matrix is a test specification, not a migration.


## 1.9C implementation notes

- Candidate SQL: [docs/sql/LEAST-PRIVILEGE-1.9C.sql](./sql/LEAST-PRIVILEGE-1.9C.sql).
- Regression plan: [docs/LEAST-PRIVILEGE-TESTS-1.9C.md](./LEAST-PRIVILEGE-TESTS-1.9C.md).
- No staging project was found in the connected Supabase account. The candidate has not been applied to the live project.
