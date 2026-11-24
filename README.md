# SYNTRA Social

**A social platform for video, photos, posts, and communities.**

 > Status: **Prototype 2.10** — mobile-first prototype with Supabase email authentication, private text-post sync, and private cross-device image/video storage. This remains a limited prototype, not a public social network.

## Vision
SYNTRA Social is a social platform within the SYNTRA ecosystem, with a goal of bringing together:
- Short and long-form video
- Photo sharing
- Text posts and discussions
- Communities and groups
- Profiles and following

## Prototype 0.1
Mobile-first responsive front-end prototype.

### Included
- Responsive desktop/mobile layout
- Feed navigation and demo category filters
- Sample posts
- Search sample posts
- Create demo posts locally
- Like/unlike
- Save/unsave
- Demo share action
- Mobile bottom navigation

### Not implemented
- Real accounts or authentication
- Backend/database
- Upload or streaming media
- Server-side comments
- Follow graph
- Notifications
- Real moderation/reporting system

Demo posts created in this version are saved in browser local storage on the current device. They are not published or visible to other people. Core content remains local to the current browser. Image and video attachments are stored separately in IndexedDB on that device; they are not uploaded to a server.

## Roadmap
1. Responsive front-end prototype — in progress; local demo features are available.
2. Backend foundation — initial Supabase database and RLS deployed; real authentication/client integration pending.
3. Profiles and following — demo/local version implemented; server-side social graph pending.
4. Posts, comments, reactions and notifications — local demo implemented; real moderation/report/block tools pending.
5. Image/video attachments and multi-image albums — local preview plus private Supabase Storage sync implemented for the signed-in account.
6. Short-video feed, recommendations and streaming — pending.
7. Real communities and group membership — pending.
8. Security, privacy controls, accessibility and deployment testing — required before public launch.
9. Explore/discovery and search — local prototype implemented; real recommendations and server-side indexing pending.

## Backend preparation

- The backend architecture is documented in [docs/BACKEND-ARCHITECTURE.md](docs/BACKEND-ARCHITECTURE.md).
- The read-only Supabase schema/RLS review is recorded in [docs/BACKEND-AUDIT-1.9.md](docs/BACKEND-AUDIT-1.9.md).
- The authorization scenarios and acceptance criteria are documented in [docs/RLS-TEST-MATRIX-1.9B.md](docs/RLS-TEST-MATRIX-1.9B.md).
- Supabase project `SYNTRA-Social` is active in Singapore (`ap-southeast-1`). The existing PostgreSQL schema and RLS baseline are deployed. The static frontend now includes email authentication and a private media bucket restricted to each authenticated user's own storage folder. End-to-end device testing remains pending.
- Keep the public prototype local-only until authentication, RLS, private media policies, block/report controls and age-appropriate safeguards pass verification.

## Authentication setup

- Follow [docs/AUTH-SETUP.md](docs/AUTH-SETUP.md) to configure Email sign-in, confirmation and exact redirect URLs.
- The profile creation trigger is deployed on `auth.users`; it creates a `public.profiles` row for new accounts.
- Do not enable public registration or connect the public prototype to real user data until the Auth test matrix, RLS policies, media policies and moderation safeguards pass.

## Safety and privacy
Before public launch, SYNTRA Social must have privacy settings, moderation/report/block controls, secure authentication, age-appropriate safeguards, and clear community rules.

## Deployment
GitHub Pages can host the static prototype. A real social network will require a backend and media storage.

© SYNTRA — in development.


## Prototype 0.2 (latest)

- Chọn loại bài viết: bài thường, ảnh/video demo, cộng đồng.
- Bình luận demo được lưu trên trình duyệt thiết bị.
- Đổi tên hiển thị hồ sơ cục bộ; xem bài của mình.
- Xóa bài demo của chính mình bằng menu bài viết.
- Sửa điều kiện lọc để tab Đã lưu và loại nội dung hoạt động đúng.

**Giới hạn:** dữ liệu vẫn chỉ nằm trên thiết bị/browser hiện tại; tab Theo dõi chưa có hệ thống follow nên chưa hiển thị feed riêng; chưa có đăng nhập, máy chủ, tải media thực, hay kiểm duyệt/report thật. Không đăng thông tin cá nhân nhạy cảm trong prototype.


## Prototype 0.3

- Hồ sơ cá nhân có tên, bio, avatar và cover (lưu local trên trình duyệt).
- Mở trang demo người dùng bằng cách bấm tên hoặc avatar trên bài viết.
- Theo dõi/bỏ theo dõi hồ sơ demo; tab Theo dõi lọc bài từ hồ sơ đã theo dõi.
- Trang hồ sơ hiển thị bài viết của chủ hồ sơ.
- Giới hạn upload ảnh hồ sơ/cover 700 KB; dữ liệu vẫn local-only.
- Chưa có đăng nhập, đồng bộ cloud, follower thật hoặc server.


## Prototype 0.4 — Tin nhắn demo

- Thêm mục Tin nhắn trên thanh điều hướng máy tính và điện thoại.
- Hộp thư có danh sách các cuộc trò chuyện demo và tìm kiếm cuộc trò chuyện.
- Giao diện chat một-một với bong bóng tin nhắn, thời gian và ô gửi tin.
- Tin nhắn do người dùng gửi được lưu trong localStorage trên trình duyệt hiện tại.
- Giao diện thích ứng: máy tính hiển thị danh sách và hội thoại cùng lúc; điện thoại chuyển giữa danh sách và màn hình chat.
- Các liên hệ hiện tại là tài khoản mẫu; chưa có đăng nhập, đồng bộ giữa thiết bị, máy chủ hoặc realtime.

## Prototype 0.5 — Trung tâm thông báo demo

- Thêm bảng thông báo mở từ biểu tượng chuông trên thanh trên cùng.
- Hiển thị số thông báo chưa đọc; hỗ trợ đánh dấu tất cả là đã đọc và đóng bảng thông báo.
- Ghi nhận hoạt động cục bộ khi người dùng thích bài viết, bình luận, theo dõi hồ sơ hoặc gửi tin nhắn demo.
- Có một số thông báo mẫu được gắn nhãn “Mẫu mô phỏng” để minh họa lượt thích và người theo dõi.
- Thông báo lưu trong localStorage trên trình duyệt/thiết bị hiện tại; giới hạn tối đa 60 mục.

**Giới hạn:** đây chưa phải thông báo từ người dùng thật, không có push notification, realtime, máy chủ hay đồng bộ giữa các thiết bị. Các mục mô phỏng được đánh dấu rõ ràng; không đại diện cho tương tác thực tế.

## Prototype 0.6 — Đính kèm ảnh và video cục bộ

- Trong hộp thoại tạo bài viết, có thể chọn ảnh hoặc video từ bộ nhớ điện thoại/máy tính.
- Có xem trước ảnh/video trước khi đăng; có thể gỡ tệp đã chọn.
- Định dạng ảnh hỗ trợ: JPG, PNG, WEBP, GIF (tối đa 4 MB).
- Định dạng video hỗ trợ: MP4, WEBM (tối đa 12 MB); video phát bằng trình phát tích hợp, không tự phát.
- Tệp media được lưu trong IndexedDB; thông tin bài viết lưu trong localStorage. Khi tải lại trang, ứng dụng thử đọc lại tệp để hiển thị trong bài viết.
- Nếu trình duyệt không hỗ trợ IndexedDB, bộ nhớ hết dung lượng hoặc tệp không đọc được, ứng dụng sẽ báo lỗi/hiển thị thông báo thay vì giả vờ tải lên máy chủ.

**Giới hạn:** tệp chỉ nằm trên trình duyệt/thiết bị hiện tại, không được tải lên máy chủ và người khác không thể xem. Đây chưa phải hệ thống lưu trữ đám mây, xử lý video, quét tệp hoặc kiểm duyệt nội dung. Hãy chỉ chọn tệp bạn có quyền chia sẻ.


## Prototype 0.7 — Trình xem media và quản lý tệp

- Bấm ảnh trong bài viết để mở trình xem ảnh toàn màn hình.
- Có nút tải ảnh về thiết bị từ trình xem.
- Khi xóa bài viết của chính mình, ứng dụng cũng xóa tệp đính kèm trong IndexedDB và thu hồi URL media đang mở.
- Video vẫn dùng trình phát tích hợp với các điều khiển chuẩn.

**Giới hạn:** trình xem/tải chỉ làm việc với media đã lưu cục bộ trong trình duyệt; chưa có media server, liên kết công khai hoặc đồng bộ thiết bị.


## Prototype 0.8 — Album nhiều ảnh và trình xem ảnh

- Một bài viết có thể đính kèm tối đa **8 ảnh**. Hỗ trợ JPG, PNG, WEBP và GIF; tối đa 4 MB mỗi ảnh và 20 MB cho cả album.
- Hộp thoại tạo bài viết hiển thị bản xem trước dạng lưới và số lượng/dung lượng ảnh đã chọn. Video vẫn chọn riêng, tối đa 1 video mỗi bài, 12 MB.
- Bài viết hiển thị album dạng lưới. Khi có trên 4 ảnh, ô cuối hiển thị số ảnh còn lại; bấm vào bất kỳ ảnh nào để mở toàn bộ album.
- Trình xem ảnh toàn màn hình có nút ảnh trước/tiếp, bộ đếm vị trí, tải ảnh về thiết bị; trên điện thoại có thể vuốt trái/phải. Máy tính hỗ trợ phím mũi tên và Escape.
- Album cũng hiển thị trong trang hồ sơ. Bài viết cũ chỉ có một trường mediaId vẫn được đọc để giữ tương thích.
- Khi xóa bài viết của chính mình, ứng dụng xóa tất cả tệp thuộc album khỏi IndexedDB và thu hồi URL media đang dùng.

**Giới hạn:** đây vẫn là prototype cục bộ. Tệp ảnh/video được lưu trong IndexedDB của trình duyệt hiện tại; nội dung bài viết lưu trong localStorage. Tệp không được tải lên máy chủ, không tự đồng bộ sang điện thoại khác và người khác không thể xem. Giới hạn dung lượng thực tế còn phụ thuộc trình duyệt và bộ nhớ thiết bị. Không dùng prototype này để lưu trữ dữ liệu quan trọng.

## Trạng thái kiểm thử

- Đã kiểm tra cú pháp JavaScript bằng cách biên dịch script sau khi cập nhật.
- Đã đọc lại index.html và README.md từ GitHub để xác nhận nội dung đã lưu.
- Chưa thực hiện kiểm thử tương tác trực tiếp trên nhiều trình duyệt hoặc thiết bị Android. Cần kiểm tra thực tế việc chọn nhiều ảnh, tải ảnh và lưu trữ IndexedDB trước khi phát hành rộng rãi.
- GitHub Actions sẽ kiểm tra cú pháp JavaScript inline và các điều kiện an toàn cơ bản của luồng xóa dữ liệu demo.


## Prototype 1.0 — Thiết kế lại giao diện và Khám phá

### Thiết kế giao diện
- Chuyển logo trên thanh điều hướng sang wordmark chữ SYNTRA, không thêm biểu tượng thương hiệu mới.
- Đồng bộ bảng màu tối theo nhận diện SYNTRA: nền charcoal, bề mặt xám than, chữ trắng ấm và điểm nhấn vàng kim #D8B56D / vàng sáng #F0D59A.
- Chuẩn hóa khoảng cách, viền, bo góc, kích thước chữ và trạng thái điều hướng; giảm độ lớn của một số khung nội dung.
- Làm mới thanh tìm kiếm, nút thông báo, menu bên trái và thanh điều hướng dưới cho điện thoại.
- Giữ các màn hình hồ sơ, tin nhắn, album và trình xem ảnh tương thích với giao diện mới.

### Khám phá và tìm kiếm
- Thêm mục Khám phá vào menu desktop và thanh điều hướng mobile.
- Tìm kiếm nội dung bài viết, tên hiển thị, nhãn tài khoản và bình luận cục bộ.
- Tìm kiếm tiếng Việt không phân biệt dấu, ví dụ “cong nghe” có thể khớp “Công nghệ”.
- Thêm các lối tắt chủ đề SYNTRA, Công nghệ, Sáng tạo, Cộng đồng, Ảnh và Video.
- Hiển thị nội dung phù hợp với truy vấn; khi chưa nhập truy vấn, hiển thị các bài demo được sắp xếp theo lượt thích mẫu.

**Giới hạn:** tìm kiếm chỉ hoạt động trên dữ liệu demo đang lưu trong trình duyệt. Chưa có tìm kiếm người dùng thật, hashtag server-side, xu hướng thời gian thực, thuật toán đề xuất, tài khoản thật hoặc đồng bộ giữa thiết bị.

### Kiểm tra phiên bản
- JavaScript inline đã được kiểm tra cú pháp sau khi cập nhật.
- Đã xác minh lại nội dung index.html từ GitHub.
- Cần tiếp tục kiểm thử tương tác thực tế trên trình duyệt Android và desktop trước khi phát hành công khai.


## Prototype 1.0 — Cài đặt, quyền riêng tư và dữ liệu

- Thêm trang Cài đặt riêng và mục điều hướng desktop.
- Các tùy chọn demo gồm chế độ hiển thị hồ sơ (mô phỏng), bật/tắt hoạt động demo, bật/tắt thao tác theo dõi demo và giao diện gọn.
- Giao diện gọn áp dụng trực tiếp cho bài viết và composer.
- Xuất bản sao JSON gồm hồ sơ, bài viết, cuộc trò chuyện, thông báo, danh sách theo dõi và cài đặt. File xuất không gồm media blobs.
- Đặt lại tùy chọn về mặc định.
- Xóa dữ liệu demo trên thiết bị, gồm media đã lưu trong IndexedDB, sau xác nhận.
- Trang thông tin phiên bản và đường dẫn GitHub.

**Giới hạn quyền riêng tư:** tùy chọn hiển thị hồ sơ chỉ là trạng thái mô phỏng; chưa có tài khoản online, quyền truy cập máy chủ, xác minh hay đồng bộ. Dữ liệu trong browser có thể bị người dùng cùng thiết bị truy cập. Không dùng dữ liệu/mật khẩu nhạy cảm.


## Prototype 1.1 — Chi tiết bài viết và bình luận

- Mở trang chi tiết riêng khi nhấn vào khu vực nội dung bài viết hoặc số lượng bình luận trên bảng tin.
- Hiển thị đầy đủ nội dung, ảnh/video đính kèm, trạng thái thích/lưu và danh sách bình luận.
- Thêm bình luận ngay trong trang chi tiết; dữ liệu vẫn được lưu cục bộ trên thiết bị.
- Có nút quay lại bảng tin; tiếp tục sử dụng cơ chế lưu dữ liệu demo hiện tại.

**Giới hạn:** đây vẫn là tính năng frontend/local demo. Bình luận chưa đồng bộ qua máy chủ, chưa có tài khoản thật, phân quyền, kiểm duyệt hoặc thông báo thời gian thực.

### Kiểm tra phiên bản 1.1
- Đã đọc lại index.html từ GitHub sau khi cập nhật.
- JavaScript inline vượt qua kiểm tra cú pháp bằng bộ phân tích JavaScript.
- Đã xác minh các thành phần trang chi tiết, biểu mẫu bình luận, điểm mở trang chi tiết và bộ xử lý thao tác.
- Chưa thực hiện kiểm thử trình duyệt thực tế trên Android/desktop; cần kiểm tra thao tác và bố cục trên thiết bị trước khi phát hành.


## Prototype 1.2 — Hashtag tương tác

- Nhận diện hashtag trong nội dung bài viết, hỗ trợ chữ tiếng Việt có dấu, chữ Latin và chữ số.
- Hashtag được hiển thị bằng màu nhấn riêng và có thể nhấn trên bảng tin, Khám phá và trang chi tiết.
- Khi nhấn hashtag, SYNTRA Social mở Khám phá và tìm các bài viết chứa từ khóa đó.
- Nội dung bài viết vẫn được escape trước khi hiển thị; hashtag không được thực thi như HTML tùy ý.

**Giới hạn:** tìm kiếm hashtag chỉ quét bài viết đang lưu cục bộ trên trình duyệt. Chưa có hashtag xu hướng, bộ đếm toàn hệ thống, gợi ý máy chủ hoặc đồng bộ giữa người dùng.

### Kiểm tra phiên bản 1.2
- Đã đọc lại index.html từ GitHub sau cập nhật.
- JavaScript inline vượt qua kiểm tra cú pháp.
- Đã xác minh hàm định dạng hashtag, hai vị trí hiển thị nội dung bài viết và xử lý nhấn hashtag.
- Chưa thực hiện kiểm thử tương tác trực tiếp trên trình duyệt Android/desktop.


## Prototype 1.3 — Content Discovery

- Thêm bộ lọc riêng cho bài viết văn bản; tiếp tục hỗ trợ Theo dõi, Video, Ảnh và Cộng đồng.
- Bổ sung lựa chọn sắp xếp Mới nhất và Phổ biến trên bảng tin và trang Khám phá.
- Mỗi chủ đề trong Khám phá mở thành trang chủ đề riêng, có tiêu đề và nút quay lại danh sách chủ đề.
- Giữ tìm kiếm tiếng Việt không phân biệt dấu và tìm kiếm hashtag cục bộ.
- Thứ tự Mới nhất sử dụng thứ tự bài viết hiện có trong dữ liệu cục bộ; Phổ biến sắp xếp theo lượt thích đang lưu.

**Giới hạn:** chủ đề, tìm kiếm, bộ lọc và sắp xếp chỉ xử lý bài viết trong trình duyệt hiện tại. Chưa có dữ liệu thời gian thực, thuật toán đề xuất, chỉ mục máy chủ hoặc đồng bộ giữa người dùng.

### Kiểm tra phiên bản 1.3
- JavaScript inline đã vượt qua kiểm tra cú pháp.
- Đã kiểm tra sự hiện diện của bộ lọc Văn bản, trang chủ đề, hai lựa chọn sắp xếp và bộ xử lý điều hướng chủ đề.
- Đã sửa luồng giữ trang chủ đề khi mở từ thẻ chủ đề và khôi phục thanh sắp xếp khi quay về bảng tin.
- Chưa thực hiện kiểm thử tương tác trực tiếp trên trình duyệt Android/desktop.


## Prototype 1.4 — Creator System

- Creator dashboard appears on the local account's profile.
- Summary metrics show published posts, likes, comments, and posts containing media.
- Creator content filters: All, Text, Photos, Video, and Communities.
- Profile post cards open the existing post detail view.
- Editing the local profile name also updates the author name on that profile's existing local posts.
- Settings version label updated to 1.4.

**Analytics limitations:** all metrics are calculated from posts saved in this browser. There are no verified views, reach, audience demographics, revenue, cross-device synchronization, or server analytics. Follower totals remain unavailable rather than being fabricated.

### Prototype 1.4 verification
- JavaScript inline syntax check passed.
- Verified creator dashboard metrics, content filter controls, responsive metric layout, and profile edit flow are present.
- Removed an unfinished control rather than leaving a button without an action.
- Live browser interaction testing on Android and desktop remains pending.


## Prototype 1.5 — SYNTRA Communities

- Thêm trang Cộng đồng riêng trong điều hướng desktop.
- Khởi tạo ba nhóm mẫu: Góc Công nghệ, Góc Học tập và Xưởng Sáng tạo.
- Tạo cộng đồng mới với tên, mô tả và danh mục; kiểm tra tên tối thiểu và trùng lặp.
- Mở trang chi tiết nhóm, xem mô tả, số thành viên và số bài viết.
- Tham gia/rời nhóm mẫu; thành viên có thể đăng bài trong nhóm.
- Người tạo có thể chỉnh sửa tên và mô tả cộng đồng của mình.
- Dữ liệu nhóm và bài viết nhóm lưu riêng trong localStorage, không trộn vào bảng tin chung.

**Giới hạn:** đây là mô phỏng cục bộ trên một trình duyệt/thiết bị. Thành viên chỉ đại diện cho người dùng cục bộ đã tham gia; chưa có tài khoản thật, thành viên từ nhiều thiết bị, phân quyền máy chủ, tìm kiếm nhóm toàn hệ thống, thông báo nhóm hoặc kiểm duyệt nội dung. Không xem số thành viên cục bộ là người dùng thật.

### Kiểm tra phiên bản 1.5
- JavaScript inline đã vượt qua kiểm tra cú pháp sau cập nhật.
- Đã xác minh mã tạo nhóm, tham gia/rời nhóm, đăng bài trong nhóm và chỉnh sửa nhóm.
- Chưa kiểm thử tương tác trực tiếp trên trình duyệt Android/desktop.


## Prototype 1.6 — Community Interaction

- Thích/bỏ thích bài viết trong cộng đồng; bộ đếm được cập nhật và lưu cục bộ.
- Bình luận trực tiếp dưới bài viết trong nhóm.
- Trả lời bình luận theo luồng một cấp, hiển thị lồng bên dưới bình luận gốc.
- Hiển thị thành viên cục bộ đã tham gia và người tạo nhóm; không tạo số liệu thành viên giả.
- Báo cáo bài viết: lưu bản ghi báo cáo trên thiết bị với trạng thái chờ xem xét cục bộ.
- Bài viết nhóm mới khởi tạo bộ đếm thích và danh sách bình luận riêng.

**Giới hạn quan trọng:** chưa có máy chủ tiếp nhận báo cáo, quy trình kiểm duyệt thật, đồng bộ nhiều người dùng, tài khoản xác thực hoặc chống spam. Báo cáo chỉ được lưu trên trình duyệt hiện tại; không có nhân viên kiểm duyệt nào nhận được. Trả lời bình luận hiện hỗ trợ một cấp lồng nhau.

### Kiểm tra phiên bản 1.6
- JavaScript inline đã vượt qua kiểm tra cú pháp.
- Đã kiểm tra sự hiện diện của các luồng thích, bình luận, trả lời, báo cáo và danh sách thành viên.
- Đã xác minh cấu trúc lưu trữ riêng cho bình luận/trả lời và bản ghi báo cáo.
- Chưa thực hiện kiểm thử tương tác trên trình duyệt thực tế hoặc Android.


## Prototype 1.7 — Community Notifications & Moderation

- Bổ sung thông báo cục bộ khi có lượt thích, bình luận hoặc câu trả lời mới trên bài viết/bình luận thuộc về một hồ sơ khác. Không tự tạo thông báo tương tác giả cho chính người đang thao tác.
- Thêm Trung tâm quản trị cho người tạo cộng đồng cục bộ: xem báo cáo thuộc nhóm của mình, đánh dấu đã xem hoặc đã xử lý.
- Chống gửi lặp báo cáo đang chờ trên cùng một bài viết trong cùng cộng đồng trên thiết bị hiện tại.
- Ghi nhật ký hoạt động quản trị khi tạo/chỉnh sửa cộng đồng và khi cập nhật trạng thái báo cáo.
- Giữ lại bản ghi báo cáo sau khi xử lý; không xóa lịch sử.

**Giới hạn:** tất cả thông báo, báo cáo và nhật ký vẫn nằm trong localStorage của trình duyệt hiện tại. Quyền quản trị chỉ là kiểm tra giao diện cục bộ, không phải phân quyền bảo mật. Không có người kiểm duyệt máy chủ, push notification, realtime, đồng bộ nhiều tài khoản hoặc bảo đảm chống sửa dữ liệu từ DevTools. Các tương tác do cùng một hồ sơ cục bộ tạo ra không phát sinh thông báo cho chính hồ sơ đó.

### Kiểm tra phiên bản 1.7
- JavaScript inline đã vượt qua kiểm tra cú pháp.
- Đã kiểm tra các luồng: báo cáo có mã định danh, chống báo cáo lặp, quyền truy cập khu vực quản trị theo chủ nhóm, chuyển trạng thái báo cáo, nhật ký quản trị và thông báo nhóm.
- Đã kiểm tra CSS responsive cho màn hình hẹp.
- Chưa kiểm thử tương tác trực tiếp trên trình duyệt Android/desktop hoặc kiểm thử backend; đây vẫn là prototype local-only.


## Prototype 1.8 — Safety & User Protection

- Chặn hồ sơ theo tên hiển thị trên thiết bị; thao tác chặn cũng bỏ theo dõi hồ sơ đó.
- Ẩn bài viết trong bảng tin/Khám phá, bài viết cộng đồng, bình luận và câu trả lời từ hồ sơ đã chặn.
- Có trang trạng thái hồ sơ bị chặn và thao tác bỏ chặn; quản lý danh sách chặn trong Cài đặt.
- Cộng đồng có phần quy tắc; người tạo nhóm có thể chỉnh sửa quy tắc cùng tên và mô tả.
- Người đăng bài trong cộng đồng có thể đánh dấu bài có nội dung cần cân nhắc; người xem phải chủ động chọn xem nội dung.
- Xóa dữ liệu demo cũng xóa danh sách chặn.

**Giới hạn quan trọng:** danh sách chặn dùng tên hiển thị, không phải ID tài khoản; có thể nhầm lẫn nếu tên bị đổi/trùng. Đây chỉ là lọc giao diện cục bộ, không ngăn người bị chặn truy cập nội dung qua máy chủ hoặc thiết bị khác. Quy tắc cộng đồng và cảnh báo nội dung chưa được kiểm duyệt tự động. Chưa có xác thực, quyền riêng tư hoặc bảo vệ thực sự phía server.

### Kiểm tra phiên bản 1.8
- JavaScript inline đã vượt qua kiểm tra cú pháp.
- Đã kiểm tra sự hiện diện của luồng chặn/bỏ chặn, lọc bài viết và bình luận, quản lý danh sách chặn, quy tắc nhóm, cảnh báo nội dung và xóa dữ liệu chặn.
- Chưa kiểm thử tương tác trực tiếp trên trình duyệt Android/desktop; chưa kết nối backend.


## Backend security preparation — 1.9C

- Added a reviewed SQL candidate for least-privilege follow acceptance: [docs/sql/LEAST-PRIVILEGE-1.9C.sql](docs/sql/LEAST-PRIVILEGE-1.9C.sql).
- Added catalog and API regression tests: [docs/LEAST-PRIVILEGE-TESTS-1.9C.md](docs/LEAST-PRIVILEGE-TESTS-1.9C.md).
- Updated the [RLS test matrix](docs/RLS-TEST-MATRIX-1.9B.md) with verified grants and policies.
- Current follow acceptance remains blocked: authenticated has no UPDATE permission or UPDATE policy on follows. The candidate allows only the recipient to transition pending → accepted. The client updates status only; a database trigger sets accepted_at.
- Notification read-state is already narrowly scoped: authenticated can update only read_at, with recipient-only UPDATE and SELECT policies. No notification permission change is proposed.
- Only one Supabase project is connected; no separate staging project was found. The candidate SQL has not been applied to the active project. API-level tests and Security Advisor verification remain pending.


## Free security checks — 1.9D

- Added a dependency-free Python static validator at [scripts/validate_security_1_9c.py](scripts/validate_security_1_9c.py). It checks the reviewed 1.9C SQL contract, least-privilege grants, recipient-only policy predicates, database-controlled acceptance timestamp, and all 14 documented API test cases.
- Added [GitHub Actions security static checks](.github/workflows/security-static-check.yml), triggered on relevant pushes and pull requests. The workflow uses the default read-only repository permission and requires no Supabase credentials or paid staging database.
- The static validator was syntax-checked and executed locally against representative fixtures: **36 static checks passed**. The current committed artifacts also passed 22 direct content/contract checks in this review.
- These checks do not execute SQL, connect to Supabase, emulate Auth/JWT, or prove RLS behavior. The 1.9C migration remains unapplied; API-level verification still requires an isolated staging environment.


## Security test automation 1.9D

- Added `scripts/test_security_validator.py`, a mutation self-test that runs the static validator in isolated temporary copies and checks that four unsafe regressions are rejected (broad UPDATE grant, missing timestamp trigger assignment, wrong recipient predicate, missing F03 regression case).
- GitHub Actions runs both the baseline static validator and mutation self-tests.
- These checks are local/static CI checks only. They do not connect to Supabase, execute migrations, test JWT/API behavior, or prove runtime RLS enforcement. The workflow run has not yet been verified.


## Security static audit 1.9F

- Deepened `scripts/validate_security_1_9c.py` to inspect transaction order, grants and protected columns, trigger function scope/search path, database timestamp transition, trigger event, policy role and both `USING`/`WITH CHECK` predicates, and unexpected extra policies.
- Expanded mutation self-tests to seven unsafe changes: broad UPDATE, protected-column grant, missing timestamp assignment, wrong identity predicate, missing WITH CHECK, extra permissive policy, and SECURITY DEFINER escalation. The baseline must still pass.
- Static checks remain a source-contract audit, not a PostgreSQL parser or runtime security test. No migration has been applied to production or a staging database.


## UI icon refresh 1.1

- Replaced desktop navigation glyphs with a cohesive rounded-outline SVG style: Home, Explore, Video, Photos, Communities, Following, Saved, Inbox, and Settings.
- Applied matching icons to mobile bottom navigation and post-composer media/community actions; the central create action uses a gold filled button.
- Added a small inline icon renderer for future UI components, using a consistent 24px viewBox, rounded strokes, and currentColor styling.
- Visual-only update: navigation behavior and local prototype data are unchanged. Browser/mobile visual testing is still pending.
- Design reference: docs/ICON-SYSTEM-1.1.md.


## UI icon refresh 1.2

- Standardized SVG icons for feed post actions (like, comment, save) and post detail actions (like, comment, save, share).
- Notification bell now uses the shared icon renderer. Interaction icons have consistent alignment, gaps, and minimum touch height.
- Visual-only change; no behavior/data changes. Browser QA remains pending.


## Icon system 1.3 — messaging, notifications and profiles
- Extended the custom SVG icon set for notification types, profile actions, and chat controls.
- Added consistent close, read-all, follow, edit, block, back, and send icon treatments.
- Documented the update in `docs/ICON-SYSTEM-1.3.md`.
- Static GitHub read-back checks passed; browser/mobile visual QA is still pending.


## Mobile UI polish 1.4
- Refined mobile feed bottom clearance, safe-area spacing, and navigation touch targets.
- Replaced topic-story emoji with consistent SVG icons and improved secondary-text contrast.
- Standardized composer and post-action control sizing without changing their handlers.
- Details: `docs/MOBILE-UI-POLISH-1.4.md`. Static source checks passed; browser/device QA remains pending.


## Post card and overflow menu 1.5
- Refined feed/discovery card surfaces, typography, spacing, and mobile action sizing.
- Added contextual three-dot menus: delete own posts (with confirmation and media cleanup) or show the report placeholder for other posts.
- Menus close on outside click or Escape and restore focus to the opener.
- Reporting is not connected to a moderation server yet. Details: `docs/POST-CARD-MENU-1.5.md`.


## Media experience 1.6
- Improved responsive album layouts for 2, 3, and 4+ photos; retained the +N overflow indicator and image viewer.
- Added a responsive video shell with a fullscreen control, feature detection, and mobile fallback.
- Preserved native video controls, local IndexedDB storage, upload limits, and no-autoplay behavior.
- Details: `docs/MEDIA-EXPERIENCE-1.6.md`. Static source checks passed; Android browser QA remains pending.


## 1.7 — Notification markup & responsive repair

- Fixed the notification button: removed JavaScript string-concatenation text from static HTML.
- Mounted the bell SVG through the existing synIcon('bell') initializer.
- Added a tablet layout for widths from 701px to 950px, with a flexible content column and hidden right rail.
- Added mobile overflow safeguards for the page, search, posts, and media; horizontal scrollers remain independently scrollable.
- Verification: fetched the updated index.html from GitHub and confirmed the broken literal is absent and the new icon initializer and responsive rules are present.
- Limitation: no real Android/browser visual test was run in this change.


## 1.8 — Visual experience polish

- Refined the visual hierarchy across the search header, feed filters, stories, composer, post cards, and action controls.
- Improved text contrast, line height, control sizing, focus visibility, and touch feedback.
- Added clearer styling for the feed sorting control and active filter state.
- Refined the mobile spacing and bottom navigation surface while retaining the existing dark, warm-gold, and violet identity.
- Respects reduced-motion preferences.
- Verification: updated index.html was fetched again from GitHub and the new visual rules were confirmed by static read-back. No live browser/device screenshot test was run.


## Prototype 1.9 — Homepage visual refinement

- Added a clear editorial heading to the home feed: “Bảng tin”.
- Added a short Vietnamese description to explain the purpose of the feed.
- Added a restrained beta-status indicator so visitors understand the product is still being tested.
- Tuned desktop and mobile spacing, typography and responsive behavior for the new heading.
- Existing feed tabs and filtering controls remain in place.

**Validation:** the updated HTML was read back from GitHub and checked for the heading, status indicator, responsive styles, preserved feed tabs and duplicate insertion. A real Android/browser visual test has not yet been performed.

## Prototype 2.0 — Mobile composer repair

- Redesigned the create-post dialog on narrow screens as a bottom sheet with safe-area-aware spacing.
- Added bounded internal scrolling so the text field, media preview, file-picker controls and publish actions remain reachable on short screens.
- Increased touch target sizing and made the action row remain visible while scrolling.
- Added dialog semantics, an accessible label for the post text field, Escape-to-close behavior, background scroll locking, and focus restoration to the opener.

**Validation:** fetched the committed index.html again from GitHub and confirmed the new CSS/JS hooks, accessibility attributes, unique style block, and removal of the old open-handler. This is a static source read-back only; real Android keyboard, browser rendering, image/video selection, and publish flow still need device testing.


## Prototype 2.7 — Sao lưu và khôi phục cục bộ

- Xuất một tệp JSON chứa các mục dữ liệu demo trong localStorage cùng ảnh/video Blob trong IndexedDB.
- Khôi phục từ tệp JSON đã tạo bởi SYNTRA Social, kiểm tra phiên bản, khóa lưu trữ và dữ liệu media trước khi thay thế dữ liệu hiện tại.
- Khôi phục media trong một IndexedDB read-write transaction; nếu transaction lỗi, trình duyệt sẽ hủy transaction.
- Giới hạn media trong mỗi bản sao là 20 MB và tệp sao lưu nhập tối đa 35 MB để tránh tiêu thụ quá nhiều bộ nhớ trên điện thoại.
- Bản sao không được mã hóa; hãy giữ tệp riêng tư. Tệp chỉ dùng để chuyển dữ liệu giữa các trình duyệt/thiết bị, không phải đồng bộ máy chủ.


## Prototype 2.8 — Trung tâm kiểm tra toàn vẹn dữ liệu

- Bổ sung công cụ quét dữ liệu cục bộ: bài viết thiếu ID, ID bài viết trùng, JSON localStorage không đọc được, media bị thiếu và media không còn được bài viết tham chiếu.
- Kiểm tra cấu trúc tệp media, bao gồm ID và Blob.
- Cho phép xuất báo cáo JSON chỉ chứa thời điểm kiểm tra, số liệu và ID liên quan; không đưa nội dung bài viết hoặc tin nhắn vào báo cáo.
- Không tự động xóa tệp media thừa, không sửa bài viết và không ghi đè dữ liệu khi phát hiện lỗi.
- Công cụ chạy trong trình duyệt hiện tại; kết quả chỉ phản ánh dữ liệu trên thiết bị đó.

**Kiểm chứng:** GitHub Actions kiểm tra cú pháp JavaScript nhúng và các điều kiện tĩnh của tính năng. Kiểm thử thao tác thực tế trên Android vẫn cần thực hiện trên thiết bị; chưa thể coi báo cáo là bằng chứng dữ liệu đã được sửa.


## Prototype 2.9 — SYNTRA Cloud và đồng bộ bài viết giữa thiết bị

- Kết nối dự án Supabase `SYNTRA-Social` bằng publishable key; không đưa service-role key vào website.
- Thêm tạo tài khoản và đăng nhập email/mật khẩu. Phiên đăng nhập được Supabase lưu trên từng trình duyệt; người dùng cần đăng nhập cùng một tài khoản trên các điện thoại.
- Bài viết văn bản mới được ghi vào bảng `public.posts` với `author_id` là tài khoản đang đăng nhập, trạng thái `published` và quyền riêng tư `private`.
- Khi đăng nhập hoặc bấm “Đồng bộ ngay”, website tải tối đa 100 bài viết của tài khoản hiện tại. Chính sách RLS hiện có chỉ cho tài khoản đọc, tạo, sửa và xóa bài viết của chính mình.
- Xóa bài viết SYNTRA Cloud sẽ xóa bản trên máy chủ, do đó bài viết cũng biến mất trên các thiết bị khác sau lần đồng bộ tiếp theo.
- Chưa đồng bộ ảnh/video, bình luận, lượt thích, tin nhắn, nhóm hoặc dữ liệu demo cũ. Các nội dung này vẫn có thể chỉ nằm trên thiết bị.
- Không tự động tải dữ liệu cũ lên máy chủ. Chỉ bài viết văn bản được đăng sau khi đăng nhập mới được ghi vào cloud.
- Dùng cùng tài khoản trên nhiều thiết bị là điều kiện để xem cùng một tập bài viết. Không chia sẻ mật khẩu qua chat hoặc mã nguồn.

**Kiểm chứng trước khi phát hành:** dự án Supabase đang hoạt động; bảng `posts` bật RLS; quyền `authenticated` có SELECT/INSERT, còn `anon` không có SELECT/INSERT; chính sách `posts_select_own` và `posts_insert_own` giới hạn theo `auth.uid() = author_id`. Cơ sở dữ liệu hiện chưa có tài khoản hoặc bài viết. Đăng ký/đăng nhập thật và kiểm tra hai điện thoại vẫn cần thử bằng tài khoản của người dùng.


## Prototype 2.10 — Private cloud media sync

- Signed-in users can publish text posts, photo albums (up to 8 images, 4 MB each / 20 MB total), or one video (MP4/WEBM, up to 12 MB).
- Media files upload to the private `syntra-post-media` Supabase Storage bucket. The bucket is not public.
- Storage SELECT, INSERT and DELETE policies restrict each account to the first folder matching its authenticated user ID.
- Media metadata is stored in the existing `public.post_media` table; no new public-facing table or service-role key is added.
- On another device, sign in to the same account and press **Đồng bộ ngay**. The app fetches the account's post/media metadata and downloads attachments only when they are displayed.
- Deleting a cloud post removes its stored media objects before deleting the post record.
- Existing local-only demo posts and files are not automatically uploaded or migrated.
- Cloud posts remain `private`; this release does not make them visible to other accounts. Comments, likes, messages, groups and public feeds are not yet cloud-synced.
- Static validation and GitHub Actions do not replace real Android upload/download testing. Test with non-sensitive sample files first.

- Signup trigger repair: fixed the profile-creation trigger to use PostgreSQL `COALESCE` syntax correctly; signup had been failing with HTTP 500 before this database migration.
- Public discovery/feed is intentionally deferred. Current cloud posts and media are private to the signed-in account.
