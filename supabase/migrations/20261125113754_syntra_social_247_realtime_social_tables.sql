-- SYNTRA Social 2.47 — expand live sync to RLS-protected social data.
-- Only INSERT/UPDATE events are consumed by clients. DELETE events are
-- intentionally excluded because they are not filtered by RLS in the same way.
alter publication supabase_realtime
  add table public.post_media,
             public.comments,
             public.likes,
             public.notifications,
             public.post_bookmarks;
