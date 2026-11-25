# SYNTRA Social 2.45 — Report rate-limit concurrency hardening

## Change

The report trigger now takes a PostgreSQL transaction-scoped advisory lock derived from the authenticated reporter ID before counting reports in the rolling 24-hour window.

This serializes submissions from the same account. If two report inserts arrive concurrently, the second waits for the first transaction to finish and then performs its count. Different reporter accounts use different lock keys and can submit independently.

The identity check also uses `IS DISTINCT FROM`, which rejects a null reporter ID as well as an ID that differs from `auth.uid()`.

## Preserved behavior

- Maximum 10 reports per reporter in a rolling 24-hour window.
- Reports must target public, published posts; comments on public, published posts; or public, discoverable profiles.
- Self-reporting remains rejected.
- New reports are forced to `open` and receive a server timestamp.
- The trigger function remains non-executable directly by `public`, `anon`, and `authenticated`.

## Verification boundaries

The repository regression test checks migration structure and ordering. The live Supabase migration and database function definition must be verified separately. A static check does not simulate two simultaneous database sessions, and the Android client still requires manual testing.
