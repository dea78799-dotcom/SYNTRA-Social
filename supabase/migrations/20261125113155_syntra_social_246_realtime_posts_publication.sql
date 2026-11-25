-- SYNTRA Social 2.46 — enable live post-change notifications.
-- Realtime payloads are used only as invalidation signals. Clients re-fetch
-- post data through authenticated PostgREST queries protected by existing RLS.
alter publication supabase_realtime add table public.posts;
