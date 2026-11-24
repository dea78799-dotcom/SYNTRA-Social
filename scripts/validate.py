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
    "settings version reflects prototype 2.30": "SYNTRA Social Prototype 2.30" in source and '<span class="meta">2.30</span>' in source,
    "own profile includes account-owned cloud posts": "posts.filter(p=>(own&&p.cloud)||p.name===name)" in source,
    "profile screen is explicitly shown and feed hidden": "profilePage.classList.add('show')" in source and "feed.style.display='none'" in source,
    "creator post editor is rendered with safe escaped content": "data-creator-editor=" in source and 'maxlength="5000"' in source and "esc(p.text||" in source,
    "creator edit controls are wired": "data-edit-own-post" in source and "data-save-own-post" in source and "data-cancel-own-post" in source,
    "cloud post edits update Supabase under current owner": "from('posts').update({body:nextText}).eq('id',post.id).eq('author_id',syntraCloudUser.id)" in source,
    "local post edits save to local storage": "post.text=nextText;" in source and "const saved=save();" in source,
    "cloud edit result is verified before local update": "if(!data)throw new Error('Không tìm thấy bài viết hoặc bạn không có quyền chỉnh sửa.')" in source,
    "settings badge reflects prototype 2.30": '<span class="meta">2.30</span>' in source,
    "settings icon has scoped optical alignment": '#desktopNav button[data-filter="settings"] .s-icon' in source and '#bottomNav button[data-filter="settings"] .s-icon' in source and "top:-1px" in source,

    "cloud avatar controls are disabled and cleared when signed out": "if(avatarFile)avatarFile.disabled=true;if(saveAvatar)saveAvatar.disabled=true;if(removeAvatar)removeAvatar.disabled=true;" in source and "cloudCurrentAvatarPath=null;releaseCloudAvatarPreview();setCloudAvatarPreview('','SYNTRA');" in source,
    "cloud avatar editor and file constraints are present": 'id="cloudAvatarFile"' in source and 'accept="image/jpeg,image/png,image/webp"' in source and 'id="saveCloudAvatar"' in source and 'id="removeCloudAvatar"' in source,
    "cloud avatar uses private storage bucket and cached download": "storage.from('syntra-avatars').download(path)" in source and "storage.from('syntra-avatars').upload(newPath,file" in source,
    "cloud avatar enforces image MIME and 2 MB client limit": "file.size>2*1024*1024" in source and "image/jpeg','image/png','image/webp" in source,
    "cloud avatar upload is scoped to authenticated user folder": "const newPath=userId+'/'+randomId+'.'+extension" in source and "upsert:false" in source,
    "cloud avatar update verifies profile row before accepting upload": "update({avatar_path:newPath,updated_at:new Date().toISOString()}).eq('id',userId).select('id,avatar_path').maybeSingle()" in source and "if(error||!data)" in source,
    "cloud avatar remove clears profile pointer before deleting own object": "update({avatar_path:null,updated_at:new Date().toISOString()}).eq('id',userId).select('id,avatar_path').maybeSingle()" in source and "storage.from('syntra-avatars').remove([oldPath])" in source,
    "profile settings load includes avatar path": "select('id,username,display_name,bio,is_private,is_discoverable,avatar_path').eq('id',userId)" in source,
    "public profile reads avatar path only for public profiles and displays image": "select('bio,avatar_path')" in source and "avatarUrl?'<img src=\"" in source,
    "avatar URLs use private object downloads": "URL.createObjectURL(data)" in source and "syntra-avatars" in source,
    "avatar controls are wired from settings": "settingsPage.querySelector('#saveCloudAvatar').onclick=saveCloudAvatar" in source and "settingsPage.querySelector('#removeCloudAvatar').onclick=removeCloudAvatar" in source,
    "cloud profile editor is present": 'id="cloudProfileDisplayName"' in source and 'id="cloudProfileUsername"' in source and 'id="cloudProfileVisibility"' in source,
    "cloud profile loads only the signed-in account's permitted columns": "from('profiles').select('id,username,display_name,bio,is_private,is_discoverable,avatar_path').eq('id',userId).maybeSingle()" in source,
    "cloud profile update is scoped to current account and verifies returned row": "from('profiles').update(updates).eq('id',userId).select('id,username,display_name,bio,is_private,is_discoverable').maybeSingle()" in source and "if(!data)throw new Error('Không tìm thấy hồ sơ hoặc tài khoản không có quyền cập nhật.')" in source,
    "cloud profile validates username and handles uniqueness": "/^[a-z0-9_]{3,30}$/.test(username)" in source and "error.code==='23505'" in source,
    "cloud profile privacy keeps private accounts undiscoverable": "is_private:visibility==='private',is_discoverable:visibility==='public'" in source,
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
    "public posts render shared like and comment controls": "data-like=\"'+esc(p.id)+'\"" in source and "loadCloudPostInteractions" in source,
    "public feed syncs when home feed renders": "if(active==='all')syncPublicFeed(true)" in source,
    "public feed loads for signed-out visitors after cloud initialization": "await syncPublicFeed(true);" in source and "if(!syntraCloudUser)render();" in source,
    "public member profile route is implemented": "async function renderPublicProfile(authorId)" in source,
    "public profile handles RLS-hidden private accounts without fetching private content": "if(!profile)" in source and "if(!privateProfile)" in source and "const knownPost=posts.find(post=>post.authorId===id&&post.publicCloud)" in source,
    "public profile queries only published public posts for author": ".eq('author_id',id).eq('visibility','public').eq('status','published')" in source,
    "public profile fetch uses only permitted profile columns": ".from('profiles').select('id,username,display_name,bio,is_private,is_discoverable,avatar_path')" in source,
    "public profile links are wired from cloud post author": "data-public-profile" in source and "renderPublicProfile(publicProfileBtn.dataset.publicProfile)" in source,
    "public profile renders escaped bio only for public profiles": "if(!privateProfile)" in source and "esc(bio)" in source,
    "cloud bio editor enforces 160 characters and updates live counter": 'id="cloudProfileBio" maxlength="160"' in source and "value.length+'/160 ký tự'" in source,
    "cloud bio is loaded and saved for the signed-in account": "bioInput.value=data.bio||''" in source and "const updates={username,display_name:displayName,bio," in source,
    "cloud bio field is loaded with explicit column selection": "select('id,username,display_name,bio,is_private,is_discoverable,avatar_path')" in source,
    "public profile navigation has a return action": "id=\"publicProfileBack\"" in source,
    "public profile styling exists": ".public-profile{" in source,
    "cloud interactions load likes and comments from Supabase": "async function loadCloudPostInteractions(postRows,userId=null)" in source and "from('likes').select('post_id,user_id')" in source and "from('comments').select('id,post_id,author_id,body,created_at')" in source,
    "public feed hydrates shared interaction counts and signed-in like state": "const interactions=await loadCloudPostInteractions(rows,syncUserId)" in source and "likes:0,liked:false,comments:[]" in source,
    "private cloud posts are excluded from public interaction hydration": "const publicRows=rows.filter(row=>row.visibility==='public')" in source and "loadCloudPostInteractions(publicRows,userId)" in source,
    "public profile hydrates post interactions": "loadCloudPostInteractions(rows,syntraCloudUser?.id||null)" in source,
    "cloud likes require login and persist to Supabase": "Đăng nhập SYNTRA Cloud để thích bài viết" in source and "from('likes').insert({post_id:p.id,user_id:userId})" in source and "from('likes').delete().eq('post_id',p.id).eq('user_id',userId)" in source,
    "cloud comments require login and persist to Supabase": "Đăng nhập SYNTRA Cloud để bình luận" in source and "from('comments').insert({post_id:p.id,author_id:userId,body:value})" in source,
    "local and demo interactions retain local behavior": "Đã thêm bình luận trên thiết bị." in source and "p.liked=!p.liked;p.likes+=p.liked?1:-1" in source,
    "public feed shows interaction controls for cloud posts": "Bài viết công khai · tương tác sẽ được bổ sung sau" not in source and "data-like=" in source,
    "signed-out public comments are disabled with clear guidance": "Đăng nhập để bình luận và đồng bộ trên các thiết bị." in source,
    "public feed survives account switches": "posts=posts.filter(post=>post.publicCloud||!post.cloud)" in source,
    "public feed status explains public interaction sync": "Bạn vẫn xem được bài viết, lượt thích và bình luận công khai" in source,
    "private multi-device sync is clearly explained": "Đăng nhập để tương tác và đồng bộ trên các thiết bị" in source,
    "hybrid cloud status copy is accurate": "Tài khoản và bài viết riêng tư dùng SYNTRA Cloud" in source and "Không có tài khoản thật, máy chủ, đồng bộ hay xác thực bảo mật." not in source,
    "cloud account UI is present": 'id="cloudSignUp"' in source and 'id="cloudSignIn"' in source,
    "cloud sync status shows active progress and last successful time": "Đang đồng bộ…" in source and "Đã đồng bộ lúc" in source and "cloudLastSyncAt" in source,
    "cloud sync clears old error status after a successful sync": "cloudAccountMessage='';updateCloudAccountUI();" in source,
    "manual sync button reflects loading and offline state": "syncButton.textContent=cloudSyncing?'Đang đồng bộ…':navigator.onLine===false?'Đang ngoại tuyến':'Đồng bộ ngay'" in source,
    "cloud sync prevents duplicate concurrent requests": "if(cloudSyncPromise&&cloudSyncUserId===userId)return cloudSyncPromise" in source,
    "cloud sync rejects stale account responses": "if(!syntraCloudUser||syntraCloudUser.id!==userId)return false" in source,
    "cloud sync refreshes when returning online or to tab": "window.addEventListener('focus',()=>{autoSyncCloudPosts()})" in source and "window.addEventListener('online',()=>{updateCloudAccountUI();autoSyncCloudPosts()})" in source and "document.addEventListener('visibilitychange'" in source,
    "cloud sync cleans old account media cache": "cloudMediaById.forEach((item,id)=>{mediaItems.delete(id);revokeMediaUrl(id)})" in source,
    "cloud sync rejects stale response after interaction hydration": "const interactions=await loadCloudPostInteractions(publicRows,userId);" in source and "if(!syntraCloudUser||syntraCloudUser.id!==userId)return false;" in source,
    "public feed rejects stale account response before replacing feed": "const syncUserId=syntraCloudUser?.id||null;" in source and "loadCloudPostInteractions(rows,syncUserId)" in source and "if((syntraCloudUser?.id||null)!==syncUserId)return false;" in source,
    "offline state is visible and disables manual sync": "Ngoại tuyến · " in source and "navigator.onLine===false" in source and "window.addEventListener('offline'" in source,
    "cloud diagnostics panel and manual action are present": 'id="cloudDiagnosticsStatus"' in source and 'id="cloudDiagnosticCheck"' in source and "onclick=checkCloudConnection" in source,
    "cloud diagnostic probe reads only public post IDs": "from('posts').select('id').eq('visibility','public').eq('status','published').limit(1)" in source,
    "cloud diagnostics classify network permission schema and server errors": "function classifyCloudError(error)" in source and "category:'network'" in source and "category:'permission'" in source and "category:'schema'" in source and "category:'server'" in source,
    "cloud diagnostics report latency and recent sync operation": "cloudDiagnostics.latencyMs=Date.now()-started" in source and "cloudDiagnostics.lastOperationAt=Date.now()" in source and "function renderCloudDiagnostics()" in source,
    "cloud sync diagnostics capture posts media interaction failures": "recordCloudDiagnostic('Tải bài viết',false,error)" in source and "recordCloudDiagnostic('Tải metadata ảnh/video',false,mediaResult.error)" in source and "recordCloudDiagnostic('Tải lượt thích/bình luận',false,error)" in source,
    "cloud sync diagnostics record successful completion": "recordCloudDiagnostic('Đồng bộ bài viết và media',true)" in source,
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
    "cloud follow relation loads from Supabase": "async function loadCloudFollowRelation" in source and "from('follows').select('follower_id,following_id,status,created_at,accepted_at')" in source,
    "public follows are accepted immediately and private follows create requests": "const status=isPrivate?'pending':'accepted'" in source and "payload.accepted_at=new Date().toISOString()" in source,
    "follow requests can be canceled or unfollowed": "from('follows').delete().eq('follower_id',userId).eq('following_id',targetId)" in source,
    "follow inbox loads follower and following counts": "id=\"cloudFollowContent\"" in source and "cloud-follow-stats" in source,
    "incoming follow requests can be accepted or rejected": "data-follow-accept" in source and "data-follow-reject" in source and "status:'accepted',accepted_at:new Date().toISOString()" in source,
    "private profiles reached from public posts show request UI without exposing profile data": "const knownPost=posts.find(post=>post.authorId===id&&post.publicCloud)" in source and "toggleCloudFollow(id,true)" in source and "Hồ sơ riêng tư" in source,
    "private profile visibility is not exposed in discovery": "is_private:visibility==='private',is_discoverable:visibility==='public'" in source and "profiles_select_discoverable_public" not in source,
    "follow controls require authentication and prevent self-follow": "Đăng nhập SYNTRA Cloud để theo dõi thành viên." in source and "targetId===syntraCloudUser.id" in source,
    "follow inbox is refreshed after loading own cloud profile": "await loadCloudFollowInbox(userId)" in source,
    "cloud following IDs sync and filter the following feed": "async function refreshCloudFollowingIds" in source and "cloudFollowingIds.has(p.authorId)" in source and "await refreshCloudFollowingIds(userId)" in source,
    "cloud notifications load only for the signed-in recipient": "async function loadCloudNotifications" in source and ".from('notifications').select('id,recipient_id,actor_id,notification_type,entity_type,entity_id,payload,read_at,created_at').eq('recipient_id',userId)" in source,
    "cloud notification actors are resolved through public profile data": "from('profiles').select('id,username,display_name').in('id',actorIds)" in source and "Thành viên SYNTRA" in source,
    "notification badge combines local and cloud unread counts": "notices.filter(x=>!x.read).length+cloudNotifications.filter(x=>!x.read).length" in source,
    "notification center renders Cloud events and existing local notices": "const items=[...cloudNotifications,...notices]" in source and "SYNTRA Cloud" in source,
    "read all updates only recipient-owned read_at fields": ".from('notifications').update({read_at:new Date().toISOString()}).eq('recipient_id',userId).is('read_at',null)" in source,
    "cloud notifications refresh on account change and app focus": "await loadCloudNotifications(syntraCloudUser.id,true)" in source and "await loadCloudNotifications(syntraCloudUser.id,true)" in source,
    "notification writes are handled by database triggers, not client inserts": "from('notifications').insert" not in source and "async function loadCloudNotifications" in source,
    "cloud search queries only public discoverable profiles": "async function searchCloudContent" in source and ".eq('is_private',false).eq('is_discoverable',true)" in source,
    "cloud search queries published public posts only": ".eq('visibility','public').eq('status','published').ilike('body',pattern)" in source,
    "cloud search limits result counts and sanitizes wildcard input": "function sanitizeCloudSearchTerm" in source and ".slice(0,60)" in source and ".limit(12)" in source and ".limit(8)" in source,
    "cloud search ignores stale responses": "requestId!==cloudSearchRequest" in source and "function scheduleCloudSearch" in source,
    "cloud search escapes profile and post content": "esc(member.display_name||member.username" in source and "esc(post.text)" in source,
    "cloud search result actions open public profiles and posts": "data-cloud-search-profile" in source and "data-cloud-search-post" in source and "openPostDetail(button.dataset.cloudSearchPost)" in source,
    "cloud bookmarks are loaded only for the signed-in user": "from('post_bookmarks').select('post_id,created_at').eq('user_id',userId)" in source and "function loadCloudBookmarks" in source,
    "cloud bookmarks load only published public posts": "in('id',ids).eq('visibility','public').eq('status','published')" in source,
    "cloud bookmarks restore saved state across sessions": "post.saved=savedIds.has(post.id)" in source and "await loadCloudBookmarks(syntraCloudUser.id,true)" in source,
    "cloud bookmark writes are scoped to the current user": "from('post_bookmarks').delete().eq('user_id',userId).eq('post_id',p.id)" in source and "from('post_bookmarks').insert({user_id:userId,post_id:p.id})" in source,
    "cloud bookmarks require sign-in and ignore stale account responses": "Đăng nhập SYNTRA Cloud để lưu bài viết giữa các thiết bị." in source and "syntraCloudUser.id!==userId" in source,
    "cloud bookmarks preserve prior saved state if refresh fails": source.index("posts.forEach(post=>{if(post.cloud&&post.publicCloud)post.saved=savedIds.has(post.id)})") > source.index("const interactions=await loadCloudPostInteractions(postRows,userId)"),

    "post detail remembers the previous screen": "let postDetailReturnView='all'" in source and "postDetailReturnView=active;activePostId=id" in source and "active=postDetailReturnView||'all'" in source,
    "post detail back action has neutral label": 'id="detailBack">← Quay lại</button>' in source,
    "settings version reflects prototype 2.30": "SYNTRA Social Prototype 2.30" in source and '<span class="meta">2.30</span>' in source,
}
failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Validation failed: " + ", ".join(failed))
print("All SYNTRA Social static checks passed.")

