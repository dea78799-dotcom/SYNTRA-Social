create table if not exists public.post_bookmarks (
  user_id uuid not null references auth.users(id) on delete cascade,
  post_id uuid not null references public.posts(id) on delete cascade,
  created_at timestamptz not null default now(),
  constraint post_bookmarks_pkey primary key (user_id, post_id)
);

create index if not exists post_bookmarks_user_created_idx
  on public.post_bookmarks (user_id, created_at desc);

alter table public.post_bookmarks enable row level security;

revoke all on table public.post_bookmarks from anon, authenticated;
grant select, insert, delete on table public.post_bookmarks to authenticated;

drop policy if exists post_bookmarks_select_own on public.post_bookmarks;
create policy post_bookmarks_select_own
  on public.post_bookmarks
  for select to authenticated
  using ((select auth.uid()) = user_id);

drop policy if exists post_bookmarks_insert_public_posts on public.post_bookmarks;
create policy post_bookmarks_insert_public_posts
  on public.post_bookmarks
  for insert to authenticated
  with check (
    (select auth.uid()) = user_id
    and exists (
      select 1
      from public.posts p
      where p.id = post_id
        and p.visibility = 'public'
        and p.status = 'published'
    )
  );

drop policy if exists post_bookmarks_delete_own on public.post_bookmarks;
create policy post_bookmarks_delete_own
  on public.post_bookmarks
  for delete to authenticated
  using ((select auth.uid()) = user_id);
