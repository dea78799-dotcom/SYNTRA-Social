#!/usr/bin/env python3
"""Static regression tests for SYNTRA Social 2.52 sync recovery."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "index.html").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")

def section(start, end):
    a = source.index(start)
    b = source.index(end, a)
    return source[a:b]

auto_sync = section("async function autoSyncCloudPosts()", "async function setCloudSession(")
feed_sync = section("async function syncPublicFeed(", "async function loadMorePublicFeed(")
session_sync = section("async function setCloudSession(", "function cloudAuthErrorMessage(")
retry_sync = section("async function retryCloudSyncCenter(", "function recordCloudDiagnostic(")

checks = {
    "prototype version is 2.52": "SYNTRA Social Prototype 2.52" in source and '<span class="meta">2.52</span>' in source,
    "auto sync checks notifications and bookmarks": "notificationsResult=await loadCloudNotifications(syncUserId,true)" in auto_sync and "bookmarksResult=await loadCloudBookmarks(syncUserId,true)" in auto_sync,
    "auto sync includes own posts and public feed in success criteria": "publicResult&&notificationsResult&&bookmarksResult&&ownPostsResult" in auto_sync,
    "auto sync rejects results after account changes": "syntraCloudUser?.id!==syncUserId" in auto_sync,
    "forced feed sync bypasses debounce": "async function syncPublicFeed(silent=true,force=false)" in feed_sync and "if(!force&&Date.now()-publicFeedLastSyncAt<30000)return false" in feed_sync,
    "session bootstrap checks every required data set": all(token in session_sync for token in ["ownSync=await syncCloudPosts(true)", "notificationSync=await loadCloudNotifications(sessionUserId,true)", "publicSync=await syncPublicFeed(true,true)", "bookmarkSync=await loadCloudBookmarks(sessionUserId,true)"]),
    "session bootstrap schedules recovery on partial failure": "else{markCloudRecoveryPending(sessionUserId);scheduleCloudRecoveryRetry()}" in session_sync,
    "recovery retry forces a public-feed refresh": "syncPublicFeed(true,true)" in retry_sync,
    "normal feed cooldown remains available": "if(!force&&Date.now()-publicFeedLastSyncAt<30000)return false" in feed_sync,
    "no offline write queue or replay was added": "No offline post publishing queue" in readme and "automatic post replay" in readme,
    "existing recovery uses account-scoped bounded backoff": "cloudRecoveryState.userId!==syntraCloudUser.id" in source and "Math.min(5*60*1000,15000*Math.pow(2,Math.min(attempts,5)))" in source,
}
failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Sync recovery checks failed: " + ", ".join(failed))
print("All SYNTRA Social sync-recovery checks passed.")
