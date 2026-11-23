# SYNTRA Social

**A social platform for video, photos, posts, and communities.**

> Status: Prototype 0.1 — under active development and testing.

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
1. UI prototype and mobile testing
2. Backend + authentication
3. Profiles and follow system
4. Posts, comments, reactions, report/block tools and moderation
5. Image upload
6. Short-video feed
7. Communities
8. Security, accessibility and deployment testing

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
