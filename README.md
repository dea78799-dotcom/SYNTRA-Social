# SYNTRA Social

**A social platform for video, photos, posts, and communities.**

> Status: **Prototype 1.1** — mobile-first local prototype with a dedicated post detail view and inline comments. Core content remains local to the current browser. Core content remains local to the current browser.

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
2. Backend, real authentication and database — not implemented.
3. Profiles and following — demo/local version implemented; server-side social graph pending.
4. Posts, comments, reactions and notifications — local demo implemented; real moderation/report/block tools pending.
5. Local image/video attachments and multi-image albums — prototype implemented; cloud media storage pending.
6. Short-video feed, recommendations and streaming — pending.
7. Real communities and group membership — pending.
8. Security, privacy controls, accessibility and deployment testing — required before public launch.
9. Explore/discovery and search — local prototype implemented; real recommendations and server-side indexing pending.

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


## Prototype 1.0 — Thiết kế lại giao diện và Khám phá

### Thiết kế giao diện
- Chuyển logo trên thanh điều hướng sang wordmark chữ SYNTRA, không thêm biểu tượng thương hiệu mới.
- Tinh chỉnh bảng màu tối: nền charcoal, bề mặt xám than, chữ trắng ấm và điểm nhấn tím #8C7BFF / lavender #B6AAFF.
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
