# SYNTRA Social Prototype 2.50 — Data Consistency Engine

## Purpose

Prototype 2.50 extends the existing manual integrity audit with a read-only comparison between locally loaded Cloud posts and records returned by the currently authenticated Supabase session.

## Checks

- Whether locally loaded Cloud posts are still returned by the authenticated posts query.
- Whether the local author ID matches the visible server row.
- Whether each visible post_media row belongs to the same author as its parent post.
- Whether media IDs attached to a local Cloud post still have matching remote metadata, and whether remote metadata is linked in the local post representation.
- Duplicate remote comment IDs, comments whose parent is not visible in the audited result, duplicate (post_id, user_id) like pairs, and likes whose parent is not visible in the audited result.

## Safety and coverage

- All requests use the existing signed-in Supabase client; RLS remains authoritative.
- Post IDs are queried in batches of 40.
- Account changes cancel the in-flight audit result.
- The audit performs SELECT queries only. It never inserts, updates, deletes, repairs, or replays records.
- A post missing from the result is reported as not visible / not returned. This does not prove deletion: RLS, visibility changes, moderation, or account changes can affect what is returned.
- The audit covers only Cloud posts currently loaded in the browser. Comment queries are capped at 1,000 rows per batch and the report marks this possible truncation.
- Cloud checks are skipped when the user is signed out or offline; local integrity checks still run.
- Exported integrity report version is 3. It includes IDs needed to locate findings, but does not include post bodies, email addresses, credentials, access tokens, or media contents.

## Database impact

No SQL migration, schema, RLS, grants, or Storage policy changes are part of Prototype 2.50.
