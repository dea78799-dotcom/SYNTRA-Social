#!/usr/bin/env python3
"""Static regression checks for the SYNTRA report rate-limit migration."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase/migrations/20261125090000_syntra_social_245_report_rate_limit_lock.sql"
sql = MIGRATION.read_text(encoding="utf-8").lower()

checks = {
    "migration replaces the existing report trigger function": "create or replace function public.validate_syntra_report()" in sql,
    "reporter identity rejects null and mismatched IDs": "new.reporter_id is distinct from auth.uid()" in sql,
    "transaction-scoped advisory lock is used": "pg_catalog.pg_advisory_xact_lock(" in sql,
    "lock key is deterministically scoped to the reporter": "'syntra_social:report_rate_limit:' || new.reporter_id::text" in sql,
    "advisory lock is acquired before the rolling-window count": sql.index("pg_catalog.pg_advisory_xact_lock(") < sql.index("select count(*) into recent_count"),
    "rolling-window limit remains 10 reports per 24 hours": "recent_count >= 10" in sql and "interval '24 hours'" in sql,
    "public target validation remains intact": "p.visibility = 'public'" in sql and "p.status = 'published'" in sql and "p.is_discoverable = true" in sql,
    "self-reporting remains blocked": "target_owner = new.reporter_id" in sql,
    "new reports are forced open with server timestamp": "new.status := 'open'" in sql and "new.created_at := now()" in sql,
    "trigger function execution remains revoked from client roles": "revoke all on function public.validate_syntra_report() from public, anon, authenticated;" in sql,
}

failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Report rate-limit migration checks failed: " + ", ".join(failed))
print("All SYNTRA report rate-limit migration checks passed.")
