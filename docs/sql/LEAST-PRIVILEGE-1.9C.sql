-- SYNTRA Social 1.9C — candidate least-privilege migration
-- Reviewed against current schema on 2026-11-23.
-- DO NOT RUN ON THE LIVE PROJECT. Apply only to dedicated staging after backup.
-- Allows only the recipient to accept a pending follow request.
-- The database, not the client, sets accepted_at.
-- Current status CHECK allows only pending and accepted; rejection is out of scope.

begin;

-- Ensure no broad UPDATE permission exists for authenticated clients.
revoke update on table public.follows from authenticated;
grant update (status) on table public.follows to authenticated;

-- Set the acceptance timestamp inside PostgreSQL. This is an invoker trigger,
-- not SECURITY DEFINER; it does not grant elevated database privileges.
create or replace function public.set_follow_accepted_at()
returns trigger
language plpgsql
set search_path = ''
as $function$
begin
  if old.status = 'pending' and new.status = 'accepted' then
    new.accepted_at := pg_catalog.now();
  end if;
  return new;
end;
$function$;

-- A trigger function is only invoked by this trigger. Remove direct EXECUTE
-- grants from API roles; the migration owner creates the trigger below.
revoke all on function public.set_follow_accepted_at() from public, anon, authenticated;

drop trigger if exists follows_set_accepted_at on public.follows;
create trigger follows_set_accepted_at
before update of status on public.follows
for each row
execute function public.set_follow_accepted_at();

drop policy if exists follows_accept_pending_request on public.follows;
create policy follows_accept_pending_request
on public.follows
for update
to authenticated
using (
  following_id = (select auth.uid())
  and status = 'pending'
)
with check (
  following_id = (select auth.uid())
  and status = 'accepted'
  and accepted_at is not null
);

commit;

-- Existing participant SELECT policy is required for UPDATE.
-- Authenticated may update status only; the trigger controls accepted_at.
-- notifications is unchanged: read_at already has a column-level UPDATE grant
-- and the table has a recipient-only UPDATE policy.
