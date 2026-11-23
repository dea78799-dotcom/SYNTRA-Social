# SYNTRA SOCIAL — Backend Architecture v1

**Status:** Design only. No live Supabase project is currently connected to this workspace.
**Applies to:** SYNTRA Social Prototype 1.0 and the planned first multi-user release.
**Principle:** Do not connect the public prototype to real user data until authentication, authorization, moderation, privacy and recovery have been reviewed.

## 1. Current boundary

The current GitHub Pages app is a browser-local prototype:
- Posts, profile settings, follows, messages and notifications use browser storage.
- Image/video files are stored in IndexedDB on the current browser.
- Nothing is uploaded to a SYNTRA server or synchronized to another device.
- There are no real accounts, server-side permissions, moderation tools or live messaging.

The backend must be introduced as a separate environment. Do not silently convert local demo data into public posts.

## 2. Proposed service layout

- **Web client:** existing mobile-first HTML/CSS/JavaScript prototype, progressively migrated to a modular client.
- **Identity:** Supabase Auth. The browser receives only the publishable key; never ship a service-role or secret key.
- **Database:** Supabase Postgres. All client-accessible tables in the exposed public schema must have RLS enabled.
- **Media:** private Supabase Storage bucket for user uploads. Storage policies must be designed separately from table policies.
- **Trusted operations:** Edge Functions for moderation queues, rate-limited actions, notification creation and any operation requiring secrets.
- **Realtime:** add only after authorization rules for each channel are verified. Do not use polling loops as a substitute.

## 3. Initial data model

| Table | Purpose | Ownership / access rule |
|---|---|---|
| profiles | Public-facing username, display name, bio and avatar path | One row per auth.users.id; never store email, phone or birth date in public profile rows |
| posts | Text posts and visibility state | Author owns insert/update/delete; reads depend on visibility, follow state and blocks |
| post_media | Metadata for uploaded image/video objects | Owner controls metadata; object access also checked by Storage RLS |
| follows | Follow requests and accepted relationships | Requester creates request; target account controls acceptance |
| blocks | User block relationships | Only the blocker can create/remove their own block |
| comments | Comments attached to posts | Author owns comment; access follows parent-post visibility |
| likes | One reaction per user per post | Unique (post_id, user_id); user can remove only their own reaction |
| notifications | Server-generated account activity | Recipient can read/mark read; client cannot forge notifications |
| reports | Reports for posts, comments or accounts | Reporter can create and view own reports; moderation access is server-side |

Do not create a direct-message table in the first backend milestone. First establish block/report controls, safe defaults, moderation workflow and age-appropriate safeguards.

## 4. Privacy and authorization baseline

1. New profiles default to private / not discoverable. A user must deliberately change visibility.
2. Do not expose email, phone, date of birth, authentication metadata or private account fields through public profile queries.
3. Enable RLS on every exposed application table before granting browser access.
4. Every ownership policy must compare the row owner with (select auth.uid()); checking only the authenticated role is insufficient.
5. UPDATE policies need both USING and WITH CHECK so users cannot transfer ownership.
6. A user must not read, follow, message or interact with an account that has blocked them; enforce this in database policies and trusted operations, not only in the UI.
7. Storage objects remain private by default. A table policy does not protect Storage objects; write and test Storage policies separately.
8. Never expose service-role keys, database passwords or private environment variables in GitHub Pages or client JavaScript.
9. Notifications and moderation outcomes are created by trusted server-side operations, not arbitrary client inserts.
10. Add rate limits, upload size/type validation, abuse reporting and audit logging before public access.

## 5. First implementation milestones

### B0 — Foundation
- Connect an existing Supabase project or explicitly create a new one after reviewing its cost and region.
- Confirm project health, region, API settings and current schema.
- Add versioned database migrations in the repository.
- Establish staging and production separation.

### B1 — Identity and profiles
- Email verification and secure session lifecycle.
- Username uniqueness and profile ownership.
- Private-by-default visibility and profile deletion/export flow.
- RLS tests for owner, another signed-in user and anonymous visitor.

### B2 — Posts and media
- Create/edit/delete posts.
- Public/followers/private visibility checks.
- Private media bucket with owner/path policies.
- Upload limits, MIME validation and cleanup of orphaned media.

### B3 — Social interactions
- Follow requests and acceptance.
- Likes and comments.
- Block and report flows before adding direct messages.
- Server-generated notifications and rate limits.

### B4 — Realtime and release hardening
- Realtime subscriptions only for authorized rows/channels.
- Abuse review, accessibility, mobile browser testing, backups and incident response.
- Independent security review before any public launch.

## 6. Required verification before each milestone

- Run Supabase Security Advisors and resolve exposed-table / missing-RLS findings.
- Test RLS with anonymous, owner, unrelated authenticated user, blocked user and accepted follower identities.
- Verify Storage read, upload, overwrite and delete behavior with separate test accounts.
- Confirm no secret key or personal data is present in built frontend assets.
- Test account export/deletion, failed uploads, quota errors and recovery paths.
- Keep the current local-only prototype available until the backend release passes acceptance tests.

## 7. Official references

- Supabase architecture: https://supabase.com/docs/guides/getting-started/architecture
- Supabase Row Level Security: https://supabase.com/docs/guides/database/postgres/row-level-security
- Supabase API security: https://supabase.com/docs/guides/api/securing-your-api
- Supabase Storage access control: https://supabase.com/docs/guides/storage/security/access-control
- Supabase API keys: https://supabase.com/docs/guides/getting-started/api-keys

**Release rule:** Prototype 1.0 remains a local demo. Do not label it a real social network or enable public user registration until B0–B4 security and product gates are complete.