# SYNTRA Social

**A social platform for video, photos, posts, and communities.**

 > Status: **Prototype 2.36** — mobile-first hybrid prototype with Supabase authentication, cross-device social features, sync diagnostics, and an account security center. This remains a limited prototype, not a production-ready public social network.

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


## Prototype 2.11 — Account status and settings clarity

- Updated the settings page to distinguish real Supabase account/private media sync from features that remain local demo data.
- Removed an outdated notice claiming the app had no real account, server, synchronization, or authentication.
- Clarified that comments, likes, messages, and some settings are still local to the current browser.
- Updated the in-app prototype version to 2.11.
- Signup and login were confirmed by the project owner after the database trigger repair. Cross-device media/post behavior still needs a two-device test.


## Prototype 2.12 — Account password UX

- Added a show/hide password control to the account settings screen.
- Added a password-reset email request using Supabase Auth `resetPasswordForEmail`; the app does not collect or transmit passwords outside Supabase Auth.
- Added Vietnamese-friendly messages for common authentication errors, including incorrect credentials, unconfirmed email, duplicate registration, invalid email and rate limiting.
- Added static regression checks for the new controls and handlers.
- The reset email uses the Supabase project's configured Site URL. Password-reset email delivery and the complete recovery-link flow still require a real inbox/device test.


## Prototype 2.13 — Cross-device sync reliability

- Prevents duplicate simultaneous cloud sync requests for the same signed-in account.
- Ignores responses from an account that is no longer the active session, preventing stale data from replacing the current feed.
- Refreshes private posts and media metadata when the user returns to the tab or the device reconnects, with a 30-second cooldown after a successful sync.
- Clears cached cloud media when signing out or switching accounts so one account's downloaded media is not retained in the next account's in-memory view.
- Static regression checks cover concurrency, stale-session protection, automatic refresh triggers and media-cache cleanup.
- Real two-device verification still requires the user to sign in with the same account on both devices.

## Prototype 2.14 — Sync status feedback

- The account settings now show whether private cloud data is currently syncing, has never synced on this device, or the local time of the last successful sync.
- The manual sync button changes to "Đang đồng bộ…" and is disabled while a sync request is running, preventing repeated taps.
- A successful sync clears an earlier sync error message so the account status does not continue showing stale failure text.
- Static regression checks cover sync progress, last-success timestamp, error clearing and button loading state.
- The timestamp is local to the current browser session and is not a server audit record.


## Prototype 2.17
- Corrected the slight vertical optical offset of the settings gear in desktop and mobile navigation.
- Kept the adjustment scoped to the settings icon so other navigation icons and button hit areas remain unchanged.
- Added a static regression check for the alignment rule.


## Prototype 2.18 — Public text feed and visibility

- Added a post visibility selector; new posts default to **Private**.
- Public text posts are written with `visibility = 'public'`; private posts remain restricted to their owner.
- Added a public feed query for published public posts, plus public profile lookup restricted by `is_private = false` and `is_discoverable = true`.
- Added database grants and RLS policies so anonymous and signed-in visitors can read only published public posts and discoverable, non-private profiles. Existing owner policies remain in place. Public profile reads are column-limited to ID, username, display name and visibility flags; bio and avatar path are not exposed.
- Public posts are read-only in this prototype: likes and comments are not presented as server-backed interactions.
- Public image/video publishing is blocked for now. The media bucket and media metadata remain private to the owner until a separate public-media authorization design is completed.
- Signed-out visitors load the public feed after the cloud client initializes; public posts are preserved when accounts switch.
- Static regression checks cover visibility selection, public-only queries, private-post filtering, profile visibility, signed-out initialization and safe media restrictions.
- Requires a real two-account / signed-out browser test before treating public visibility as production-ready.


## Prototype 2.19 — Public member profiles

- Tapping the author name or avatar on a public cloud post opens that account's public profile.
- The profile page shows the account display name, username and up to 50 published public text posts.
- The profile query checks both `is_private = false` and `is_discoverable = true`; unavailable or private profiles are not shown.
- Profile reads request only ID, username, display name and visibility flags. Bio and avatar storage paths are not fetched or displayed.
- The profile post query is scoped to the selected author and `visibility = 'public'` plus `status = 'published'`.
- This remains a read-only profile view; follow counts, likes, comments and public media are not represented as server-backed features.
- Static regression checks cover profile routing, visibility checks, public-only post queries, limited profile fields and return navigation.
- Test with a signed-out browser or a second account after publishing a public text post.


## Prototype 2.20 — Cloud profile settings

- Added a signed-in account profile editor for display name, username and profile visibility.
- Profile loading requests only the existing allowed columns and is scoped to the current authenticated user ID.
- Updates are scoped to the current account, use the existing owner-only RLS policy, request the changed row with `.select()`, and verify that a row was actually updated.
- Username validation requires 3–30 lowercase letters, digits or underscores; the existing case-insensitive unique database index prevents duplicate usernames.
- Public visibility sets `is_private = false` and `is_discoverable = true`; private visibility disables both public profile discovery and profile access. Public post content remains controlled separately by each post's visibility.
- Public feed is refreshed after a successful profile update. This release does not add profile bio or avatar editing.
- Settings gear alignment from 2.17 remains unchanged.
- Static regression checks cover account scoping, column selection, validation, visibility mapping and update-result verification. Real account testing is still required.


## Prototype 2.21 — Cloud profile avatars

- Added profile avatar upload and removal in the SYNTRA Cloud profile settings.
- Uses the private `syntra-avatars` Storage bucket. Uploads are limited to JPEG, PNG or WebP and 2 MB.
- Each object is stored under the authenticated user's ID folder with a unique filename. Uploads use `upsert: false`; the profile pointer is updated only after the upload succeeds.
- Storage SELECT policy permits the owner to read their own avatar and permits other visitors to read avatars only when the corresponding profile is public and discoverable. INSERT and DELETE are owner-folder scoped.
- Public profile pages now display the stored avatar. Private profiles remain unavailable to signed-out visitors, and their avatar objects are not readable by other users.
- The database exposes only the `avatar_path` profile column in addition to the previously permitted public fields; no service-role key is used in the browser.
- Static regression checks cover upload validation, owner-scoped storage paths, profile pointer verification, deletion, and public-profile display. Real uploads and two-device viewing still need a user-device test.


## Prototype 2.22 — Cloud profile bio

- Added a 160-character bio editor to the signed-in SYNTRA Cloud profile settings, with a live character counter.
- Bio values load from and save to the current authenticated user's own profile row; the update is verified by selecting the updated row.
- Public profile pages request the bio only alongside the profile's public visibility fields. A bio is rendered only after the profile passes both `is_private = false` and `is_discoverable = true` checks, and its text is HTML-escaped before display.
- Granted column-level `SELECT (bio)` to `anon` and `authenticated`; existing profile RLS policies continue to restrict visible rows to public/discoverable profiles or the signed-in owner. No service-role key is exposed.
- Static regression checks cover the editor, character limit, owner-scoped save, public-only rendering and explicit column selection. Real account and second-device tests are still required.


## Prototype 2.23 — Cloud likes and comments

- Public published posts now load like counts, the signed-in user's like state, and comments from Supabase so interactions are consistent across devices.
- Likes and comments on public Cloud posts require a signed-in account and are written to the existing `likes` and `comments` tables. Local/demo posts keep their device-local behavior.
- Public visitors can read interactions on published public posts. Private-post interaction rows remain visible only to their owner under the existing RLS ownership rules.
- Added owner-scoped and public-post-aware RLS policies, limited new comment text to 500 characters at the client and database policy, and added a comments-by-post index.
- Static regression checks cover cross-device interaction loading, public-post checks, authenticated writes and preserving local/demo behavior. Real account and second-device interaction tests are still required.


## Prototype 2.24 — Cloud follow and private follow requests

- Added cross-device follow/unfollow for SYNTRA Cloud member profiles using the existing `public.follows` table.
- Following a public profile creates an accepted relation immediately. Following a private but discoverable profile creates a pending request; the requester can cancel it.
- Account settings show accepted follower/following counts and incoming pending requests. Profile owners can accept or reject requests.
- Private profiles remain hidden from public discovery. If a visitor reaches a private account through an already visible public post, SYNTRA shows a limited private-profile screen and allows a pending follow request. Private bio, avatar and posts are not exposed. Private-content access for accepted followers is not part of this prototype yet.
- Updated RLS: follow rows remain readable only by the two participants; only the profile owner can accept an incoming pending request; accepted relations can be created only for public/discoverable profiles. Pending requests do not expose private profile rows. Column-level UPDATE permission is limited to status and accepted_at.
- Profile discovery now permits discoverable private profiles while the client requests only identity columns for those profiles. No service-role key is exposed.
- Static regression checks cover follow state, private requests, request moderation and authentication guards. Real two-account and two-device tests are still required.


## Prototype 2.25 — Cloud Notifications

- The existing notification center now merges local/demo notices with notifications stored in Supabase and shows a combined unread badge.
- Database triggers create notifications for new likes and comments on published public posts, follow requests, new public followers, and accepted follow requests.
- Notifications are read only by their recipient under RLS. Authenticated clients can update only the `read_at` column on their own notification rows; direct client inserts are not granted.
- Trigger logic runs from a non-exposed `private` schema with a fixed empty search path. It checks the authenticated actor and derives the recipient from the affected post or follow relation; self-notifications are skipped.
- The client refreshes notifications after sign-in/account changes, when the notification panel opens, and when the app returns to the foreground. Read-all status is saved to Supabase across devices.
- Private actor profiles are not exposed to notification readers; when profile visibility blocks actor lookup, the UI uses the neutral label “Thành viên SYNTRA”.
- Static regression checks cover recipient scoping, badge aggregation, read state and the absence of direct client inserts. Runtime trigger delivery still needs a test using two real accounts and a public post.


## Prototype 2.26 — Cloud Search

- Added cross-device search for public/discoverable member profiles by display name and username, plus published public text posts.
- Profile searches explicitly filter is_private = false and is_discoverable = true; database RLS remains the final access-control boundary.
- Post searches explicitly filter visibility = 'public' and status = 'published'. Private posts are never queried by the search feature.
- Search input is length-limited, strips wildcard/control characters, waits briefly before querying, and ignores stale responses. Results are bounded and rendered with escaped text.
- No database schema changes or privileged RPCs were needed. Static checks cover privacy filters, bounded queries, escaped output, and stale-request handling. Real two-account search and private-profile tests still need to be completed.


## Prototype 2.27 — Search navigation continuity

- Fixed Cloud Search result navigation so opening a public post and returning restores the previous screen instead of always sending the user to the home feed.
- The previous view is preserved for other post-detail entry points as well, including profile and discovery screens.
- Changed the detail-page back label to the neutral “Quay lại”.
- No database or Supabase policy changes were needed.
- Static regression checks cover return-view preservation and the back control label. Device-level navigation testing remains recommended.


## Prototype 2.28 — Cloud Bookmarks

- Added the `post_bookmarks` table with a composite user/post primary key and cascading foreign keys.
- Row Level Security limits bookmark reads and deletes to the owning account. Inserts require the authenticated owner and a published public post.
- Explicit Data API grants are limited to authenticated SELECT, INSERT, and DELETE; anonymous access and direct UPDATE are not granted.
- Cloud bookmarks sync on sign-in and app foreground. The existing “Đã lưu” navigation displays cloud-saved public posts alongside local-only saved items.
- Public post content is re-fetched under the existing posts RLS policy; private or unpublished posts are excluded. Bookmarks remain account-scoped and are cleared from the local cloud state when switching accounts.
- Local/demo posts keep their existing device-only save behavior.
- Static regression checks cover ownership scoping, public-post filtering, stale-account protection, and cross-session restore. Actual two-account/device testing remains required.

## Prototype 2.29 — Cloud Sync Reliability

- Cloud sync now checks the active account again after loading likes/comments, before replacing the feed. A response started under a previous account is discarded instead of overwriting the current account's view.
- Public feed hydration captures the session identity at request start and rejects the result if the session changes before completion.
- Bookmark refresh applies saved-state changes only after the bookmark, post, profile, media and interaction reads have succeeded. A temporary query failure no longer clears the previously displayed saved state.
- Bookmark media metadata is added to the in-memory cloud cache only after the account identity is revalidated.
- The account status displays an **Ngoại tuyến** prefix when the browser reports no network connection. The manual sync control is disabled while offline; reconnecting updates the status and triggers the existing foreground sync.
- Supabase JS is pinned to 2.119.2. Current Supabase documentation describes built-in exponential-backoff retries for idempotent PostgREST GET/HEAD/OPTIONS requests on network failures and HTTP 503/520. SYNTRA does not add a second retry wrapper, avoiding duplicate retry layers. Writes are not automatically retried by that documented mechanism.
- No database migration was required.
- Static regression checks cover stale-session protection, bookmark-state preservation, and offline UI behavior. Real Android network interruption and two-device account-switch tests remain required; CI does not simulate those device scenarios.

## Prototype 2.30 — Cloud Sync Diagnostics

- Added a diagnostics panel to Settings with a manual Data API connectivity check.
- The probe requests only the id column from published public posts and applies the public visibility/status filters. It does not fetch post bodies or private account data.
- Reports request latency, last diagnostic time, most recent sync operation, and a short categorized explanation.
- Classifies common network, permission, missing-table/endpoint, server, and generic API errors. It avoids displaying credentials or raw response payloads.
- Cloud sync now records failures while loading posts, media metadata, and public likes/comments, and records successful completion.
- No database migration or new table is required.
- Static regression checks cover the minimal probe, diagnostic categories, latency display, operation status, and version metadata. Real Android offline/online testing and multi-account testing remain necessary.


## Prototype 2.31 — Cloud Sync Center

- Added a Sync Center to Settings with the 12 most recent local-device sync events and a manual “Đồng bộ lại tất cả” action.
- The history is stored locally on the current device and capped at 20 events. It stores only a generic category, timestamp, success/failure state, and safe summary; it does not store post content, credentials, or account identifiers.
- Retry refreshes the signed-in account's posts/media/interactions, public feed, notifications, and bookmarks, while preserving existing per-request account checks and sync de-duplication.
- No database migration was required.
- Static regression checks cover bounded history, local-only storage, privacy-safe summaries, and retry wiring. Actual Android and two-device testing remains required.


## Prototype 2.32 — Random Auto Sync

- Added foreground auto-sync scheduling with a newly randomized interval of 30–60 minutes after each completed cycle.
- The scheduler reuses the existing Cloud sync pipeline and its in-flight guards; it does not create parallel sync jobs.
- The timer pauses while the page is hidden or the device is offline. Returning to the app or reconnecting triggers a sync and starts a new randomized interval.
- The Settings Sync Center displays the estimated next automatic sync time.
- Browser/Android background execution is not guaranteed: mobile browsers may suspend JavaScript timers while the app is backgrounded or closed. This is foreground auto-sync, not an Android background service or push mechanism.
- No database migration was required. Automated static regression checks cover interval bounds, overlap prevention, lifecycle pause/resume, and the Settings status indicator.


## Prototype 2.33 — Account Security Center

- Added a Security Center in Settings showing the signed-in account's email verification state and the current browser/device session.
- Added a resend-confirmation action for unverified email accounts, using the Supabase Auth resend endpoint.
- Added password update with minimum-length and confirmation checks. Password values are never written to local storage or diagnostic history.
- Added “sign out other sessions” using Supabase Auth's `scope: 'others'`; the current session remains active. Revoked refresh tokens do not guarantee immediate invalidation of already-issued access tokens.
- Reviewed the current Supabase RLS configuration: all 10 public tables have RLS enabled, and current policies scope private records to their owners/participants or explicitly published public content. This is a configuration review, not a substitute for runtime tests with separate accounts.
- Supabase Security Advisor currently reports **Leaked Password Protection Disabled**. The app surfaces this warning and links to the official guidance; the setting still needs to be enabled in the Supabase dashboard.
- No database migration or new table was required. Static regression checks cover the password update, email verification, session revocation controls, and security status rendering. Real Android and two-account tests remain required.


## Prototype 2.33 — Account Security Center

- Added a Security Center in Settings with the signed-in email, email-verification state, current-device session status, and the latest database RLS baseline.
- Added authenticated password updates through Supabase Auth, including length and confirmation checks.
- Added a resend-email-verification action for accounts that are not yet verified.
- Added an explicit “Đăng xuất thiết bị khác” action using Supabase Auth's `others` scope. The current device remains signed in. Revoked refresh sessions may retain an access token until that token expires.
- Corrected ordinary sign-out to use the `local` scope, so signing out on one phone does not intentionally terminate the other phone's refresh session.
- Read-only database audit confirmed RLS is enabled on all 10 public application tables and found 35 table policies. Supabase Security Advisor still reports that leaked-password protection is disabled; the Settings panel explains where this must be enabled in the Supabase Dashboard.
- The browser app does not expose a full device/IP session inventory, so SYNTRA does not claim to show one.
- No database migration was required. Automated regression checks cover password updates, email verification resend, session scopes, and security UI wiring. Real email delivery and two-device session tests remain required.


## Prototype 2.34 — Cloud Privacy Center

- Reused the existing `public.blocks` table and added a bounded `blocked_label` display field so the account that created a block can identify it in the block list across devices.
- Added block-aware RLS to public profile, public post, follow, comment, like, and notification reads. A block hides the two accounts from each other while they are authenticated. Anonymous public browsing does not have an account identity to apply a per-account block against.
- Prevented new follow relations between blocked accounts. A private-schema trigger removes any existing follow relation in either direction when a block is created; its SECURITY DEFINER function is restricted to the authenticated blocker and uses a fixed search path.
- Added a Cloud block list with unblock controls, profile-level block actions, and block actions from the follower list.
- Added follower management: view accepted followers and remove a follower without blocking them.
- Added a Cloud data export JSON for the current account: profile, own posts, accessible comments/likes, bookmarks, follows, blocks, notifications, deletion-request records, and owned media metadata. Passwords, auth tokens, and raw media files are excluded. Browser-local demo data is not part of this Cloud export.
- Added `account_deletion_requests` with RLS and a one-active-request constraint. Users can submit and cancel a pending request. Submitting a request does **not** delete the account; the project owner must process it through a secure administrative workflow.
- No credentials or service-role key are exposed in the browser. The new public table has explicit authenticated grants and RLS. Anonymous SELECT on `blocks` is granted only because public RLS expressions reference the table; its RLS policy returns no block rows to anonymous users.
- No automatic account deletion, password changes, or data erasure are performed by this feature.
- Static regression checks cover Cloud block syncing, block controls, follower removal, export boundaries, and deletion-request state. Two-account Android tests and a manual deletion-request processing test remain required.


### 2.34.1 — Privacy permission correction

- Granted authenticated users column-level UPDATE permission on `account_deletion_requests.status` so the existing cancel-pending-request action can work.
- The existing RLS policy still limits cancellation to the signed-in owner of a pending request and requires the resulting status to be `cancelled`; users cannot update `user_id` or other columns.
- Applied and verified against the live Supabase project. The privilege check confirms UPDATE on `status` is allowed while UPDATE on `user_id` and table-wide UPDATE remain unavailable.


## Prototype 2.35 — Community Safety and Reports

- Added a Cloud report dialog for public posts, public discoverable profiles, and comments attached to public published posts. Reports require an authenticated SYNTRA Cloud account.
- Added reason categories (spam/scams, harassment, hate, violence, misinformation, privacy, and other) and optional details capped at 1,000 characters.
- Added a report-history panel in Settings. RLS continues to limit report history to the submitting account; users cannot view other users' reports or change moderation status.
- Added a server-side trigger that verifies the reporter identity, validates that the target still exists and is publicly reportable, rejects self-reports, forces new reports to `open`, and limits each account to 10 reports per rolling 24-hour period.
- The report system records cases for later owner review. It does not automatically remove content, suspend accounts, or expose an administrative moderation console. Those actions require a separately authenticated moderator workflow.
- Existing `reports` table and RLS policies were reused; no duplicate table was created. Migration: `20261124130000_syntra_social_235_report_validation.sql`.
- Static checks cover report UI, authenticated ownership, target validation, rate limits, and version metadata. Real multi-account report submission and moderation operations still require manual testing.

## Prototype 2.36 — Owner-only moderation and mandatory 2FA

- Added a private `syntra_owner_roles` table. It has RLS enabled, no client read/write grants, and intentionally contains no pre-seeded owner. Owner assignment must be performed by the project owner in the Supabase SQL Editor after verifying the correct Auth user UUID.
- Added a server-side Owner status check. The website cannot create or promote its own Owner role; user-editable profile metadata is not used for authorization.
- Added TOTP enrollment and challenge in the Owner Console using Supabase Auth MFA. The moderation queue is shown only after the current session reaches `aal2`.
- Enforced Owner membership and `aal2` in database policies and the private moderation function. Client-side visibility is only a convenience; the database remains the authorization boundary.
- Added a private moderation audit table. Status changes and audit insertion occur atomically in the server-side function. Direct authenticated-client UPDATE on `public.reports` is revoked.
- The Owner queue does not select the reporter's user ID. The existing reporter-only report-history policy remains in place.
- Allowed transitions: `open` → `reviewing`, `resolved`, or `dismissed`; `reviewing` → `resolved` or `dismissed`. Closed reports cannot be reopened through the UI.
- Owner assignment SQL (run only in the Supabase Dashboard SQL Editor after copying the correct UUID from Authentication → Users):

```sql
insert into private.syntra_owner_roles (user_id, role)
values ('AUTH_USER_UUID', 'owner')
on conflict (user_id) do nothing;
```

- No service-role key or secret is placed in browser code. The first Owner must be assigned manually before the TOTP setup screen becomes available.
- Automated static checks cover private role storage, AAL2 enforcement, TOTP flow, report queue field selection, audit logging, and the prohibition on direct client status updates. Real TOTP enrollment and moderation still require a manual signed-in test.

### 2.36.1 — Report identity column hardening

- Removed table-wide SELECT for authenticated clients on `public.reports` and re-granted only the columns required by the reporter history and Owner queue. The reporter UUID is no longer readable through the Data API.
- Updated report history to rely on the existing reporter-only RLS policy rather than filtering by the protected `reporter_id` column.
- Revoked authenticated DELETE on reports. Owner-role table remains inaccessible directly; a self-row SELECT policy is present as defense in depth, but no SELECT grant is given.
- Live ACL verification confirms authenticated users cannot read `reporter_id`, cannot directly update report status, cannot insert or read Owner roles, and cannot call moderation functions anonymously.

## Prototype 2.37 — Mobile interaction quality checks

- Improved the fixed mobile bottom navigation with a minimum 44 × 44 CSS-pixel target for each navigation control and explicit touch interaction handling.
- Constrained the post composer dialog to the dynamic viewport height and enabled internal scrolling so the action buttons remain reachable on shorter screens and when the on-screen keyboard is open.
- Added a visible keyboard-focus indicator for interactive controls.
- Expanded GitHub static regression checks for mobile navigation, composer actions, media viewer semantics, notification labeling, and the new responsive CSS.
- Added [the Android mobile regression checklist](docs/MOBILE-REGRESSION-TEST-2.37.md) for real-device checks. Automated checks cannot replace testing on physical Android phones; account sign-in, cross-device sync, media upload, and MFA still require manual verification.


## Prototype 2.39 — Private posts across devices and duplicate sync repair

- Fixed the home feed filter so private Cloud posts are visible to the currently signed-in owner on any device. Private posts from other accounts remain excluded.
- Kept private media access owner-scoped: the client downloads media only through authenticated metadata for the signed-in account, while the existing Storage RLS policy restricts objects to the matching account folder.
- Fixed Cloud sync merging by database post ID. A post already loaded from the public feed is replaced by its authoritative owner-sync row instead of being appended a second time.
- Preserved unrelated public Cloud posts and browser-local demo posts during owner sync.
- Added regression checks for owner-only private feed visibility, authenticated private media retrieval, and stable-ID deduplication. No database schema or RLS policy was changed.
- Manual verification is still required on two Android devices using the same test account: one private image/video post, one private text post, and one public text post. Confirm each appears exactly once and private posts remain invisible to a separate account.


## Prototype 2.39 — Local composer drafts

- Added automatic local draft saving for composer text, post type, and visibility as the user edits the form.
- Restores the latest draft when the composer is opened again, including after a page reload on the same browser/device.
- Added an explicit clear-draft action. A draft is also cleared after a post is successfully published; failed publishing keeps the draft.
- Drafts remain in this browser's local storage and are not uploaded to SYNTRA Cloud or shared across devices.
- Browser file inputs cannot be restored after closing or reloading a page, so image/video attachments must be selected again. No attachment bytes, passwords, or account credentials are stored in the draft.
- Added static regression checks for autosave, restoration, clearing, and the local-only/media behavior. Manual Android browser testing is still required.


## Prototype 2.40 — Multiple named composer drafts

- Added a separate local draft collection alongside the existing automatic working draft. Users can save the current text and post options under a name, reopen a saved draft, rename it, or delete it.
- The collection is capped at 20 entries. Saving with an existing name updates that named entry instead of creating a duplicate; names are compared case-insensitively.
- Stored records are validated when read. Storage and quota errors are caught and surfaced in the composer; malformed collections are not silently overwritten.
- Named drafts remain local to the current browser origin and device. They do not sync through SYNTRA Cloud. Attachments are not stored and must be selected again.
- Added static regression checks for collection bounds, CRUD actions, validation, UI wiring, and responsive styling. Real Android interaction still requires manual verification.


## Prototype 2.41 — Public feed pagination

- Reduced the initial public-feed request from 50 posts to 20 posts to limit the amount of data fetched and hydrated when opening the home feed.
- Added deterministic ordering by `created_at` and post ID, then keyset pagination using the last loaded row as a composite cursor. Older posts are fetched in additional batches of 20.
- Added a small “Tải thêm bài viết” control; the rest of the interface is unchanged.
- Appended pages are deduplicated by database post ID. Requests reject results if the signed-in account changes while they are in flight.
- Pagination state resets when the Cloud account changes or the profile is updated. No database schema, RLS policy, or storage permission was changed.
- Static regression checks cover page bounds, stable ordering, cursor filtering, duplicate prevention, account-change protection, and the load-more control. Real Android scrolling, two-account privacy, and high-volume feed tests remain required.


## Prototype 2.42 — Media loading and memory management

- Post images and videos are now queued through `IntersectionObserver`; media is fetched only when its placeholder approaches the viewport (360 px preload margin).
- Concurrent media reads/downloads are capped at three to avoid opening many IndexedDB/Storage operations at once on mobile devices.
- Images use asynchronous decoding and native lazy loading. Videos use `preload="none"` so metadata and video data are not requested until playback is needed.
- Blob URLs and in-memory Blob references are released when their media elements are no longer present in the document. The active image viewer retains its current media reference.
- Existing authenticated Storage downloads and local IndexedDB media remain unchanged. Private media is not copied into a new persistent browser cache, avoiding cross-account persistence and additional storage growth.
- Static regression checks cover viewport loading, concurrency limits, detached-node handling, lazy image/video behavior, and object URL cleanup. Manual Android scroll/playback and account-switch tests remain required.

## Prototype 2.43 — Media Cache Manager

- Expanded the existing media storage check to report the number and total size of local IndexedDB media files, the size of unreferenced local files, missing local attachments, and browser-reported origin storage usage/quota when supported.
- Shows the browser's IndexedDB usage breakdown when `navigator.storage.estimate()` provides it. Browser storage figures are estimates and may include other SYNTRA Social site data; they are not an exact media-only measurement.
- Added a manual cleanup action for local IndexedDB media records that are not referenced by the currently loaded post collection. The candidate set is recalculated immediately before deletion, and media currently open in the viewer is excluded.
- Cleanup requires explicit confirmation and deletes only the local IndexedDB copies. It does not delete posts, account data, or original media objects in Supabase Storage. No automatic cleanup or persistent-storage permission request is performed.
- Added static regression checks for storage reporting, orphan byte accounting, viewer protection, confirmation, and the local-only deletion boundary. Android browser testing is still required, especially after switching accounts, scrolling through older posts, and restoring a backup.

## Prototype 2.44 — Media Integrity Checker

- Extended the existing manual integrity audit to inspect local IndexedDB media Blob records without changing them.
- Checks stored size and MIME metadata against the actual Blob, detects zero-byte files, and reports files that cannot be read.
- Computes SHA-256 fingerprints sequentially for readable files up to 20 MB and groups identical content. Hashes are used only during the local audit; they are not uploaded or persisted. If Web Crypto is unavailable or hashing is skipped for a large file, the report marks that item as skipped rather than treating it as unreadable.
- Distinguishes media references that have authenticated SYNTRA Cloud metadata from references with neither a local file nor known Cloud metadata, avoiding a false missing-file warning for remote-only media.
- The exported integrity report is version 2 and includes detailed findings. The audit is manual and read-only: it does not repair, rename, upload, or delete files or Cloud objects.
- Added regression checks for Blob metadata, empty/unreadable media, SHA-256 duplicate grouping, hashing limits, Cloud metadata distinction, report details, and the manual-only action. Browser and Android testing remains necessary with real posts and multiple accounts.

## Prototype 2.44 maintenance audit

- A full repository review found that the Owner moderation panel defined its delegated click handler but did not register it. The panel now binds one delegated listener to its stable content root, so MFA enrollment, TOTP verification, queue refresh, and report actions can receive clicks.
- Removed an unused IndexedDB media writer, an obsolete report-action branch with no matching UI control, and a cleanup check for a viewer video element that does not exist in the current image-only viewer.
- Media integrity reports now state that reference checks cover posts and Cloud metadata currently loaded on the device. Unreferenced local media is not automatically described as a confirmed orphan.
- When Supabase is configured, local media cleanup is blocked until the public feed has been synchronized and all public-feed pages have been loaded. This avoids deleting cached media merely because its public post has not yet been paginated into the current view.
- Static validation now checks the Owner event binding, dead-code removals, integrity scope, and cleanup coverage guard. Automated checks do not replace live Supabase/RLS verification or real-device testing.


## Prototype 2.46 — Realtime multi-device post synchronization

- Enabled only `public.posts` in the existing Supabase Realtime publication. The table's existing RLS policies continue to control which rows each signed-in account can read.
- Signed-in clients listen for post INSERT and UPDATE events only. Events are used only to trigger a debounced re-fetch through authenticated Supabase queries; event payloads are not written directly into local post state. DELETE events are intentionally excluded because Supabase does not apply RLS filtering to them like normal row changes; deletions are reconciled through authenticated refresh/fallback sync.
- Realtime refresh waits for already-running post/feed requests to settle, then fetches again so a newly committed change is not hidden behind an older in-flight request.
- Realtime subscriptions are cleaned up and recreated on account changes. Existing 30–60 minute randomized fallback sync, manual sync, and foreground/reconnect sync remain.
- Added static regression checks for publication scope, debounce, in-flight request ordering, session cleanup, and fallback behavior. Live multi-device and Android background/reconnect testing remains outstanding.


## Prototype 2.47 — Expanded Realtime data synchronization

- Expanded the existing Realtime publication to include `post_media`, `comments`, `likes`, `notifications`, and `post_bookmarks`, in addition to `posts`. All six tables were checked for enabled RLS, authenticated SELECT grants, and existing policies before the migration.
- Signed-in devices listen for INSERT/UPDATE events on posts, media, comments, and notifications, and INSERT events on likes and bookmarks. Realtime payloads are invalidation signals only; content is re-fetched through authenticated queries under existing RLS.
- DELETE events remain excluded because they cannot be filtered by RLS like normal row changes. Deletes are reconciled by authenticated refresh/fallback sync, so removals may not appear instantly on another device.
- Added regression checks for all publication tables, event scope, account cleanup, debounce, in-flight sync ordering, and fallback behavior. Live two-device and Android background/reconnect testing remains outstanding.


## Prototype 2.48 — Conflict-safe Cloud post editing

- Cloud post edits now read the current server row and compare its body with the version originally loaded by the editor before attempting a write.
- The update is conditional on the exact server `updated_at` value read immediately before saving. If another device changes the post between the read and update, the conditional update returns no row and SYNTRA refuses to overwrite the newer version.
- If the server body already differs when the editor starts saving, the edit is rejected and the user is asked to reload the page to receive the current version.
- This is optimistic concurrency control for Cloud post edits; it does not implement automatic text merging. Local-only posts keep their existing save behavior.
- No database migration, RLS policy, grant, or UI redesign was needed. The existing `posts.updated_at` trigger provides the version token.
- Static regression checks cover the preflight comparison, account/owner scoping, conditional timestamp update, and both conflict paths. Simultaneous two-device editing still requires a manual live test.


## Prototype 2.49 — Offline recovery and bounded retry

- Added a small device-local recovery marker containing only the signed-in user ID, retry count, and timestamps. It stores no credentials, post text, media, or queued write operations.
- Losing network connectivity or moving the app into the background marks the current account as needing a refresh. When the device returns online/foreground, SYNTRA schedules a full authenticated refresh.
- Failed recovery attempts use exponential backoff beginning at approximately 15 seconds, capped at 5 minutes, with small random jitter to avoid synchronized retry bursts.
- Successful full recovery clears the marker. The marker is account-scoped and is not replayed under a different signed-in account.
- Existing Realtime, manual sync, 30–60 minute fallback, and local composer drafts remain unchanged. No offline post publishing queue was added, so the client will not silently submit duplicate writes after reconnect.
- Static regression checks cover account scoping, minimal persisted state, retry bounds, online/foreground triggers, success cleanup, and silent automatic retry. Android background suspension and real network interruption tests remain necessary.


## Prototype 2.50 — Data Consistency Engine

- Expanded the existing manual integrity audit to compare locally loaded Cloud posts with authenticated Supabase rows.
- Checks visible post ownership, post-media ownership, missing or locally unlinked media metadata, duplicate comment IDs, comments and likes whose parent is not visible in the audited result, and duplicate like pairs.
- Queries are account-session scoped, use batches of 40 post IDs, and read only through the existing Supabase client and RLS policies.
- The audit does not insert, update, delete, repair, or replay records. It exports Cloud findings in integrity report version 3.
- A post not returned by the current authenticated query is labelled not visible / not returned, not definitively deleted. Cloud coverage is limited to posts currently loaded on the device; comments may be truncated at 1,000 rows per batch.
- No database schema, migration, grants, or RLS policy changes were made.


## Prototype 2.51 — Sync Recovery Engine

- Automatic sync now treats public feed, own posts/media, notifications, and bookmarks as separate required results for a successful recovery cycle.
- A notification or bookmark load failure can no longer be hidden by a successful public-feed refresh.
- The public-feed 30-second debounce is bypassed for explicit recovery and session bootstrap, so a recent fetch is not misreported as a failed sync.
- Session bootstrap now checks each dataset independently and schedules account-scoped recovery if any required read fails.
- Recovery remains read-only. No offline write queue, automatic post replay, database migration, schema, grant, or RLS change was introduced.
