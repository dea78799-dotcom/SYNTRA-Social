#!/usr/bin/env python3
"""Static regression checks for SYNTRA Social 2.46 Realtime post sync."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQL = ROOT / "supabase/migrations/20261125113155_syntra_social_246_realtime_posts_publication.sql"
INDEX = ROOT / "index.html"
sql = SQL.read_text(encoding="utf-8").lower()
source = INDEX.read_text(encoding="utf-8")

checks = {
    "migration adds only the posts table to the existing Realtime publication": "alter publication supabase_realtime add table public.posts;" in sql and "drop publication" not in sql,
    "Realtime listener subscribes only to public posts": ".on('postgres_changes',{event:'*',schema:'public',table:'posts'}" in source,
    "Realtime payloads trigger a guarded re-fetch rather than direct local writes": "queueCloudRealtimeRefresh()" in source and "await autoSyncCloudPosts()" in source,
    "Realtime refresh invalidates both feed and own-post sync timestamps": "publicFeedLastSyncAt=0;cloudLastSyncAt=0;" in source,
    "Realtime refresh waits for in-flight queries before fetching again": "activeOwnSync" in source and "activePublicSync" in source,
    "Realtime refresh is debounced": "setTimeout(()=>{cloudRealtimeRefreshTimer=null;flushCloudRealtimeRefresh()},650)" in source,
    "Realtime subscriptions are replaced on account change and cleaned up": "stopCloudRealtimeSync()" in source and "removeChannel(channel)" in source and "startCloudRealtimeSync(syntraCloudUser.id)" in source,
    "Realtime errors retain scheduled sync fallback": "cloudRealtimeStatus='fallback'" in source and "scheduleCloudAutoSync()" in source,
    "Realtime pending changes resume after app returns online or foreground": "cloudRealtimeRefreshPending" in source and "queueCloudRealtimeRefresh()" in source,
    "Realtime status is exposed in existing sync status text": "Đồng bộ trực tiếp đang kết nối" in source and "Realtime tạm gián đoạn" in source,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Realtime sync checks failed: " + ", ".join(failed))
print("All SYNTRA Social Realtime sync checks passed.")
