# SYNTRA Social Prototype 2.53 — Session Isolation Guard

## Problem

A browser can restore Cloud-backed records from local storage before Supabase finishes restoring the authenticated session. Session changes can also overlap with asynchronous account-specific reads. Without a generation guard, a previous bootstrap or automatic-sync task can continue after a newer account becomes active.

## Implementation

- The in-memory session generation increases on every setCloudSession call.
- The bootstrap captures its generation and checks it after each awaited account-scoped operation. A stale bootstrap returns without starting Realtime, updating the active account UI, or scheduling account-specific recovery.
- On an identity change, account-scoped UI/cache state is cleared immediately: notifications, follows, blocks, deletion request, avatar URL cache, and avatar preview.
- The loaded post collection removes private Cloud posts on every identity change, including null-to-user during first session restoration. Public Cloud posts remain, but the active viewer's liked and saved flags are reset.
- refreshCloudFollowingIds verifies the active account after the Supabase response before replacing the shared following set.
- Automatic sync captures the current session generation and account ID. A completion or failure from a stale session cannot clear or mark recovery for the currently active account.
- autoSyncCloudPosts stops between account-scoped datasets as soon as the active user changes.

## Preserved behavior and boundaries

- Local-only posts and locally saved composer drafts are not removed.
- No auth tokens, credentials, or session secrets are read or copied by this feature.
- No database schema, migration, grants, RLS policies, or Realtime subscriptions changed.
- This is client-side state isolation, not server-side authorization. Supabase RLS remains the access-control boundary.
- Static CI tests do not replace real-device testing with two accounts and interrupted network conditions.

## Verification

The scripts/test_session_isolation.py suite checks generation invalidation, stale async guards, cache cleanup, initial private-post cache filtering, viewer-specific interaction reset, stale following response protection, and recovery scoping.
