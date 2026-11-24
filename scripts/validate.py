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
    "settings version reflects prototype 2.9": "SYNTRA Social Prototype 2.9" in source,
    "cloud account UI is present": "id=\'cloudSignUp\'" in source and "id=\'cloudSignIn\'" in source,
    "cloud client bootstrap is referenced": 'type="module" src="./supabase-client.js"' in source,
    "Supabase client uses pinned version": "@supabase/supabase-js@2.119.2" in cloud_source,
    "only publishable key is configured": "sb_publishable_" in cloud_source and "service_role" not in cloud_source,
    "cloud sign up uses email auth": "auth.signUp({email,password" in source,
    "cloud sign in uses password auth": "auth.signInWithPassword({email,password})" in source,
    "cloud posts are fetched from server": "from('posts').select('id,author_id,body,visibility,status,created_at')" in source,
    "cloud posts are inserted on publish": "from('posts').insert({author_id:syntraCloudUser.id,body:textValue" in source,
    "posting requires cloud login": "Hãy đăng nhập trong Cài đặt để đăng bài đồng bộ" in source,
    "cloud posts are deleted remotely": "from('posts').delete().eq('id',p.id)" in source,
    "media sync limitation is disclosed": "Đồng bộ ảnh/video sẽ được bổ sung" in source,
}
failed = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + name)
if failed:
    raise SystemExit("Validation failed: " + ", ".join(failed))
print("All SYNTRA Social static checks passed.")
