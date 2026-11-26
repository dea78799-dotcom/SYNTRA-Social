# SYNTRA Social Prototype 2.56 — Background Sync Queue

## Scope

Prototype 2.56 introduces an in-memory, account-scoped queue for background read/refresh orchestration. It is not a generic job runner and does not accept server writes.

## Queue behavior

- Maximum six jobs total, counting the active job and pending jobs.
- One job runs at a time. Job lifecycle states are `pending`, `running`, `succeeded`, `failed`, and `cancelled`.
- An unexpected task exception is recorded in existing diagnostics and schedules the existing account-scoped recovery backoff.
- Duplicate jobs are coalesced by job key, account ID, and session generation.
- Each job captures the session generation and account ID. Pending jobs are cancelled on account transitions. Active jobs are marked cancelled and must stop at the next orchestration checkpoint.
- The queue exposes a small status line in the existing Sync Center.
- Outcome history is in-memory and capped at twelve entries. No queue payload or account identifier is persisted.
- If capacity is exhausted, the new task is rejected and the existing account-scoped recovery scheduler is asked to retry later.

## Integrated operations

- Automatic account refresh.
- Manual Sync Center recovery.
- Realtime-triggered refresh and public-feed reconciliation.

Session bootstrap remains a direct sequence guarded by the existing session-generation checks. This avoids delaying the initial account load behind queued background work.

## Retry and offline behavior

The queue does not own timers or add automatic retry loops. Existing recovery backoff remains responsible for retry scheduling. Offline, hidden-page, and stale-session guards remain in force.

## Safety boundaries

No post publication, edit, delete, like, comment, or other write is queued or replayed. The queue does not change Supabase schema, migrations, grants, RLS policies, or Realtime publication. It orchestrates existing read/refresh functions only.

## Verification limits

Static regression tests and GitHub Actions validate queue invariants and integration points. They do not prove Android background execution, real network interruption behavior, or cross-device runtime behavior. Those still require device testing.
