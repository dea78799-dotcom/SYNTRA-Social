# SYNTRA Social 2.47 — Realtime multi-device data synchronization

## Tables enabled

The existing `supabase_realtime` publication now includes:
- `posts`
- `post_media`
- `comments`
- `likes`
- `notifications`
- `post_bookmarks`

All six tables had RLS enabled and authenticated SELECT privileges verified before they were added. Existing policies remain unchanged:
- Posts: published public rows or rows owned by the signed-in user.
- Post media: owner-only metadata.
- Comments and likes: rows allowed by their existing public-or-own policies, including block checks.
- Notifications: recipient-only.
- Bookmarks: owner-only.

## Client behavior

- Signed-in devices subscribe to INSERT/UPDATE events on posts, media, comments, and notifications; INSERT events on likes and bookmarks.
- Event payloads are invalidation signals only. The client re-fetches data using existing authenticated Supabase queries and the existing RLS policies.
- A 650 ms debounce coalesces multiple events. If an older sync request is already running, the Realtime refresh waits for it and fetches again.
- The same channel is scoped to the current account and removed on sign-out/account switch.
- Existing randomized 30–60 minute fallback sync, manual sync, and foreground/reconnect refresh remain.

## Deliberate DELETE-event exclusion

No DELETE event is subscribed to. Supabase documents that DELETE changes cannot be filtered by RLS in the same way as normal row changes. Avoiding those events prevents a subscription from exposing identifiers for deleted private rows. Deletions are reconciled through authenticated refreshes, foreground/reconnect sync, and the existing fallback cycle.

This means likes/bookmarks/comments removed on another device may not disappear immediately on a second device; they are reconciled on the next authenticated refresh. INSERT/UPDATE activity is synchronized through Realtime.

## Verification

- Supabase migration history confirms 2.47 is applied.
- Publication membership was queried directly and contains exactly the six intended public tables.
- RLS was verified enabled on all six tables; authenticated SELECT grants and policy names were inspected.
- GitHub Actions checks inline JavaScript syntax, the 2.46/2.47 migration files, event scope, debounce, in-flight request ordering, account cleanup, and fallback behavior.
- No live two-device or Android background/reconnect test has been performed yet.
