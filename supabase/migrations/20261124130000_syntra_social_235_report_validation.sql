-- SYNTRA Social 2.35 — server-side report validation and abuse limits
-- Reports remain visible only to their reporter through the existing RLS policies.

create or replace function public.validate_syntra_report()
returns trigger
language plpgsql
security definer
set search_path = pg_catalog, public, auth
as $$
declare
  target_owner uuid;
  recent_count integer;
begin
  if auth.uid() is null or new.reporter_id <> auth.uid() then
    raise exception 'You can only submit reports for your own account.'
      using errcode = '42501';
  end if;

  select count(*) into recent_count
  from public.reports r
  where r.reporter_id = new.reporter_id
    and r.created_at >= now() - interval '24 hours';

  if recent_count >= 10 then
    raise exception 'Report limit reached. Try again later.'
      using errcode = 'P0001';
  end if;

  if new.target_type = 'post' then
    select p.author_id into target_owner
    from public.posts p
    where p.id = new.target_id
      and p.visibility = 'public'
      and p.status = 'published';
  elsif new.target_type = 'comment' then
    select c.author_id into target_owner
    from public.comments c
    join public.posts p on p.id = c.post_id
    where c.id = new.target_id
      and p.visibility = 'public'
      and p.status = 'published';
  elsif new.target_type = 'profile' then
    select p.id into target_owner
    from public.profiles p
    where p.id = new.target_id
      and p.is_private = false
      and p.is_discoverable = true;
  else
    raise exception 'Unsupported report target.'
      using errcode = '22023';
  end if;

  if target_owner is null then
    raise exception 'The reported content is unavailable or not public.'
      using errcode = 'P0002';
  end if;

  if target_owner = new.reporter_id then
    raise exception 'You cannot report your own content.'
      using errcode = '22023';
  end if;

  new.status := 'open';
  new.created_at := now();
  return new;
end;
$$;

drop trigger if exists reports_validate_before_insert on public.reports;
create trigger reports_validate_before_insert
before insert on public.reports
for each row execute function public.validate_syntra_report();

revoke all on function public.validate_syntra_report() from public, anon, authenticated;
