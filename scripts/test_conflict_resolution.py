#!/usr/bin/env python3
"""Static regression checks for SYNTRA Social 2.53 conflict-safe post editing."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
source = INDEX.read_text(encoding="utf-8")

checks = {
    "prototype version reflects 2.53": "SYNTRA Social Prototype 2.53" in source and '<span class="meta">2.53</span>' in source,
    "Cloud post edit fetches the latest server version before writing": "select('id,body,updated_at')" in source,
    "preflight read is restricted to the current post and authenticated owner": ".eq('id',post.id).eq('author_id',syntraCloudUser.id).maybeSingle()" in source,
    "stale editor content is rejected before update": "if(current.body!==oldText)throw new Error(" in source,
    "Cloud update uses compare-and-swap on the exact updated_at token": ".eq('updated_at',current.updated_at).select('id,body,updated_at').maybeSingle()" in source,
    "empty conditional update result is handled as a concurrent conflict": "if(!data)throw new Error('Bài viết vừa thay đổi trên thiết bị khác." in source,
    "local-only post editing path remains available": "const saved=save();" in source and "if(post.cloud){" in source,
    "Cloud edit remains scoped to the signed-in author": ".eq('author_id',syntraCloudUser.id)" in source,
}
failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Conflict-resolution checks failed: " + ", ".join(failed))
print("All SYNTRA Social conflict-resolution checks passed.")
