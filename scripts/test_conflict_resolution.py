#!/usr/bin/env python3
"""Static regression checks for SYNTRA Social 2.55 conflict recovery post editing."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
source = INDEX.read_text(encoding="utf-8")

checks = {
    "prototype version reflects 2.55": "SYNTRA Social Prototype 2.55" in source and '<span class="meta">2.55</span>' in source,
    "Cloud post edit fetches the latest server version before writing": "select('id,body,updated_at')" in source,
    "preflight read is restricted to the current post and authenticated owner": ".eq('id',post.id).eq('author_id',syntraCloudUser.id).maybeSingle()" in source,
    "stale editor content is rejected before update": "if(current.body!==oldText)throw new Error(" in source,
    "Cloud update uses compare-and-swap on the exact updated_at token": ".eq('updated_at',current.updated_at).select('id,body,updated_at').maybeSingle()" in source,
    "empty conditional update result is handled as a concurrent conflict": "if(!data)throw new Error('Bài viết vừa thay đổi trên thiết bị khác." in source,
    "local-only post editing path remains available": "const saved=save();" in source and "if(post.cloud){" in source,
    "Cloud edit remains scoped to the signed-in author": ".eq('author_id',editUserId)" in source,
    "conflict recovery preserves the exact editor draft": "const draft=field.value" in source and "field.value=draft" in source,
    "latest Cloud version is displayed with escaped text": "Xem nội dung mới nhất trên Cloud" in source and "esc(String(currentRow.body||''))" in source,
    "draft rebasing requires an explicit user click": "data-accept-cloud-version" in source and "post.text=String(currentRow.body||'')" in source,
    "draft is not written automatically after conflict": "showCloudPostConflictRecovery(post,editor,field,editUserId,current);return" in source,
    "compare-and-swap is retained after draft rebasing": ".eq('updated_at',current.updated_at).select('id,body,updated_at').maybeSingle()" in source,
    "conflict recovery checks the active account": "syntraCloudUser?.id!==editUserId" in source and "syntraCloudUser?.id!==userId" in source,
}
failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Conflict-resolution checks failed: " + ", ".join(failed))
print("All SYNTRA Social conflict-resolution checks passed.")
