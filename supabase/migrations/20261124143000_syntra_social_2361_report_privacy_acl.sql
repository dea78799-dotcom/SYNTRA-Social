-- SYNTRA Social 2.36.1 — tighten report column privileges
-- Report ownership is enforced by RLS; clients do not need to read reporter_id.

revoke select on table public.reports from authenticated;
grant select (id, target_type, target_id, reason, details, status, created_at)
  on table public.reports to authenticated;
revoke delete on table public.reports from authenticated;

-- Keep the private role table locked while documenting its only permissible row scope.
drop policy if exists syntra_owner_roles_select_self on private.syntra_owner_roles;
create policy syntra_owner_roles_select_self
  on private.syntra_owner_roles
  for select
  to authenticated
  using (user_id = (select auth.uid()));
