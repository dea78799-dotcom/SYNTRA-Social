# SYNTRA Social Prototype 2.51 — Sync Recovery Engine

## Fixed recovery completion criteria

A sync cycle is successful only when the required reads complete for:
- The public feed and its interaction data
- The signed-in user's own posts and media metadata
- Notifications
- Bookmarks and their visible public post data

Previously, automatic sync ignored the boolean results of notification and bookmark loading. It could clear the recovery marker after a successful public-feed read even when one of those datasets failed. Prototype 2.51 aggregates these results and preserves the recovery marker when any required dataset fails.

## Forced refresh

`syncPublicFeed(silent, force)` now supports an explicit force flag. Recovery and account-session bootstrap bypass the 30-second feed debounce. Normal callers retain the existing debounce behavior.

## Session bootstrap

When a user signs in or the session is restored, SYNTRA attempts each required dataset independently. One failed read does not prevent the remaining datasets from being attempted. If the same account is still active and any required read fails, the account-scoped recovery marker is preserved and a retry is scheduled.

## Safety

- Reads continue through the existing authenticated Supabase client and RLS policies.
- No database schema, migration, grant, or RLS changes.
- No queued offline writes or automatic replay of posts, comments, likes, or bookmarks.
- Recovery markers contain only the account ID and retry metadata, not post content or credentials.
