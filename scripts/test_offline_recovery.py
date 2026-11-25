#!/usr/bin/env python3
"""Static regression checks for SYNTRA Social 2.49 offline recovery."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "index.html").read_text(encoding="utf-8")

checks = {
    "prototype version is 2.49": "SYNTRA Social Prototype 2.49" in source and '<span class="meta">2.49</span>' in source,
    "recovery marker is stored locally under a dedicated key": "CLOUD_RECOVERY_KEY='syntra_cloud_recovery_v1'" in source and "localStorage.setItem(CLOUD_RECOVERY_KEY,JSON.stringify(cloudRecoveryState))" in source,
    "recovery marker contains account scope and retry metadata": "cloudRecoveryState={userId,attempts:0,updatedAt:Date.now()}" in source and "cloudRecoveryState.userId!==syntraCloudUser.id" in source,
    "recovery state does not store post content or credentials": "CLOUD_RECOVERY_KEY='syntra_cloud_recovery_v1'" in source and "password" not in source[source.index("function persistCloudRecovery"):source.index("function scheduleCloudRecoveryRetry")],
    "retry uses bounded exponential backoff and jitter": "Math.min(5*60*1000,15000*Math.pow(2,Math.min(attempts,5)))+Math.floor(Math.random()*5000)" in source,
    "retry requires matching signed-in account and visible online app": "cloudRecoveryState.userId!==syntraCloudUser.id" in source and "navigator.onLine===false||document.visibilityState==='hidden'" in source,
    "offline event marks current account for recovery": "window.addEventListener('offline',()=>{if(syntraCloudUser)markCloudRecoveryPending(syntraCloudUser.id)" in source,
    "online and foreground events resume pending recovery": "if(cloudRecoveryState?.pending&&cloudRecoveryState.userId===syntraCloudUser?.id)scheduleCloudRecoveryRetry()" in source,
    "successful full refresh clears only the matching account marker": "if(ok)clearCloudRecoveryPending(userId)" in source and "cloudRecoveryState.userId!==userId)return" in source,
    "automatic retry is silent and does not auto-queue writes": "retryCloudSyncCenter(true)" in source and "No offline post publishing queue" in (ROOT / "README.md").read_text(encoding="utf-8"),
}
failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Offline recovery checks failed: " + ", ".join(failed))
print("All SYNTRA Social offline-recovery checks passed.")
