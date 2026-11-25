#!/usr/bin/env python3
"""Static regression checks for SYNTRA Social 2.51 Cloud data consistency."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "index.html").read_text(encoding="utf-8")
start = source.index("async function inspectCloudDataConsistency()")
end = source.index("async function auditDataIntegrity()", start)
audit = source[start:end]

checks = {
    "prototype version is 2.51": "SYNTRA Social Prototype 2.51" in source and '<span class="meta">2.51</span>' in source,
    "manual integrity audit invokes the Cloud consistency engine": "const cloudConsistency=await inspectCloudDataConsistency()" in source,
    "Cloud audit requires a signed-in account and online state": "!syntraSupabaseClient||!syntraCloudUser" in audit and "navigator.onLine===false" in audit,
    "Cloud audit scopes the result to the active account": "const userId=syntraCloudUser.id" in audit and "syntraCloudUser.id!==userId" in audit,
    "Cloud audit queries bounded groups of post IDs": "offset+=40" in audit and "postIds.slice(offset,offset+40)" in audit,
    "Cloud audit reads posts, media, comments, and likes": all(token in audit for token in [
        "from('posts').select('id,author_id,visibility,status,updated_at')",
        "from('post_media').select('id,post_id,owner_id,storage_path,mime_type,byte_size')",
        "from('comments').select('id,post_id,author_id')",
        "from('likes').select('post_id,user_id')",
    ]),
    "Cloud audit checks ownership and media references": all(token in audit for token in [
        "postAuthorMismatches", "mediaOwnerMismatches",
        "missingRemoteMediaMetadata", "remoteMediaNotLinkedLocally",
    ]),
    "Cloud audit checks comment and like relationships": all(token in audit for token in [
        "duplicateRemoteCommentIds", "commentsWithoutVisibleParent",
        "duplicateRemoteLikePairs", "likesWithoutVisibleParent",
    ]),
    "Cloud audit detects possible comment query truncation": "commentQueryMayBeTruncated" in audit and "length===1000" in audit,
    "Cloud audit does not mutate database or local post data": all(token not in audit for token in [
        ".insert(", ".update(", ".delete(", "save(", "localStorage.setItem",
    ]),
    "account changes invalidate the in-flight result": audit.count("syntraCloudUser.id!==userId") >= 2,
    "missing posts are not labelled as deleted": "notVisiblePostIds" in audit and "notVisiblePostIds.push(id)" in audit,
    "integrity report version 3 includes Cloud findings": "reportVersion:3" in source and "cloudConsistency}" in source,
    "settings describes the Cloud checks as read-only": "Data Consistency Engine" in source and "Chỉ đọc, không tự sửa hoặc xóa dữ liệu" in source,
}
failed = [name for name, passed in checks.items() if not passed]
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Data consistency checks failed: " + ", ".join(failed))
print("All SYNTRA Social data-consistency checks passed.")
