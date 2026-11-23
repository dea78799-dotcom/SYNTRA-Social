#!/usr/bin/env python3
"""Mutation self-tests for SYNTRA Social's static security validator.

Runs in isolated temporary copies and ensures known unsafe regressions fail.
No network, credentials, or Supabase connection are used.
"""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_security_1_9c.py"
SQL = ROOT / "docs/sql/LEAST-PRIVILEGE-1.9C.sql"
TESTS = ROOT / "docs/LEAST-PRIVILEGE-TESTS-1.9C.md"
MATRIX = ROOT / "docs/RLS-TEST-MATRIX-1.9B.md"


def run_case(label, mutate_sql=None, mutate_tests=None):
    with tempfile.TemporaryDirectory(prefix="syntra-security-test-") as tmp:
        root = Path(tmp)
        (root / "scripts").mkdir()
        (root / "docs/sql").mkdir(parents=True)
        shutil.copy2(VALIDATOR, root / "scripts/validate_security_1_9c.py")
        sql = SQL.read_text(encoding="utf-8")
        tests = TESTS.read_text(encoding="utf-8")
        matrix = MATRIX.read_text(encoding="utf-8")
        if mutate_sql:
            sql = mutate_sql(sql)
        if mutate_tests:
            tests = mutate_tests(tests)
        (root / "docs/sql/LEAST-PRIVILEGE-1.9C.sql").write_text(sql, encoding="utf-8")
        (root / "docs/LEAST-PRIVILEGE-TESTS-1.9C.md").write_text(tests, encoding="utf-8")
        (root / "docs/RLS-TEST-MATRIX-1.9B.md").write_text(matrix, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(root / "scripts/validate_security_1_9c.py")],
            text=True, capture_output=True, check=False
        )
        if result.returncode == 0:
            raise AssertionError(f"Validator failed to reject unsafe mutation: {label}")
        print(f"PASS mutation rejected: {label}")


def baseline():
    result = subprocess.run([sys.executable, str(VALIDATOR)], text=True, capture_output=True)
    if result.returncode != 0:
        raise SystemExit(result.stdout + result.stderr)
    print("PASS baseline candidate")


def main():
    baseline()
    run_case("broad table UPDATE grant", lambda s: s.replace(
        "grant update (status) on table public.follows to authenticated;",
        "grant update on table public.follows to authenticated;"
    ))
    run_case("protected accepted_at UPDATE grant", lambda s: s.replace(
        "grant update (status) on table public.follows to authenticated;",
        "grant update (status, accepted_at) on table public.follows to authenticated;"
    ))
    run_case("missing accepted_at assignment", lambda s: s.replace(
        "new.accepted_at := pg_catalog.now();", "new.accepted_at := null;"
    ))
    run_case("wrong recipient predicate", lambda s: s.replace(
        "following_id = (select auth.uid())", "follower_id = (select auth.uid())"
    ))
    run_case("missing WITH CHECK clause", lambda s: s.replace(
        "with check (", "with check missing ("
    ))
    run_case("extra permissive policy", lambda s: s.replace(
        "commit;", "create policy unsafe_extra on public.follows for select to authenticated using (true);\ncommit;"
    ))
    run_case("SECURITY DEFINER escalation", lambda s: s.replace(
        "set search_path = ''", "security definer set search_path = ''"
    ))
    run_case("missing F03 regression case", mutate_tests=lambda s: s.replace(
        "| F03 |", "| FXX |"
    ))
    print("PASS: 7 mutation tests rejected; baseline candidate accepted.")


if __name__ == "__main__":
    main()
