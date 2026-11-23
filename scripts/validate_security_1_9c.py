#!/usr/bin/env python3
"""Dependency-free static checks for SYNTRA Social backend security artifacts.

This validates the reviewed 1.9C SQL/document contract only. It does not
connect to PostgreSQL, emulate Supabase Auth, or prove RLS behavior.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SQL_PATH = ROOT / "docs/sql/LEAST-PRIVILEGE-1.9C.sql"
TEST_PATH = ROOT / "docs/LEAST-PRIVILEGE-TESTS-1.9C.md"
MATRIX_PATH = ROOT / "docs/RLS-TEST-MATRIX-1.9B.md"

errors = []
checks = 0


def require(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        errors.append(message)


def read(path: Path) -> str:
    require(path.is_file(), f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


sql = read(SQL_PATH)
tests = read(TEST_PATH)
matrix = read(MATRIX_PATH)
sql_lower = re.sub(r"\s+", " ", sql.lower())
tests_lower = tests.lower()
matrix_lower = matrix.lower()

# Migration safety and least-privilege contract.
require("begin;" in sql_lower and "commit;" in sql_lower,
        "Migration must be transaction-wrapped.")
require("revoke update on table public.follows from authenticated;" in sql_lower,
        "Missing revoke of broad follows UPDATE privilege.")
require(bool(re.search(
    r"grant update\s*\(\s*status\s*\)\s*on\s+table\s+public\.follows\s+to\s+authenticated",
    sql_lower
)), "Authenticated must receive UPDATE on status only.")
require(not bool(re.search(
    r"grant update\s+on\s+table\s+public\.follows\s+to\s+authenticated",
    sql_lower
)), "Unsafe table-level UPDATE grant detected on follows.")
require("following_id = (select auth.uid())" in sql_lower,
        "UPDATE policy must bind the recipient to auth.uid().")
require("status = 'pending'" in sql_lower,
        "UPDATE policy must restrict the old row to pending.")
require("status = 'accepted'" in sql_lower,
        "UPDATE policy must restrict the new row to accepted.")
require("accepted_at is not null" in sql_lower,
        "UPDATE policy must require the acceptance timestamp.")
require("before update of status on public.follows" in sql_lower,
        "Missing BEFORE UPDATE OF status trigger.")
require("new.accepted_at := pg_catalog.now();" in sql_lower,
        "Trigger must set accepted_at using the database clock.")
require("set search_path = ''" in sql_lower,
        "Trigger function must use an empty search_path.")
require("security definer" not in sql_lower,
        "SECURITY DEFINER is not permitted in this candidate.")
require("revoke all on function public.set_follow_accepted_at() from public, anon, authenticated;" in sql_lower,
        "Trigger function direct EXECUTE grants must be revoked from API roles.")
require("drop policy if exists follows_accept_pending_request" in sql_lower,
        "Migration must be repeatable for the named policy.")
require("notifications" in sql_lower and "read_at" in sql_lower,
        "Migration must document the unchanged notification permission boundary.")

# Regression-plan coverage.
for test_id in ("f01", "f02", "f03", "f04", "f05", "f06", "f07", "f08",
                "f09", "f10", "n01", "n02", "n03", "n04"):
    require(bool(re.search(rf"\b{test_id}\b", tests_lower)),
            f"Missing regression case {test_id.upper()}.")
require("not applied to the live database" in tests_lower,
        "Test plan must state that the migration has not been applied.")
require("not as the database owner" in tests_lower,
        "API tests must use the client role, not owner-bypass SQL.")
require("notifications" in matrix_lower and "read_at" in matrix_lower,
        "RLS matrix must retain notification read_at scope.")
require("database trigger" in matrix_lower or "sets accepted_at" in matrix_lower,
        "RLS matrix must describe database-controlled accepted_at.")

if errors:
    print(f"FAIL: {len(errors)} issue(s), {checks} checks executed.")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print(f"PASS: {checks} static security checks.")
print("Scope: reviewed SQL/document contract only; no live database or API test was run.")
