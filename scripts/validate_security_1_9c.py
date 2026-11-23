#!/usr/bin/env python3
"""Dependency-free static audit for SYNTRA Social 1.9C security artifacts.

Checks the candidate SQL's structure and least-privilege contract. It is not a
PostgreSQL parser, does not connect to Supabase, and cannot prove runtime RLS.
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


def require(condition, message):
    global checks
    checks += 1
    if not condition:
        errors.append(message)


def read(path):
    require(path.is_file(), f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def norm(value):
    return re.sub(r"\s+", " ", value.lower()).strip()


sql = read(SQL_PATH)
tests = read(TEST_PATH)
matrix = read(MATRIX_PATH)
clean_sql = re.sub(r"--[^\n]*", "", sql)
sql_n = norm(clean_sql)
tests_n = norm(tests)
matrix_n = norm(matrix)

# Transaction and scope.
require(bool(re.search(r"\bbegin\s*;", sql_n)) and bool(re.search(r"\bcommit\s*;", sql_n)),
        "Migration must be wrapped in BEGIN/COMMIT.")
require(sql_n.find("begin;") < sql_n.find("commit;"),
        "COMMIT must occur after BEGIN.")
require("public.follows" in sql_n, "Candidate must target public.follows.")
require(not re.search(r"\b(public\.|\s)(notifications|profiles|posts|comments|likes)\b", sql_n),
        "Candidate must not modify unrelated application tables.")

# Least-privilege grants: broad UPDATE revoked, status column only granted.
require("revoke update on table public.follows from authenticated;" in sql_n,
        "Missing broad follows UPDATE revoke.")
require(bool(re.search(
    r"grant update\s*\(\s*status\s*\)\s*on\s+table\s+public\.follows\s+to\s+authenticated\s*;",
    sql_n
)), "Authenticated must receive UPDATE on status only.")
require(not bool(re.search(
    r"grant update\s+on\s+table\s+public\.follows\s+to\s+authenticated\s*;",
    sql_n
)), "Unsafe table-level UPDATE grant.")
require(not bool(re.search(
    r"grant update\s*\([^)]*(accepted_at|follower_id|following_id|created_at)[^)]*\)\s*on\s+table\s+public\.follows",
    sql_n
)), "Unsafe UPDATE grant includes protected follows columns.")
require(not bool(re.search(r"grant\s+.*\b(update|all)\b.*\b(public|anon)\b", sql_n)),
        "Unexpected grant to PUBLIC or anon.")

# Trigger: invoker context, fixed search_path, timestamp controlled by DB.
function_match = re.search(
    r"create\s+or\s+replace\s+function\s+public\.set_follow_accepted_at\s*\(\s*\)\s*"
    r"returns\s+trigger\s+(.*?)\$function\$\s*(.*?)\$function\$\s*;",
    sql_n, re.S
)
require(function_match is not None, "Trigger function definition/body missing or malformed.")
if function_match:
    function_header, function_body = function_match.groups()
    require("set search_path = ''" in function_header,
            "Trigger function must use an empty search_path.")
    require("security definer" not in function_header,
            "Trigger must not use SECURITY DEFINER.")
    require("old.status = 'pending' and new.status = 'accepted'" in function_body,
            "Timestamp assignment must be limited to pending-to-accepted transition.")
    require("new.accepted_at := pg_catalog.now();" in function_body,
            "Database timestamp assignment is missing.")
    require("return new;" in function_body,
            "Trigger must return NEW.")
require("revoke all on function public.set_follow_accepted_at() from public, anon, authenticated;" in sql_n,
        "Direct function EXECUTE grants must be revoked from API roles.")
require("before update of status on public.follows" in sql_n,
        "Trigger must fire BEFORE UPDATE OF status.")
require("execute function public.set_follow_accepted_at();" in sql_n,
        "Trigger must invoke the reviewed function.")
require("drop trigger if exists follows_set_accepted_at on public.follows;" in sql_n,
        "Trigger creation should be idempotent.")

# Policy: exact role, old/new row restrictions and no accidental extra policy.
policy_match = re.search(
    r"create\s+policy\s+follows_accept_pending_request\s+on\s+public\.follows\s+"
    r"for\s+update\s+to\s+authenticated\s+using\s*\((.*?)\)\s+with\s+check\s*\((.*?)\)\s*;",
    sql_n, re.S
)
require(policy_match is not None, "Expected UPDATE policy with USING and WITH CHECK is missing/malformed.")
if policy_match:
    using, check = map(norm, policy_match.groups())
    require("following_id = (select auth.uid())" in using,
            "USING must bind the recipient to auth.uid().")
    require("status = 'pending'" in using,
            "USING must restrict the old row to pending.")
    require("following_id = (select auth.uid())" in check,
            "WITH CHECK must bind the recipient to auth.uid().")
    require("status = 'accepted'" in check,
            "WITH CHECK must require accepted state.")
    require("accepted_at is not null" in check,
            "WITH CHECK must require accepted_at.")
require("drop policy if exists follows_accept_pending_request on public.follows;" in sql_n,
        "Named policy drop should make the migration repeatable.")
policies = re.findall(r"create\s+policy\s+([a-z0-9_]+)", sql_n)
require(policies == ["follows_accept_pending_request"],
        "Candidate must not create extra policies.")

# Notifications remain outside this migration; documentation preserves scope.
require("notifications is unchanged" in norm(sql),
        "SQL comments must document that notifications are unchanged.")
require("read_at" in tests_n and "payload" in tests_n,
        "Regression plan must preserve notification read_at-only access.")
require("not applied to the live database" in tests_n,
        "Test plan must state migration is not applied live.")
require("not as the database owner" in tests_n,
        "API tests must avoid owner-bypass testing.")
for test_id in ("f01", "f02", "f03", "f04", "f05", "f06", "f07", "f08", "f09", "f10",
                "n01", "n02", "n03", "n04"):
    require(bool(re.search(rf"\b{test_id}\b", tests_n)), f"Missing regression case {test_id.upper()}.")
require("notifications" in matrix_n and "read_at" in matrix_n,
        "RLS matrix must retain notification read_at scope.")
require("sets accepted_at" in matrix_n or "database trigger" in matrix_n,
        "RLS matrix must describe database-controlled accepted_at.")

if errors:
    print(f"FAIL: {len(errors)} issue(s), {checks} checks executed.")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)
print(f"PASS: {checks} static security contract checks.")
print("Scope: candidate SQL/document static audit only; no PostgreSQL, Supabase API, JWT, or runtime RLS test.")
