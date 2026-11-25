# SYNTRA Social 2.46 — Realtime multi-device post synchronization

## What changed

- Enabled the existing `public.posts` table in the `supabase_realtime` publication. Existing row-level security policies remain in place.
- Signed-in clients subscribe to Postgres Changes for `public.posts` INSERT and UPDATE events only. Realtime events are invalidation signals only; the app re-fetches data through the existing authenticated Supabase queries, so it does not trust event payloads as authoritative content.\n- The listener subscribes to `INSERT` and `UPDATE` only. It deliberately does not subscribe to `DELETE`: Supabase documents that DELETE changes cannot be filtered by RLS in the same way, so omitting them avoids exposing identifiers from deleted private rows through an unfiltered delete event. Deletions are reconciled by the existing authenticated refresh/fallback sync.
- Events are debounced by 650 ms to coalesce bursts of writes.
- If a sync query is already in flight when an event arrives, the refresh waits for that query to settle and then runs another fetch. This avoids missing a just-committed change behind an older request.
- Subscriptions are scoped to the current account session and removed on sign-out or account switch.
- If Realtime is unavailable, the existing randomized 30–60 minute background sync, manual sync, focus/visibility refresh, and reconnect refresh remain available.
- The existing sync status line now indicates whether live updates are connected or temporarily using fallback sync.

## Security and data behavior

Realtime events are not applied directly to local posts. The client re-fetches rows via PostgREST under the existing RLS policies. Private posts remain owner-only. The publication includes only the `posts` table; no private media, report, moderation, notification, or account tables were added.

## Verification boundaries

The publication membership was verified in Supabase and the existing `posts` table has RLS enabled with authenticated SELECT permission constrained by its policies. Static regression checks cover subscription scope, debounce, in-flight refresh ordering, session cleanup, and fallback behavior. GitHub Actions checks syntax and static assertions. A true two-device end-to-end test and real Android background/reconnect test are still required.
