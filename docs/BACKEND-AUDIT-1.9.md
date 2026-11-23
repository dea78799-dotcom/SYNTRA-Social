# SYNTRA Social — Backend Audit 1.9

**Date:** 2026-11-23  
**Scope:** Read-only inspection of the existing SYNTRA-Social Supabase project. No database schema, policies, user records, or Auth settings were changed during this audit.

## Executive result

The Supabase project already exists and is healthy. PostgreSQL 17.12 is running in Singapore (`ap-southeast-1`). The database contains nine application tables and three recorded migrations. All nine application tables have Row Level Security (RLS) enabled. The Security Advisor returned no findings at the time of this check.

This is a useful private-by-default foundation, but it is **not yet a complete multi-user social backend**. Current policies intentionally limit most reads to the record owner or relationship participant. The application cannot yet use these policies for a normal shared feed, public profile discovery, or cross-user comments and reaction counts.

## Verified database inventory

| Table | Current purpose |
|---|---|
| `profiles` | User profile; defaults to private and not discoverable |
| `posts` | Text posts; defaults to private and draft |
| `post_media` | Metadata for image/video objects |
| `follows` | Follow requests and accepted relationships |
| `blocks` | Block relationships |
| `comments` | Post comments |
| `likes` | One like per user/post |
| `notifications` | Recipient-owned notifications |
| `reports` | User-submitted reports |

All nine tables currently report zero rows. The database has three migrations recorded:

- `syntra_social_initial_schema`
- `syntra_social_security_and_index_hardening`
- `syntra_social_auth_profile_trigger`

The `auth.users` after-insert trigger creates a profile row. Its function uses `SECURITY DEFINER`, an empty `search_path`, schema-qualified writes, and only uses user-editable Auth metadata for profile display fields. This is a reasonable baseline, but registration and collision behavior still need dedicated test accounts and runtime tests.

## RLS and API access findings

- RLS is enabled on every application table in the exposed `public` schema.
- The `authenticated` role has table-level SELECT access; row visibility is then restricted by the RLS policies.
- The `anon` role has no SELECT privilege on these application tables. This matches the current authenticated-only baseline.
- Profile reads are currently owner-only. Profiles default to `is_private = true` and `is_discoverable = false`.
- Post reads are author-only. New posts default to `visibility = 'private'` and `status = 'draft'`.
- Comment and like reads are currently limited to the current user's own rows.
- Follow rows are visible to the two participants. Block rows are visible to the blocker.
- Notifications are readable by their recipient. Notification creation has no client insert policy, which keeps creation server-controlled.
- Reports can be created and read by their reporter. No client moderation-queue policy is present.
- Owner UPDATE policies for profiles, posts and comments include both `USING` and `WITH CHECK`, preventing ownership reassignment through those policies.

### Functional gaps to resolve before connecting the frontend

1. **Shared feed:** other signed-in users cannot currently read published public posts. Add explicit visibility-aware read policies only after defining the complete private-account, accepted-follower, and two-way block rules.
2. **Profiles:** there is no cross-user profile read policy yet. Define exactly which profile fields may be visible; do not expose email, phone, birth date, or Auth metadata.
3. **Comments and reactions:** other users cannot read comments or likes, so shared comment threads and reaction counts are not ready.
4. **Notifications:** an UPDATE RLS policy exists for the recipient, but the `authenticated` role currently has only SELECT table privilege on `notifications`. The mark-as-read path therefore needs a deliberate privilege/policy design before client integration.
5. **Communities:** group, membership, group-post, and group-rule tables are not present in the current nine-table schema. They need a separate data model and access review before migrating the local community prototype.
6. **Media:** the `post_media` table is metadata only. No Storage bucket/policies were verified in this audit. Keep media private until object read/upload/update/delete policies are separately tested.
7. **Moderation:** client users can submit their own reports, but no moderator role/queue workflow is established in the current schema.

## Advisor results

- **Security Advisor:** zero findings returned.
- **Performance Advisor:** 13 indexes are currently reported unused. The project has an empty dataset, so this is expected at this stage. Do not remove these indexes until representative queries and workload measurements exist.

A clean Advisor result is not a penetration test and does not prove every application workflow is secure.

## Current Supabase platform consideration

Supabase changed the default exposure behavior for new public-schema tables. As of 2026-10-30, tables are not automatically exposed to the Data API by default. Table grants and RLS are separate controls: grants determine whether a role can reach a table; RLS determines which rows it can access. Preserve the current least-privilege approach and explicitly grant only the roles/operations needed by each future table.

## Recommended implementation sequence

### 1.9A — Freeze and document the baseline
- Keep the existing local-only prototype unchanged.
- Keep the nine-table schema and three migrations as the current database baseline.
- Store future migrations in version control and review them before applying to the hosted database.
- Do not create a second Supabase project or duplicate the existing schema.

### 1.9B — RLS test matrix
Use isolated test accounts for:
- anonymous visitor;
- account owner;
- unrelated authenticated account;
- accepted follower;
- pending follower;
- blocked account in both directions;
- moderation operator (only after a role model is designed).

Test SELECT, INSERT, UPDATE and DELETE separately. Include attempts to change ownership IDs and notification/report fields.

### 1.9C — Shared content policies
Design and test visibility-aware profile, post, comment, and reaction reads. A public post must not bypass a private profile or a block relationship. Do not add a broad `TO authenticated USING (true)` policy.

### 1.9D — Communities and media
Design community tables and private Storage policies as separate reviewed changes. Test upload, read, overwrite, and delete behavior independently from database-table RLS.

### 1.9E — Frontend integration
Only after the preceding tests pass: connect the client using the project URL and publishable key, implement Auth/session handling, and keep local demo data separate from authenticated server data. Never put a service-role or secret key in browser code or GitHub.

## Release boundary

The current browser prototype remains local-only. This audit did not enable registration, change public visibility, expose new tables, create Storage buckets, or migrate local user data. Do not announce a production social network until authentication, RLS, media access, moderation, account recovery, mobile testing, and age-appropriate safeguards pass their acceptance tests.
