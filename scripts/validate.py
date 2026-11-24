from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile

HTML = Path("index.html")
source = HTML.read_text(encoding="utf-8")
CLOUD_CLIENT = Path("supabase-client.js")
PRIVACY_MIGRATION = Path("supabase/migrations/20261124120000_privacy_deletion_cancel_grant.sql")
REPORT_MIGRATION = Path("supabase/migrations/20261124130000_syntra_social_235_report_validation.sql")
OWNER_MIGRATION = Path("supabase/migrations/20261124140000_syntra_social_236_owner_moderation.sql")
OWNER_PRIVACY_MIGRATION = Path("supabase/migrations/20261124143000_syntra_social_2361_report_privacy_acl.sql")
report_migration_source = REPORT_MIGRATION.read_text(encoding="utf-8") if REPORT_MIGRATION.exists() else ""
owner_migration_source = OWNER_MIGRATION.read_text(encoding="utf-8") if OWNER_MIGRATION.exists() else ""
owner_privacy_migration_source = OWNER_PRIVACY_MIGRATION.read_text(encoding="utf-8") if OWNER_PRIVACY_MIGRATION.exists() else ""
privacy_migration_source = PRIVACY_MIGRATION.read_text(encoding="utf-8") if PRIVACY_MIGRATION.exists() else ""
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
    "named composer drafts use a separate versioned local collection with a 20-item cap": "NAMED_COMPOSER_DRAFTS_KEY='syntra_social_named_composer_drafts_v1'" in source and "MAX_NAMED_COMPOSER_DRAFTS=20" in source,
    "named composer drafts support save open rename and delete": "function saveNamedComposerDraft()" in source and "function loadNamedComposerDraft()" in source and "function renameNamedComposerDraft()" in source and "function deleteNamedComposerDraft()" in source,
    "named composer draft controls are wired and accessible": 'id="draftList"' in source and 'id="saveNamedDraft"' in source and 'id="loadNamedDraft"' in source and 'id="renameNamedDraft"' in source and 'id="deleteNamedDraft"' in source and 'aria-label="Quản lý nhiều bản nháp"' in source,
    "named composer drafts validate records and handle storage failures": "function readNamedComposerDrafts()" in source and "catch(error){console.warn('SYNTRA named draft save failed:'" in source and "toLocaleLowerCase()" in source,
    "named composer draft controls have responsive styling": ".composer-draft-manager-actions" in source and ".composer-draft-manager input" in source,
    "prototype version reflects 2.40": "SYNTRA Social Prototype 2.40" in source and "syntra-composer-draft-2-40" in source,
    "composer drafts autosave text and post options locally": "COMPOSER_DRAFT_KEY='syntra_social_composer_draft_v1'" in source and "localStorage.setItem(COMPOSER_DRAFT_KEY" in source and "getElementById('postText').addEventListener('input',saveComposerDraft)" in source and "getElementById('postType').addEventListener('change',saveComposerDraft)" in source and "getElementById('postVisibility').addEventListener('change',saveComposerDraft)" in source,
    "composer drafts restore when the composer opens": "function restoreComposerDraft()" in source and "restoreComposerDraft();syncComposerViewport()" in source,
    "composer drafts can be explicitly cleared and clear after successful publishing": "getElementById('clearDraft').addEventListener('click',()=>clearComposerDraft(true))" in source and "save();clearComposerDraft(true);close();filter('all')" in source,
    "composer draft UI explains local-only storage and media re-selection": 'id="draftStatus"' in source and "Bản nháp chỉ lưu văn bản và lựa chọn bài viết trên trình duyệt này." in source and "Ảnh/video cần chọn lại nếu bạn đóng trang." in source,
    "composer draft stylesheet is present and closed in document head": '<style id="syntra-composer-draft-2-39">' in source and source.find("</style>",source.find('<style id="syntra-composer-draft-2-39">')) < source.find("</head>"),
    "report migration validates authenticated ownership and public target": "new.reporter_id <> auth.uid()" in report_migration_source and "p.visibility = 'public'" in report_migration_source and "p.is_discoverable = true" in report_migration_source,
    "report migration enforces a daily submission limit": "recent_count >= 10" in report_migration_source and "interval '24 hours'" in report_migration_source,
    "report migration rejects self-reporting and locks status": "target_owner = new.reporter_id" in report_migration_source and "new.status := 'open'" in report_migration_source,
    "report trigger function is not executable directly by client roles": "revoke all on function public.validate_syntra_report() from public, anon, authenticated;" in report_migration_source,
    "cloud report dialog submits only supported report target types": "function openCloudReportDialog(targetType,targetId,targetLabel)" in source and "!['post','comment','profile'].includes(targetType)" in source,
    "cloud report dialog sends authenticated reports with bounded details": "from('reports').insert({reporter_id:userId,target_type:targetType,target_id:targetId,reason,details})" in source and 'maxlength="1000"' in source,
    "report history relies on reporter-only RLS without selecting reporter identity": "from('reports').select('id,target_type,target_id,reason,details,status,created_at').order('created_at'" in source and ".eq('reporter_id',userId)" not in source,
    "public post menu opens the cloud report dialog": "openCloudReportDialog('post',p.id,p.name)" in source,
    "public profile has a report action": 'id="cloudReportProfile"' in source and "openCloudReportDialog('profile',id,displayName)" in source,
    "cloud comments have report actions": "data-report-comment" in source and "openCloudReportDialog('comment',b.dataset.reportComment" in source,
    "report center is present in settings": 'id="cloudReportsList"' in source and "loadCloudReports();" in source,
    "privacy cancellation migration grants status only": "GRANT UPDATE (status) ON TABLE public.account_deletion_requests TO authenticated;" in privacy_migration_source and "GRANT UPDATE ON TABLE public.account_deletion_requests" not in privacy_migration_source,
    "local reset clears the posts key": "[KEY," in source and "BLOCKED_USERS_KEY].forEach(k=>localStorage.removeItem(k))" in source,
    "local reset clears the notices collection": "notices=[]" in source,
    "no stale POST_KEY reference": "POST_KEY" not in source,
    "no stale notifications variable": "notifications=[]" not in source,
    "no undefined updateAuthStatus call": "updateAuthStatus()" not in source,
    "mobile viewport is configured": "width=device-width" in source,
    "mobile bottom navigation has minimum 44px touch targets": ".bottomnav button{border:0;background:none;color:var(--muted);font-size:20px;padding:6px 10px;min-width:44px;min-height:44px;touch-action:manipulation}" in source,
    "composer dialog scrolls within short mobile viewports": ".dialog{width:min(520px,100%);max-height:calc(100dvh - 32px);overflow-y:auto;overscroll-behavior:contain" in source,
    "keyboard focus indicator is visible": ":focus-visible{outline:2px solid var(--accent2);outline-offset:3px}" in source,
    "mobile navigation and composer controls are present": 'class="bottomnav"' in source and 'id="bottomCreate"' in source and 'id="publish"' in source and 'id="cancel"' in source,
    "media viewer exposes dialog semantics and accessible controls": 'id="mediaViewer" role="dialog" aria-modal="true"' in source and 'id="viewerClose" aria-label="Đóng"' in source,
    "notification panel has an accessible label": 'id="noticePanel" aria-label="Trung tâm thông báo"' in source,
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
    "cloud sync center stores bounded local-only event history": "CLOUD_SYNC_HISTORY_KEY='syntra_cloud_sync_history_v1'" in source and "cloudSyncHistory=cloudSyncHistory.slice(0,20)" in source and "writeLocalJSON(CLOUD_SYNC_HISTORY_KEY,cloudSyncHistory)" in source,
    "cloud sync center renders recent events and retry control": 'id="cloudSyncHistory"' in source and 'id="cloudSyncCenterRetry"' in source and "async function retryCloudSyncCenter()" in source,
    "cloud sync center avoids storing account credentials or post content": "Không lưu nội dung bài viết hoặc thông tin đăng nhập." in source and "summary:ok?'Đồng bộ hoàn tất':result.detail" in source,
    "cloud auto sync uses a randomized 30 to 60 minute interval": "cloudAutoSyncDelay=30*60*1000+Math.floor(Math.random()*(30*60*1000+1))" in source,
    "cloud auto sync runs through existing guarded sync pipeline": "return await autoSyncCloudPosts()" in source,
    "cloud auto sync prevents overlapping runs": "if(cloudAutoSyncPromise)return cloudAutoSyncPromise" in source,
    "cloud auto sync pauses while hidden or offline": "document.visibilityState==='hidden'" in source and "navigator.onLine===false" in source,
    "cloud auto sync resumes on focus visibility and reconnect": "runCloudAutoSyncNow()" in source,
    "cloud auto sync reports next scheduled time in settings": 'id="cloudAutoSyncStatus"' in source,
    "security center shows email verification and database RLS baseline": 'id="cloudSecurityEmailState"' in source and 'RLS bật trên 11/11 bảng public' in source,
    "security center updates password through Supabase Auth": "auth.updateUser({password})" in source and "async function handleCloudSecurityUpdatePassword()" in source,
    "security center supports email confirmation resend": "auth.resend({type:'signup',email:syntraCloudUser.email})" in source,
    "security center can revoke other device refresh sessions": "auth.signOut({scope:'others'})" in source,
    "ordinary sign out only affects current device": "auth.signOut({scope:'local'})" in source,
    "security center controls are wired and account-aware": "renderCloudSecurityCenter()" in source and "cloudSecuritySignOutOthers" in source,
    "security center warns about leaked password protection": "Leaked Password Protection" in source,
    "settings version reflects prototype 2.36": "SYNTRA Social Prototype 2.36" in source and '<span class="meta">2.36</span>' in source,
    "Owner Console requires server-side Owner status and TOTP MFA": "rpc('syntra_owner_status')" in source and "auth.mfa.enroll({factorType:'totp'" in source and "auth.mfa.challenge({factorId})" in source and "auth.mfa.verify({factorId,challengeId:challenge.id,code})" in source,
    "Owner moderation queue does not select reporter identity": ".select('id,target_type,target_id,reason,details,status,created_at')" in source,
    "moderation actions use the protected server RPC": "rpc('syntra_moderate_report'" in source and "rpc('syntra_get_moderation_audit'" in source and "from('reports').update(" not in source,
    "Owner Console is wired into Settings and account changes": 'id="syntraOwnerConsole"' in source and "loadSyntraOwnerConsole();" in source,
    "Owner migration keeps role table private and blocks direct writes": "private.syntra_owner_roles" in owner_migration_source and "revoke all on table private.syntra_owner_roles from public, anon, authenticated;" in owner_migration_source,
    "Owner moderation requires AAL2 on the server": "auth.jwt()->>'aal','aal1') <> 'aal2'" in owner_migration_source and "reports_select_owner_aal2" in owner_migration_source,
    "moderation audit is private and records every status transition": "private.syntra_report_moderation_audit" in owner_migration_source and "insert into private.syntra_report_moderation_audit" in owner_migration_source,
    "reports cannot be updated directly by authenticated clients": "revoke update (id,reporter_id,target_type,target_id,reason,details,status,created_at)" in owner_migration_source,
    "reporter identity is not selectable by authenticated clients": "revoke select on table public.reports from authenticated;" in owner_privacy_migration_source and "grant select (id, target_type, target_id, reason, details, status, created_at)" in owner_privacy_migration_source,
    "cloud block records load across devices for the current account": "async function loadCloudBlocks" in source and "from('blocks').select('blocker_id,blocked_id,blocked_label,created_at')" in source,
    "cloud blocking stores stable account IDs and labels": "from('blocks').insert({blocker_id:userId,blocked_id:targetId,blocked_label:safeLabel})" in source,
    "cloud block list supports unblocking": "async function unblockCloudUser" in source and "data-cloud-unblock" in source,
    "public Cloud profiles can be blocked from profile view": "id=\"cloudBlockToggle\"" in source and "blockCloudUser(id,displayName)" in source,
    "blocked Cloud authors are filtered from cached feeds and post detail": "cloudBlockedUserIds.has(p.authorId)" in source and "cloudBlockedUserIds.has(p.authorId)" in source,
    "followers can be removed and blocked from account settings": "data-follow-remove" in source and "data-follow-block" in source,
    "cloud privacy center exports account data": "async function exportCloudAccountData" in source and "format:'syntra-social-cloud-export'" in source,
    "cloud export omits credentials and raw media binaries": "Không bao gồm mật khẩu, access token hoặc refresh token." in source and "Không bao gồm nội dung nhị phân của ảnh/video" in source,
    "account deletion requests are explicit and not automatic": "async function submitCloudDeletionRequest" in source and "tài khoản KHÔNG bị xóa ngay" in source,
    "account deletion requests can be cancelled while pending": "async function cancelCloudDeletionRequest" in source and "status','pending'" in source,
    "privacy center buttons are wired": "cloudExportData').onclick=exportCloudAccountData" in source and "cloudRequestDeletion').onclick=submitCloudDeletionRequest" in source,
    "privacy UI is mobile-responsive": ".cloud-privacy-row" in source and "@media(max-width:700px)" in source,
    "own profile includes account-owned cloud posts": "posts.filter(p=>(own&&p.cloud)||p.name===name)" in source,
    "profile screen is explicitly shown and feed hidden": "profilePage.classList.add('show')" in source and "feed.style.display='none'" in source,
    "creator post editor is rendered with safe escaped content": "data-creator-editor=" in source and 'maxlength="5000"' in source and "esc(p.text||" in source,
    "creator edit controls are wired": "data-edit-own-post" in source and "data-save-own-post" in source and "data-cancel-own-post" in source,
    "cloud post edits update Supabase under current owner": "from('posts').update({body:nextText}).eq('id',post.id).eq('author_id',syntraCloudUser.id)" in source,
    "local post edits save to local storage": "post.text=nextText;" in source and "const saved=save();" in source,
    "cloud edit result is verified before local update": "if(!data)throw new Error('Không tìm thấy bài viết hoặc bạn không có quyền chỉnh sửa.')" in source,
    "settings badge reflects prototype 2.36": '<span class="meta">2.36</span>' in source,
    "security center is present in Settings": 'id="securityCenter"' in source and 'id="securityAccountStatus"' in source,
    "security center reports verified email from Supabase Auth": "user.email_confirmed_at||user.confirmed_at" in source and 'id="securityEmailStatus"' in source,
    "unverified email can request a confirmation resend": "auth.resend({type:'signup',email:syntraCloudUser.email})" in source and "handleCloudResendVerification" in source,
    "password update uses Supabase Auth and validates confirmation": "auth.updateUser({password:nextPassword})" in source and "nextPassword!==confirmPassword" in source and "nextPassword.length<8" in source,
    "password fields are cleared after a successful update": "if(first)first.value='';if(second)second.value='';" in source,
    "other sessions can be revoked without signing out the current session": "auth.signOut({scope:'others'})" in source and "handleCloudSignOutOthers" in source,
    "security center renders the current browser session": "function renderSecurityCenter()" in source and "navigator.userAgent" in source,
    "security center refreshes when account state changes": "renderSecurityCenter();" in source and "function updateCloudAccountUI(message)" in source,
    "security center documents RLS review and leaked-password warning": "10/10 bảng trong public đã bật Row Level Security (RLS)" in source and "password-security#password-strength-and-leaked-password-protection" in source,
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
    "cloud sync deduplicates posts by stable database ID": "const syncedPostIds=new Set(cloudPosts.map(post=>post.id));" in source and "!syncedPostIds.has(post.id)" in source,
    "cloud sync preserves unrelated public cloud posts and local demo posts": "posts.filter(post=>!post.cloud||!syncedPostIds.has(post.id))" in source,
    "private cloud posts are visible only to their signed-in owner": "active==='all'&&p.cloud&&!p.publicCloud&&p.authorId!==syntraCloudUser?.id" in source,
    "private post media is resolved from authenticated cloud metadata": "const remote=cloudMediaById.get(id)" in source and "storage.from(SYNTRA_MEDIA_BUCKET).download(remote.storage_path)" in source,
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
    "cloud sync refreshes when returning online or to tab": "window.addEventListener('focus',()=>{if(document.visibilityState==='visible')runCloudAutoSyncNow()})" in source and "window.addEventListener('online',()=>{updateCloudAccountUI();runCloudAutoSyncNow()})" in source and "document.addEventListener('visibilitychange'" in source,
    "cloud sync cleans old account media cache": "cloudMediaById.forEach((item,id)=>{mediaItems.delete(id);revokeMediaUrl(id)})" in source,
    "cloud sync rejects stale response after interaction hydration": "let interactions;" in source and "loadCloudPostInteractions(publicRows,userId)" in source and "if(!syntraCloudUser||syntraCloudUser.id!==userId)return false;" in source,
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
    "cloud sync center stores bounded local-only event history": "CLOUD_SYNC_HISTORY_KEY='syntra_cloud_sync_history_v1'" in source and "cloudSyncHistory=cloudSyncHistory.slice(0,20)" in source and "writeLocalJSON(CLOUD_SYNC_HISTORY_KEY,cloudSyncHistory)" in source,
    "cloud sync center renders recent events and retry control": 'id="cloudSyncHistory"' in source and 'id="cloudSyncCenterRetry"' in source and "async function retryCloudSyncCenter()" in source,
    "cloud sync center avoids storing account credentials or post content": "Không lưu nội dung bài viết hoặc thông tin đăng nhập." in source and "summary:ok?'Đồng bộ hoàn tất':result.detail" in source,
}
failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Validation failed: " + ", ".join(failed))
print("All SYNTRA Social static checks passed.")



# Regression guard for the Cloud Search stylesheet wrapper.
if "<style id=\"syntra-cloud-search-2-26\">" not in source:
    raise SystemExit("FAIL: Cloud Search CSS style wrapper is missing")
cloud_style_start = source.index("<style id=\"syntra-cloud-search-2-26\">")
cloud_style_end = source.find("</style>", cloud_style_start)
cloud_style_html_end = source.find("</head>", cloud_style_start)
if cloud_style_end < 0 or (cloud_style_html_end >= 0 and cloud_style_end > cloud_style_html_end):
    raise SystemExit("FAIL: Cloud Search CSS is not closed before </head>")
