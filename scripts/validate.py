from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile

HTML = Path("index.html")
source = HTML.read_text(encoding="utf-8")
CLOUD_CLIENT = Path("supabase-client.js")
cloud_source = CLOUD_CLIENT.read_text(encoding="utf-8") if CLOUD_CLIENT.exists() else ""

class InlineScripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.capture = False
        self.parts = []
        self.current = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "script":
            attrs = dict(attrs)
            self.capture = not attrs.get("src")
            self.current = []

    def handle_data(self, data):
        if self.capture:
            self.current.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "script" and self.capture:
            self.parts.append("".join(self.current))
            self.capture = False
            self.current = []

parser = InlineScripts()
parser.feed(source)
if not parser.parts:
    raise SystemExit("FAIL: no inline JavaScript found")

for index, js in enumerate(parser.parts, start=1):
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as file:
        file.write(js)
        path = file.name
    result = subprocess.run(["node", "--check", path], text=True, capture_output=True)
    Path(path).unlink(missing_ok=True)
    if result.returncode:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(f"FAIL: inline script {index} has a syntax error")
    print(f"PASS: inline JavaScript {index} syntax")

if not CLOUD_CLIENT.exists():
    raise SystemExit("FAIL: supabase-client.js is missing")
with tempfile.NamedTemporaryFile("w", suffix=".mjs", encoding="utf-8", delete=False) as file:
    file.write(cloud_source)
    cloud_path = file.name
cloud_result = subprocess.run(["node", "--check", cloud_path], text=True, capture_output=True)
Path(cloud_path).unlink(missing_ok=True)
if cloud_result.returncode:
    print(cloud_result.stdout)
    print(cloud_result.stderr)
    raise SystemExit("FAIL: Supabase module has a syntax error")
print("PASS: Supabase module syntax")

checks = {
    "local reset clears the posts key": "[KEY," in source and "BLOCKED_USERS_KEY].forEach(k=>localStorage.removeItem(k))" in source,
    "local reset clears the notices collection": "notices=[]" in source,
    "no stale POST_KEY reference": "POST_KEY" not in source,
    "no stale notifications variable": "notifications=[]" not in source,
    "no undefined updateAuthStatus call": "updateAuthStatus()" not in source,
    "mobile viewport is configured": "width=device-width" in source,
    "local-only data limitation is visible in README": "Core content remains local to the current browser" in Path("README.md").read_text(encoding="utf-8"),
    "full backup export is implemented": "async function exportFullBackup()" in source,
    "backup includes media blobs": "dataUrl:await blobToDataURL(item.blob)" in source,
    "restore validates backup version": "payload.backupVersion!==SYNTRA_BACKUP_VERSION" in source,
    "restore uses an IndexedDB transaction": "store.clear();records.forEach(item=>store.put(item))" in source,
    "restore restricts local storage keys": "const allowed=new Set(getBackupKeys())" in source,
    "backup restore controls are wired": "restoreFullBackup(file)" in source,
    "integrity audit is implemented": "async function auditDataIntegrity()" in source,
    "integrity audit checks duplicate post IDs": "duplicatePostIds" in source,
    "integrity audit detects missing media": "missingMediaIds" in source,
    "integrity audit detects orphan media": "orphanMediaIds" in source,
    "integrity audit checks malformed local JSON": "malformedLocalStorageKeys" in source,
    "integrity report export is wired": "exportIntegrityReport()" in source and 'id="exportIntegrityReport"' in source,
    "integrity audit does not auto-delete media": "Không tự sửa hoặc xóa dữ liệu" in source,
    "settings version reflects prototype 2.15": "SYNTRA Social Prototype 2.15" in source,
    "own profile includes account-owned cloud posts": "posts.filter(p=>(own&&p.cloud)||p.name===name)" in source,
    "creator post editor is rendered with safe escaped content": 'data-creator-editor="'+esc(p.id)+'"' in source and 'maxlength="5000">'+esc(p.text||'')+'</textarea>' in source,
    "creator edit controls are wired": "data-edit-own-post" in source and "data-save-own-post" in source and "data-cancel-own-post" in source,
    "cloud post edits update Supabase under current owner": "from('posts').update({body:nextText}).eq('id',post.id).eq('author_id',syntraCloudUser.id)" in source,
    "local post edits save to local storage": "post.text=nextText;" in source and "const saved=save();" in source,
    "cloud edit result is verified before local update": "if(!data)throw new Error('Không tìm thấy bài viết hoặc bạn không có quyền chỉnh sửa.')" in source,
    "settings badge reflects prototype 2.15": '<span class="meta">2.15</span>' in source,
    "public feed is clearly deferred": "Bảng tin công khai và xem bài của người khác sẽ làm ở giai đoạn sau." in source,
    "private multi-device sync is clearly explained": "Đăng nhập cùng tài khoản trên các thiết bị để đồng bộ riêng tư." in source,
    "hybrid cloud status copy is accurate": "Tài khoản và bài viết riêng tư dùng SYNTRA Cloud" in source and "Không có tài khoản thật, máy chủ, đồng bộ hay xác thực bảo mật." not in source,
    "cloud account UI is present": 'id="cloudSignUp"' in source and 'id="cloudSignIn"' in source,
    "cloud sync status shows active progress and last successful time": "Đang đồng bộ…" in source and "Đã đồng bộ lúc" in source and "cloudLastSyncAt" in source,
    "cloud sync clears old error status after a successful sync": "cloudAccountMessage='';updateCloudAccountUI();" in source,
    "manual sync button reflects loading state": "syncButton.textContent=cloudSyncing?'Đang đồng bộ…':'Đồng bộ ngay'" in source,
    "cloud sync prevents duplicate concurrent requests": "if(cloudSyncPromise&&cloudSyncUserId===userId)return cloudSyncPromise" in source,
    "cloud sync rejects stale account responses": "if(!syntraCloudUser||syntraCloudUser.id!==userId)return false" in source,
    "cloud sync refreshes when returning online or to tab": "window.addEventListener('focus',()=>{autoSyncCloudPosts()})" in source and "window.addEventListener('online',()=>{autoSyncCloudPosts()})" in source and "document.addEventListener('visibilitychange'" in source,
    "cloud sync cleans old account media cache": "cloudMediaById.forEach((item,id)=>{mediaItems.delete(id);revokeMediaUrl(id)})" in source,
    "password visibility control is present and wired": 'id="cloudPasswordToggle"' in source and "function toggleCloudPassword()" in source,
    "password reset request uses Supabase Auth": "auth.resetPasswordForEmail(email)" in source and 'id="cloudResetPassword"' in source,
    "password reset control is wired": "handleCloudPasswordReset" in source and "cloudResetPassword').onclick=handleCloudPasswordReset" in source,
    "auth errors are translated to clear Vietnamese messages": "function cloudAuthErrorMessage(error,mode)" in source and "Email hoặc mật khẩu chưa chính xác." in source,
    "password tools are mobile-friendly": ".cloud-password-tools{display:flex;gap:8px;margin-top:7px}" in source,
    "cloud client bootstrap is referenced": 'type="module" src="./supabase-client.js"' in source,
    "Supabase client uses pinned version": "@supabase/supabase-js@2.119.2" in cloud_source,
    "only publishable key is configured": "sb_publishable_" in cloud_source and "service_role" not in cloud_source,
    "cloud sign up uses email auth": "auth.signUp({email,password" in source,
    "cloud sign in uses password auth": "auth.signInWithPassword({email,password})" in source,
    "cloud posts are fetched from server": "from('posts').select('id,author_id,body,visibility,status,created_at')" in source,
    "cloud posts are inserted on publish": "from('posts').insert({author_id:syntraCloudUser.id,body:textValue" in source,
    "posting requires cloud login": "Hãy đăng nhập trong Cài đặt để đăng bài đồng bộ" in source,
    "cloud posts are deleted remotely": "from('posts').delete().eq('id',p.id)" in source,
    "private storage bucket is configured": "syntra-post-media" in source and "SYNTRA_MEDIA_BUCKET='syntra-post-media'" in source,
    "media uploads use authenticated storage client": ".storage.from(SYNTRA_MEDIA_BUCKET).upload(path,item.file" in source,
    "media metadata is inserted": "from('post_media').insert(mediaRows)" in source,
    "cloud sync fetches media metadata": "from('post_media').select('id,post_id,owner_id,storage_path,media_type,mime_type,byte_size')" in source,
    "remote media is downloaded on demand": ".storage.from(SYNTRA_MEDIA_BUCKET).download(remote.storage_path)" in source,
    "cloud deletion removes media objects": ".storage.from(SYNTRA_MEDIA_BUCKET).remove(paths)" in source,
    "media size validation remains enabled": "const max=kind==='image'?4*1024*1024:12*1024*1024" in source and "total>20*1024*1024" in source,
    "old media sync limitation is removed": "Đồng bộ ảnh/video sẽ được bổ sung" not in source,
}
failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Validation failed: " + ", ".join(failed))
print("All SYNTRA Social static checks passed.")

