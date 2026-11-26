#!/usr/bin/env python3
"""Static regression checks for SYNTRA Social 2.56 background sync queue."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "index.html").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")

start = source.index("const CLOUD_SYNC_QUEUE_LIMIT=6;")
end = source.index("let cloudSyncCenterRunning=false;", start)
queue = source[start:end]

checks = {
    "queue capacity is bounded to six jobs": "const CLOUD_SYNC_QUEUE_LIMIT=6;" in queue and "CLOUD_SYNC_QUEUE_LIMIT" in queue,
    "queue exposes pending running succeeded failed and cancelled states": all(token in queue for token in ["status:'pending'", "job.status='running'", "'succeeded'", "'failed'", "'cancelled'"]),
    "queue exceptions schedule the existing account recovery": "markCloudRecoveryPending(job.userId);scheduleCloudRecoveryRetry()" in queue,
    "queue executes only one job at a time": "if(cloudSyncQueueRunning)return;" in queue and "while(cloudSyncQueuePending.length)" in queue,
    "duplicate jobs are coalesced by key account and generation": "job.key===key&&job.userId===(userId||null)&&job.generation===generation" in queue,
    "queue rejects new jobs when capacity is reached": "cloudSyncQueuePending.length+(cloudSyncQueueActive?1:0)>=CLOUD_SYNC_QUEUE_LIMIT" in queue,
    "queued jobs capture session generation and account": "generation===cloudSessionGeneration" in queue and "userId:userId||null,generation" in queue,
    "pending and active jobs are invalidated on account transition": "cancelPendingCloudSyncJobs();" in source and "cloudSyncQueueActive.cancelled=true" in queue,
    "automatic sync uses the background queue": "enqueueCloudSyncJob('automatic-refresh'" in source,
    "manual recovery uses the background queue": "enqueueCloudSyncJob('manual-recovery'" in source,
    "Realtime refresh uses the background queue": "enqueueCloudSyncJob('realtime-refresh'" in source,
    "automatic sync checks generation between awaited datasets": "expectedGeneration=cloudSessionGeneration" in source and "if(!isCurrent())return false;" in source[source.index("async function autoSyncCloudPosts"):source.index("async function setCloudSession")],
    "queue status is shown in Sync Center": 'id="cloudSyncQueueStatus"' in source and "renderCloudSyncQueueStatus()" in source,
    "queue metadata is in-memory and bounded": "cloudSyncQueueHistory=cloudSyncQueueHistory.slice(0,12)" in queue and "localStorage" not in queue,
    "queue itself performs no database writes": all(token not in queue for token in [".insert(", ".update(", ".delete("]),
    "queue overflow schedules existing account recovery": "if(!queued&&syntraCloudUser?.id===userId){markCloudRecoveryPending(userId);scheduleCloudRecoveryRetry()}" in source,
    "README documents read-only queue and no offline write replay": "Prototype 2.56 — Background Sync Queue" in readme and "does not accept publishing, editing, deleting" in readme,
    "CI runs this regression suite": "python scripts/test_background_sync_queue.py" in workflow,
}
failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Background sync queue checks failed: " + ", ".join(failed))
print("All SYNTRA Social background-sync-queue checks passed.")
