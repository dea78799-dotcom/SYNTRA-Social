#!/usr/bin/env python3
"""Static regression tests for SYNTRA Social 2.53 session isolation."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "index.html").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")

def section(start, end):
    a = source.index(start)
    b = source.index(end, a)
    return source[a:b]

session = section("async function setCloudSession(session){", "function cloudAuthErrorMessage(")
following = section("async function refreshCloudFollowingIds(", "async function toggleCloudFollow(")
auto_sync = section("async function autoSyncCloudPosts(expectedGeneration=cloudSessionGeneration)", "async function setCloudSession(")
auto_runner = section("async function runCloudAutoSyncNow()", "function renderCloudSyncCenter()")

checks = {
    "application and README identify prototype 2.56": "SYNTRA Social Prototype 2.56" in source and "Prototype 2.55" in readme,
    "each session bootstrap advances a generation": "let cloudSessionGeneration=0;" in source and "const generation=++cloudSessionGeneration;" in session,
    "session bootstrap stops after stale awaited operations": session.count("if(!isCurrent())return false;") >= 6,
    "session switch clears account-specific notifications and privacy state": "cloudNotifications=[]" in session and "cloudFollowingIds=new Set();cloudBlockRecords=[];cloudBlockedUserIds=new Set();" in session and "cloudDeletionRequest=null" in session,
    "session switch revokes cached avatar object URLs": "cloudAvatarUrls.forEach(url=>" in session and "cloudAvatarUrls.clear();" in session and "releaseCloudAvatarPreview();" in session,
    "private Cloud posts are removed even on initial account bootstrap": "posts=posts.filter(post=>!post.cloud||post.publicCloud);" in session,
    "signed-out startup also removes persisted private Cloud posts": "posts=posts.filter(post=>!post.cloud||post.publicCloud);" in session[session.index("}else{"):],
    "viewer-specific public-post likes and bookmarks reset between accounts": "post.saved=false;post.liked=false" in session,
    "following response cannot mutate state after account switch": "if(!syntraCloudUser||syntraCloudUser.id!==userId)return false;" in following and following.index("if(!syntraCloudUser||syntraCloudUser.id!==userId)return false;") > following.index("await syntraSupabaseClient.from") and following.index("if(!syntraCloudUser||syntraCloudUser.id!==userId)return false;") < following.index("cloudFollowingIds=new Set", following.index("await syntraSupabaseClient.from")),
    "automatic sync stops between account-scoped reads after switch": auto_sync.count("if(!isCurrent())return false;") >= 3,
    "account switch releases the previous automatic-sync lock": "cloudAutoSyncPromise=null;" in session,
    "automatic sync recovery is bound to its original session generation": "const generation=cloudSessionGeneration,userId=syntraCloudUser?.id||null;" in auto_runner and "const generation=cloudSessionGeneration,userId=syntraCloudUser?.id||null;" in auto_runner and "isCurrent()" in auto_runner and "userId!==(syntraCloudUser?.id||null)" in auto_runner,
    "old sessions cannot mark a newly active account for recovery": "if(isCurrent())" in auto_runner,
    "local drafts and local-only posts are not globally cleared": "localStorage.clear()" not in session and "posts=posts.filter(post=>!post.cloud||post.publicCloud);" in session,
    "no database migration or RLS change is claimed": "No database migration, schema, grants, RLS policy" in readme,
}
failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Session isolation checks failed: " + ", ".join(failed))
print("All SYNTRA Social session-isolation checks passed.")
