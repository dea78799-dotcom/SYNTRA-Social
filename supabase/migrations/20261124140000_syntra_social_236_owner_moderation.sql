-- SYNTRA Social 2.36 — Owner-only moderation with mandatory AAL2
-- Owner assignment is intentionally empty: only the project owner may seed it from the Supabase SQL Editor.
create schema if not exists private;
create table if not exists private.syntra_owner_roles (
 user_id uuid primary key references auth.users(id) on delete cascade,
 role text not null default 'owner' check (role = 'owner'),
 created_at timestamptz not null default now()
);
alter table private.syntra_owner_roles enable row level security;
revoke all on table private.syntra_owner_roles from public, anon, authenticated;
create or replace function private.is_syntra_owner()
returns boolean language sql stable security definer set search_path = pg_catalog
as $$
 select exists(select 1 from private.syntra_owner_roles r where r.user_id=(select auth.uid()) and r.role='owner');
$$;
revoke all on function private.is_syntra_owner() from public, anon;
grant usage on schema private to authenticated;
grant execute on function private.is_syntra_owner() to authenticated;
create or replace function public.syntra_owner_status()
returns boolean language sql stable security invoker set search_path = pg_catalog, private
as $$ select private.is_syntra_owner(); $$;
revoke all on function public.syntra_owner_status() from public, anon;
grant execute on function public.syntra_owner_status() to authenticated;

create table if not exists private.syntra_report_moderation_audit (
 id uuid primary key default gen_random_uuid(),
 report_id uuid not null references public.reports(id) on delete restrict,
 actor_id uuid not null references auth.users(id) on delete restrict,
 old_status text not null,
 new_status text not null,
 note text not null default '',
 created_at timestamptz not null default now()
);
create index if not exists syntra_report_moderation_audit_created_idx on private.syntra_report_moderation_audit(created_at desc);
alter table private.syntra_report_moderation_audit enable row level security;
revoke all on table private.syntra_report_moderation_audit from public, anon;
grant select on table private.syntra_report_moderation_audit to authenticated;
drop policy if exists syntra_owner_audit_select_aal2 on private.syntra_report_moderation_audit;
create policy syntra_owner_audit_select_aal2 on private.syntra_report_moderation_audit for select to authenticated
using (private.is_syntra_owner() and (select auth.jwt()->>'aal')='aal2');

create or replace function private.syntra_moderate_report(p_report_id uuid,p_status text,p_note text default '')
returns jsonb language plpgsql security definer set search_path = pg_catalog, public, private, auth
as $$
declare
 v_actor uuid := auth.uid();
 v_old_status text;
 v_note text := coalesce(p_note,'');
begin
 if v_actor is null then raise exception 'Authentication required.' using errcode='42501'; end if;
 if coalesce(auth.jwt()->>'aal','aal1') <> 'aal2' then raise exception 'Owner two-factor verification (AAL2) is required.' using errcode='42501'; end if;
 if not private.is_syntra_owner() then raise exception 'Owner permission required.' using errcode='42501'; end if;
 if p_status not in ('reviewing','resolved','dismissed') then raise exception 'Unsupported moderation status.' using errcode='22023'; end if;
 if length(v_note)>500 then raise exception 'Moderation note is limited to 500 characters.' using errcode='22023'; end if;
 select r.status into v_old_status from public.reports r where r.id=p_report_id for update;
 if not found then raise exception 'Report not found.' using errcode='P0002'; end if;
 if not ((v_old_status='open' and p_status in ('reviewing','resolved','dismissed')) or (v_old_status='reviewing' and p_status in ('resolved','dismissed'))) then
  raise exception 'This report is already closed or the transition is not allowed.' using errcode='22023';
 end if;
 update public.reports set status=p_status where id=p_report_id;
 insert into private.syntra_report_moderation_audit(report_id,actor_id,old_status,new_status,note)
 values(p_report_id,v_actor,v_old_status,p_status,v_note);
 return jsonb_build_object('ok',true,'report_id',p_report_id,'status',p_status);
end;
$$;
revoke all on function private.syntra_moderate_report(uuid,text,text) from public, anon;
grant execute on function private.syntra_moderate_report(uuid,text,text) to authenticated;
create or replace function public.syntra_moderate_report(p_report_id uuid,p_status text,p_note text default '')
returns jsonb language sql security invoker set search_path = pg_catalog, private
as $$ select private.syntra_moderate_report(p_report_id,p_status,p_note); $$;
revoke all on function public.syntra_moderate_report(uuid,text,text) from public, anon;
grant execute on function public.syntra_moderate_report(uuid,text,text) to authenticated;
create or replace function public.syntra_get_moderation_audit(p_limit integer default 50)
returns table(id uuid,report_id uuid,old_status text,new_status text,note text,created_at timestamptz)
language sql stable security invoker set search_path = pg_catalog, private
as $$
 select a.id,a.report_id,a.old_status,a.new_status,a.note,a.created_at
 from private.syntra_report_moderation_audit a order by a.created_at desc
 limit least(greatest(coalesce(p_limit,50),1),100);
$$;
revoke all on function public.syntra_get_moderation_audit(integer) from public, anon;
grant execute on function public.syntra_get_moderation_audit(integer) to authenticated;
drop policy if exists reports_select_owner_aal2 on public.reports;
create policy reports_select_owner_aal2 on public.reports for select to authenticated
using (private.is_syntra_owner() and (select auth.jwt()->>'aal')='aal2');
revoke select (reporter_id) on table public.reports from authenticated;
revoke update on table public.reports from authenticated;
revoke update (id,reporter_id,target_type,target_id,reason,details,status,created_at) on table public.reports from authenticated;
