# SYNTRA Social 1.9C — Least-Privilege Regression Tests

**Date:** 2026-11-23  
**Status:** SQL candidate and test plan only; not applied to the live database.  
**Target:** dedicated staging project, after the schema is recreated from reviewed migrations.

## 1. Verified live baseline (read-only inspection)

- public.follows columns: follower_id, following_id, status, created_at, accepted_at.
- follows.status permits only pending and accepted.
- A consistency constraint requires pending rows to have accepted_at NULL and accepted rows to have accepted_at non-NULL.
- authenticated has table-level SELECT, INSERT and DELETE on follows; it has no UPDATE table privilege, no UPDATE column privilege, and no UPDATE policy.
- Existing follows SELECT policy allows either participant to read the relationship. Existing INSERT policy binds follower_id to auth.uid(). Existing DELETE policy allows either participant to delete.
- notifications has table-level SELECT, but no table-level UPDATE. It already has a column-level UPDATE privilege on read_at only, and no UPDATE privilege on payload.
- notifications already has a recipient-only UPDATE policy with matching USING and WITH CHECK, plus a recipient-only SELECT policy. 1.9C must not broaden notification grants or replace that policy.

## 2. Candidate migration

See [LEAST-PRIVILEGE-1.9C.sql](./sql/LEAST-PRIVILEGE-1.9C.sql).

The migration grants UPDATE on only follows.status and follows.accepted_at. Its UPDATE policy permits the target (following_id = auth.uid()) to update only a currently pending row, and requires the resulting row to be accepted with a non-null acceptance timestamp.

The current CHECK constraint does not include rejected; rejection is intentionally out of scope. If rejection is required later, design and test a separate state-transition migration rather than silently widening this one.

## 3. Catalog verification (read-only)

Run after the candidate migration on staging:

```sql
select
  has_table_privilege('authenticated', 'public.follows', 'UPDATE') as follows_table_update,
  has_column_privilege('authenticated', 'public.follows', 'status', 'UPDATE') as follows_status_update,
  has_column_privilege('authenticated', 'public.follows', 'accepted_at', 'UPDATE') as follows_accepted_at_update,
  has_column_privilege('authenticated', 'public.follows', 'follower_id', 'UPDATE') as follows_follower_id_update,
  has_column_privilege('authenticated', 'public.follows', 'following_id', 'UPDATE') as follows_following_id_update,
  has_table_privilege('authenticated', 'public.notifications', 'UPDATE') as notifications_table_update,
  has_column_privilege('authenticated', 'public.notifications', 'read_at', 'UPDATE') as notifications_read_at_update,
  has_column_privilege('authenticated', 'public.notifications', 'payload', 'UPDATE') as notifications_payload_update;
```

Expected: follows_table_update=false; follows_status_update=true; follows_accepted_at_update=true; both participant-ID update privileges false; notifications_table_update=false; notifications_read_at_update=true; notifications_payload_update=false.

Inspect the effective policies:

```sql
select tablename, policyname, cmd, roles, qual, with_check
from pg_policies
where schemaname = 'public'
  and tablename in ('follows', 'notifications')
order by tablename, policyname;
```

Expected: follows_accept_pending_request is an UPDATE policy for authenticated, with recipient/pending predicate in USING and recipient/accepted/non-null predicate in WITH CHECK. Existing notification recipient policies remain unchanged.

## 4. API-level test matrix

Use synthetic identities A (requester), B (recipient), and C (unrelated user), with valid Auth sessions/JWTs. Execute through the same Supabase Data API role used by the client, not as the database owner.

| Test | Actor | Operation | Expected |
|---|---|---|---|
| F01 | A | Create follow row with follower_id=A, following_id=B, status=pending | Allowed if other constraints pass |
| F02 | A | Create follow row with follower_id=C | Denied by INSERT policy |
| F03 | B | Update A→B row to status=accepted, accepted_at=now() | Allowed |
| F04 | A | Update own A→B row to accepted | Denied / zero rows affected |
| F05 | C | Update A→B row | Denied / zero rows affected |
| F06 | B | Change follower_id or following_id | Rejected by column privileges |
| F07 | B | Change created_at | Rejected by column privileges |
| F08 | B | Update an already accepted row through this policy | Denied / zero rows affected |
| F09 | B | Accept pending row but leave accepted_at null | Rejected by row CHECK / policy |
| F10 | A | Delete own follow relationship, if current product behavior is retained | Allowed |
| N01 | Notification recipient | Update own read_at | Allowed |
| N02 | Unrelated user | Update another recipient's read_at | Denied / zero rows affected |
| N03 | Recipient | Update payload or recipient_id | Rejected by column privileges |
| N04 | Recipient | Insert a notification through client | Denied (no client INSERT grant/policy) |

For every test, record request, HTTP/PostgREST status, affected-row count, expected result and actual result. A zero-row UPDATE is a denial, not a successful state transition.

## 5. Test setup and safety

1. Confirm a dedicated staging project exists and is isolated from production.
2. Create synthetic users and synthetic follow/notification rows only in staging.
3. Apply the reviewed migration to staging only.
4. Run catalog checks and the API matrix with separate user sessions.
5. Run Supabase Security Advisor and inspect effective grants after migration.
6. Re-run all existing RLS tests.
7. Do not connect the public prototype to this backend until the full authorization matrix passes.

No SQL in this document has been executed against the current live project.
