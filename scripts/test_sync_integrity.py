#!/usr/bin/env python3
"""Static regression tests for SYNTRA Social 2.55 Sync Integrity Monitor."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "index.html").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
validator = (ROOT / "scripts/validate.py").read_text(encoding="utf-8")

checks = {
    "prototype version is 2.56": "SYNTRA Social Prototype 2.56" in source and '<span class="meta">2.56</span>' in source,
    "monitor is visible in existing sync center": 'id="cloudSyncIntegrity"' in source and "renderCloudSyncIntegrity()" in source,
    "monitor covers six diagnostic categories": all("key:'" + key + "'" in source for key in ["posts", "media", "notifications", "bookmarks", "interactions", "connection"]),
    "monitor is scoped to active account": "cloudSyncIntegrity.userId!==userId" in source and "cloudSyncIntegrity=createCloudSyncIntegrityState(nextId)" in source,
    "account changes reset monitor state": "cloudSyncIntegrity=createCloudSyncIntegrityState(nextId)" in source,
    "diagnostics update per-category state": "recordCloudSyncIntegrity(category,ok,result.detail)" in source and "item.at=Date.now();item.ok=!!ok" in source,
    "old results are marked stale after 65 minutes": "CLOUD_SYNC_INTEGRITY_MAX_AGE=65*60*1000" in source and "now-item.at>CLOUD_SYNC_INTEGRITY_MAX_AGE" in source,
    "unknown datasets are not treated as healthy": "Chưa xác nhận" in source and "item.ok!==null" in source,
    "overall success requires four core groups": "const required=['posts','media','notifications','bookmarks']" in source and "allKnown&&states.every(item=>item.ok===true)" in source,
    "recovery pending prevents healthy summary": "recoveryPending||hasFailure" in source,
    "monitor adds no polling loop": "setInterval(" not in source[source.index("function createCloudSyncIntegrityState"):source.index("function getCloudAvatarUrl")],
    "monitor adds no persistence": "localStorage.setItem" not in source[source.index("function createCloudSyncIntegrityState"):source.index("function getCloudAvatarUrl")],
    "README retains the original 2.54 monitor release note": "Prototype 2.54 — Sync Integrity Monitor" in readme,
    "validator includes monitor checks": "Sync Integrity Monitor is account-scoped" in validator,
}
failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Sync integrity checks failed: " + ", ".join(failed))
print("All SYNTRA Social 2.56 integrity-monitor checks passed.")
