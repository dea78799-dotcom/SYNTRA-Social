# SYNTRA Social 2.48 — Conflict-safe Cloud post editing

## Problem

Two devices can open the same Cloud post for editing. Without a version check, the later save can silently overwrite the earlier device's changes.

## Behavior

1. Before saving, the client reads the current post body and `updated_at` from Supabase, scoped by post ID and the authenticated author ID.
2. If the current server body differs from the body originally loaded into the editor, the save is rejected and the user is asked to reload.
3. Otherwise, the client updates the body only where the row still has the exact `updated_at` value read in step 1.
4. If another device commits an edit between steps 1 and 3, the conditional update affects no row. SYNTRA reports a conflict rather than overwriting the newer content.

The existing database trigger updates `posts.updated_at` on each update. No schema or RLS change is required.

## Scope and limitations

- Applies to Cloud posts edited from the creator/profile editor.
- Local-only posts retain their existing local save path.
- This is optimistic concurrency control, not automatic merge. The user must reload and reapply their intended changes after a conflict.
- Other concurrent mutations, including profile changes, comments, likes, and media metadata, are not covered by this feature.
- Automated checks are static regression checks. A live two-device simultaneous-edit test remains necessary.
