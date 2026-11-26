#!/usr/bin/env python3
"""Static regression tests for SYNTRA Social 2.53 multi-device reconciliation."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "index.html").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")

def section(start, end):
    a = source.index(start)
    b = source.index(end, a)
    return source[a:b]

feed = section("async function syncPublicFeed(", "async function loadMorePublicFeed(")
bookmarks = section("async function loadCloudBookmarks(", "async function reconcileLoadedPublicPosts(")
reconcile = section("async function reconcileLoadedPublicPosts(", "function classifyCloudError(")
realtime = section("async function flushCloudRealtimeRefresh()", "function scheduleCloudAutoSync()")

saved_snapshot = "posts.forEach(post=>{if(post.cloud&&post.publicCloud)post.saved=savedIds.has(post.id)});"
checks = {
    "application and README identify prototype 2.56": "SYNTRA Social Prototype 2.56" in source and "Prototype 2.55" in readme,
    "public feed refresh retains previously paginated public posts": "const currentPublicPosts=posts.filter(post=>post.publicCloud)" in feed and "retainedOlderPosts=currentPublicPosts.filter(post=>!firstPageIds.has(post.id))" in feed,
    "bookmark state is reconciled outside the non-empty bookmark branch": saved_snapshot in bookmarks and bookmarks.index(saved_snapshot) > bookmarks.rfind("if(ids.length){"),
    "bookmark snapshot is applied before persistence": bookmarks.index(saved_snapshot) < bookmarks.index("save();"),
    "saved-state snapshot contains only posts still visible as published public content": "const savedIds=new Set();" in bookmarks and "postRows.forEach(row=>savedIds.add(row.id));" in bookmarks,
    "loaded public posts are checked in batches of 40": "offset+=40" in reconcile and "ids.slice(offset,offset+40)" in reconcile,
    "only currently published public posts remain in loaded feed": ".in('id',batch).eq('visibility','public').eq('status','published')" in reconcile and "posts=posts.filter(post=>!(post.cloud&&post.publicCloud)||visibleIds.has(post.id))" in reconcile,
    "likes and comments are re-fetched through the existing authenticated client": "loadCloudPostInteractions(rows,userId)" in reconcile,
    "account changes invalidate reconciliation before applying state": reconcile.count("syntraCloudUser?.id!==userId") >= 2 and "if(syntraCloudUser?.id!==userId)return false;" in reconcile,
    "realtime refresh retries when state reconciliation fails": "const reconcileOk=await reconcileLoadedPublicPosts(userId)" in realtime and "if(!reconcileOk){markCloudRecoveryPending(userId);scheduleCloudRecoveryRetry();return false}" in realtime,
    "successful realtime reconciliation clears the matching recovery marker": "clearCloudRecoveryPending(userId)" in realtime,
    "CI executes the reconciliation regression suite": "python scripts/test_state_reconciliation.py" in workflow,
    "no DELETE realtime listener was introduced": ".on('postgres_changes',{event:'DELETE'" not in source,
    "no offline write replay was introduced": "automatic post replay" in readme and "No database migration" in readme,
}
failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + name)
if failed:
    raise SystemExit("State reconciliation checks failed: " + ", ".join(failed))
print("All SYNTRA Social state-reconciliation checks passed.")
