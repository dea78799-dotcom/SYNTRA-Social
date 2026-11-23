# SYNTRA Social

**A social platform for video, photos, posts, and communities.**

> Status: **Prototype 1.8** — mobile-first local prototype with discovery, creator dashboard, community groups, local social interactions, and safety controls including block, community rules, and content warnings.

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

Demo posts created in this version are saved in browser local storage on the current device. They are not published or visible to other people.

## Roadmap
1. Responsive front-end prototype — in progress; local demo features are available.
2. Backend foundation — initial Supabase database and RLS deployed; real authentication/client integration pending.
3. Profiles and following — demo/local version implemented; server-side social graph pending.
4. Posts, comments, reactions and notifications — local demo implemented; real moderation/report/block tools pending.
5. Local image/video attachments and multi-image albums — prototype implemented; cloud media storage pending.
6. Short-video feed, recommendations and streaming — pending.
7. Real communities and group membership — pending.
8. Security, privacy controls, accessibility and deployment testing — required before public launch.
9. Explore/discovery and search — local prototype implemented; real recommendations and server-side indexing pending.

## Backend preparation

- The backend architecture is documented in [docs/BACKEND-ARCHITECTURE.md](docs/BACKEND-ARCHITECTURE.md).
- The read-only Supabase schema/RLS review is recorded in [docs/BACKEND-AUDIT-1.9.md](docs/BACKEND-AUDIT-1.9.md).
- Supabase project `SYNTRA-Social` is active in Singapore (`ap-southeast-1`). The initial nine-table PostgreSQL schema and RLS baseline are deployed. Email provider configuration, frontend authentication, Storage policies and end-to-end tests are still pending.
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
