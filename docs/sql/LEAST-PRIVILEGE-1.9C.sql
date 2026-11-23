-- SYNTRA Social 1.9C — candidate least-privilege migration
-- Reviewed against current schema on 2026-11-23.
-- DO NOT RUN ON THE LIVE PROJECT. Apply only to dedicated staging after backup.
-- Allows only the recipient to accept a pending follow request.
-- Current status CHECK allows only pending and accepted; rejection is out of scope.

begin;

revoke update on table public.follows from authenticated;
grant update (status, accepted_at) on table public.follows to authenticated;

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
-- notifications is intentionally unchanged: read_at already has a
-- column-level UPDATE grant and the table has a recipient-only UPDATE policy.
