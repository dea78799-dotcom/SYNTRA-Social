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
    "settings version reflects prototype 2.22": "SYNTRA Social Prototype 2.22" in source,
    "own profile includes account-owned cloud posts": "posts.filter(p=>(own&&p.cloud)||p.name===name)" in source,
    "profile screen is explicitly shown and feed hidden": "profilePage.classList.add('show')" in source and "feed.style.display='none'" in source,
    "creator post editor is rendered with safe escaped content": "data-creator-editor=" in source and 'maxlength="5000"' in source and "esc(p.text||" in source,
    "creator edit controls are wired": "data-edit-own-post" in source and "data-save-own-post" in source and "data-cancel-own-post" in source,
    "cloud post edits update Supabase under current owner": "from('posts').update({body:nextText}).eq('id',post.id).eq('author_id',syntraCloudUser.id)" in source,
    "local post edits save to local storage": "post.text=nextText;" in source and "const saved=save();" in source,
    "cloud edit result is verified before local update": "if(!data)throw new Error('Không tìm thấy bài viết hoặc bạn không có quyền chỉnh sửa.')" in source,
    "settings badge reflects prototype 2.22": '<span class="meta">2.22</span>' in source,
    "settings icon has scoped optical alignment": '#desktopNav button[data-filter="settings"] .s-icon' in source and '#bottomNav button[data-filter="settings"] .s-icon' in source and "top:-1px" in source,

    "cloud avatar controls are disabled and cleared when signed out": "if(avatarFile)avatarFile.disabled=true;if(saveAvatar)saveAvatar.disabled=true;if(removeAvatar)removeAvatar.disabled=true;" in source and "cloudCurrentAvatarPath=null;releaseCloudAvatarPreview();setCloudAvatarPreview('','SYNTRA');" in source,
    "cloud avatar editor and file constraints are present": 'id="cloudAvatarFile"' in source and 'accept="image/jpeg,image/png,image/webp"' in source and 'id="saveCloudAvatar"' in source and 'id="removeCloudAvatar"' in source,
    "cloud avatar uses private storage bucket and cached download": "storage.from('syntra-avatars').download(path)" in source and "storage.from('syntra-avatars').upload(newPath,file" in source,
    "cloud avatar enforces image MIME and 2 MB client limit": "file.size>2*1024*1024" in source and "image/jpeg','image/png','image/webp" in source,
    "cloud avatar upload is scoped to authenticated user folder": "const newPath=userId+'/'+randomId+'.'+extension" in source and "upsert:false" in source,
    "cloud avatar update verifies profile row before accepting upload": "update({avatar_path:newPath,updated_at:new Date().toISOString()}).eq('id',userId).select('id,avatar_path').maybeSingle()" in source and "if(error||!data)" in source,
    "cloud avatar remove clears profile pointer before deleting own object": "update({avatar_path:null,updated_at:new Date().toISOString()}).eq('id',userId).select('id,avatar_path').maybeSingle()" in source and "storage.from('syntra-avatars').remove([oldPath])" in source,
    "profile settings load includes avatar path": "select('id,username,display_name,is_private,is_discoverable,avatar_path').eq('id',userId)" in source,
    "public profile reads permitted avatar path and displays image": "select('id,username,display_name,is_private,is_discoverable,avatar_path').eq('id',profileToken)" in source and "profile.avatar_path?await getCloudAvatarUrl(profile.avatar_path)" in source,
    "avatar URLs use private object downloads": "URL.createObjectURL(data)" in source and "syntra-avatars" in source,
    "avatar controls are wired from settings": "settingsPage.querySelector('#saveCloudAvatar').onclick=saveCloudAvatar" in source and "settingsPage.querySelector('#removeCloudAvatar').onclick=removeCloudAvatar" in source,
    "cloud profile editor is present": 'id="cloudProfileDisplayName"' in source and 'id="cloudProfileUsername"' in source and 'id="cloudProfileVisibility"' in source,
    "cloud profile loads only the signed-in account's permitted columns": "from('profiles').select('id,username,display_name,bio,is_private,is_discoverable,avatar_path').eq('id',userId).maybeSingle()" in source,
    "cloud profile update is scoped to current account and verifies returned row": "from('profiles').update(updates).eq('id',userId).select('id,username,display_name,bio,is_private,is_discoverable').maybeSingle()" in source and "if(!data)throw new Error('Không tìm thấy hồ sơ hoặc tài khoản không có quyền cập nhật.')" in source,
    "cloud profile validates username and handles uniqueness": "/^[a-z0-9_]{3,30}$/.test(username)" in source and "error.code==='23505'" in source,
    "cloud profile privacy maps to database visibility flags": "is_private:visibility==='private',is_discoverable:visibility==='public'" in source,
    "cloud profile controls are wired and reload after login": "saveCloudProfileSettings" in source and "loadCloudProfileSettings();" in source,
    "cloud profile refreshes public feed after save": "publicFeedLastSyncAt=0;" in source and "await syncPublicFeed(true);" in source,
    "public feed fetches published public posts only": ".eq('visibility','public').eq('status','published')" in source,
    "public feed loads only discoverable profiles": "is_private,is_discoverable" in source and ".from('profiles').select('id,username,display_name,is_private,is_discoverable')" in source,
    "public post author identity uses public profile data without leaking local account name": "profile?.display_name||profile?.username" in source and "||'Thành viên SYNTRA'" in source,
    "post composer defaults to private visibility": 'id="postVisibility"' in source and 'value="private" selected' in source,
    "public posts reject media attachments": "visibility==='public'&&selectedMedia.length" in source,
    "selected visibility is written to cloud post": "insert({author_id:syntraCloudUser.id,body:textValue,visibility,status:'published'})" in source,
    "public feed preserves private cloud posts during own sync": "post.publicCloud||!post.cloud" in source,
    "private cloud posts are hidden from public home feed": "active==='all'&&p.cloud&&!p.publicCloud" in source,
    "public posts do not imply local-only social interactions": "Bài viết công khai · tương tác sẽ được bổ sung sau" in source,
    "public feed syncs when home feed renders": "if(active==='all')syncPublicFeed(true)" in source,
    "public feed loads for signed-out visitors after cloud initialization": "await syncPublicFeed(true);" in source and "if(!syntraCloudUser)render();" in source,
    "public member profile route is implemented": "async function renderPublicProfile(authorId)" in source,
    "public profile loads only discoverable non-private account": "profile.is_private!==false||profile.is_discoverable!==true" in source,
    "public profile queries only published public posts for author": ".eq('author_id',profileToken).eq('visibility','public').eq('status','published')" in source,
    "public profile fetch uses only permitted profile columns": ".from('profiles').select('id,username,display_name,bio,is_private,is_discoverable,avatar_path')" in source,
    "public profile links are wired from cloud post author": "data-public-profile" in source and "renderPublicProfile(publicProfileBtn.dataset.publicProfile)" in source,
    "public profile renders escaped bio only after public visibility check": "profile.is_private!==false||profile.is_discoverable!==true" in source and "profile.bio?'<p class=\"public-profile-bio\">'+esc(profile.bio)" in source,
    "cloud bio editor enforces 160 characters and updates live counter": 'id="cloudProfileBio" maxlength="160"' in source and "value.length+'/160 ký tự'" in source,
    "cloud bio is loaded and saved for the signed-in account": "bioInput.value=data.bio||''" in source and "const updates={username,display_name:displayName,bio," in source,
    "cloud bio field is loaded with explicit column selection": "select('id,username,display_name,bio,is_private,is_discoverable,avatar_path')" in source,
    "public profile navigation has a return action": "id=\"publicProfileBack\"" in source,
    "public profile styling exists": ".public-profile{" in source,
    "public feed survives account switches": "posts=posts.filter(post=>post.publicCloud||!post.cloud)" in source,
    "public feed status is accurate": "Bảng tin công khai đã hỗ trợ bài viết văn bản" in source,
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

