#!/usr/bin/env python3
"""Static regression checks for SYNTRA Social 2.52 Realtime multi-device sync."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQL_246 = ROOT / "supabase/migrations/20261125113155_syntra_social_246_realtime_posts_publication.sql"
SQL_247 = ROOT / "supabase/migrations/20261125113754_syntra_social_247_realtime_social_tables.sql"
INDEX = ROOT / "index.html"
sql_246 = SQL_246.read_text(encoding="utf-8").lower()
sql_247 = SQL_247.read_text(encoding="utf-8").lower()
source = INDEX.read_text(encoding="utf-8")

tables = ("posts", "post_media", "comments", "likes", "notifications", "post_bookmarks")
checks = {
    "2.46 migration enables posts publication": "alter publication supabase_realtime add table public.posts;" in sql_246,
    "2.52 migration adds RLS-protected social tables": all(f"public.{table}" in sql_247 for table in tables[1:]) and "alter publication supabase_realtime" in sql_247,
    "Realtime listens for inserts and updates on posts and media": all(f".on('postgres_changes',{{event:'{event}',schema:'public',table:'{table}'}}" in source for table in ("posts", "post_media") for event in ("INSERT", "UPDATE")),
    "Realtime listens for comment inserts and updates": all(f".on('postgres_changes',{{event:'{event}',schema:'public',table:'comments'}}" in source for event in ("INSERT", "UPDATE")),
    "Realtime listens for like inserts": ".on('postgres_changes',{event:'INSERT',schema:'public',table:'likes'}" in source,
    "Realtime listens for notification inserts and updates": all(f".on('postgres_changes',{{event:'{event}',schema:'public',table:'notifications'}}" in source for event in ("INSERT", "UPDATE")),
    "Realtime listens for bookmark inserts": ".on('postgres_changes',{event:'INSERT',schema:'public',table:'post_bookmarks'}" in source,
    "Realtime does not subscribe to unfiltered wildcard or DELETE events": "event:'*'" not in source and "event:'DELETE'" not in source,
    "Realtime events trigger a guarded re-fetch rather than direct local writes": "queueCloudRealtimeRefresh()" in source and "await autoSyncCloudPosts()" in source,
    "Realtime refresh invalidates both feed and own-post sync timestamps": "publicFeedLastSyncAt=0;cloudLastSyncAt=0;" in source,
    "Realtime refresh waits for in-flight queries before fetching again": "activeOwnSync" in source and "activePublicSync" in source,
    "Realtime refresh is debounced": "setTimeout(()=>{cloudRealtimeRefreshTimer=null;flushCloudRealtimeRefresh()},650)" in source,
    "Realtime subscriptions are replaced on account change and cleaned up": "stopCloudRealtimeSync()" in source and "removeChannel(channel)" in source and "startCloudRealtimeSync(syntraCloudUser.id)" in source,
    "Realtime errors retain scheduled sync fallback": "cloudRealtimeStatus='fallback'" in source and "scheduleCloudAutoSync()" in source,
    "Realtime pending changes resume after app returns online or foreground": "cloudRealtimeRefreshPending" in source and "queueCloudRealtimeRefresh()" in source,
    "Realtime status is exposed in existing sync status text": "Đồng bộ trực tiếp đang kết nối" in source and "Realtime tạm gián đoạn" in source,
    "prototype version reflects 2.52": "SYNTRA Social Prototype 2.52" in source and '<span class="meta">2.52</span>' in source,
}

failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Realtime sync checks failed: " + ", ".join(failed))
print("All SYNTRA Social Realtime sync checks passed.")
