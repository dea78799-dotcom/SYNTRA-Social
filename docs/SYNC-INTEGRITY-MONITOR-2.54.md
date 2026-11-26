# SYNTRA Social Prototype 2.54 — Sync Integrity Monitor

## Mục tiêu
Bổ sung trạng thái quan sát cho các nhóm dữ liệu đồng bộ trong Trung tâm đồng bộ. Tính năng chỉ đọc kết quả đã được ghi nhận bởi luồng chẩn đoán hiện có; không tự gọi thêm truy vấn Supabase và không tạo chu kỳ polling mới.

## Phạm vi
- Theo dõi bảng tin công khai, bài viết/ảnh-video, thông báo, bài đã lưu, lượt thích/bình luận và kết nối Cloud.
- Trạng thái thuộc phiên tài khoản đang đăng nhập và được xóa khi đổi tài khoản hoặc đăng xuất.
- Kết quả thành công cũ hơn 65 phút được đánh dấu "Đã cũ", phù hợp với chu kỳ dự phòng 30–60 phút cộng biên an toàn.
- Nhóm chưa có kết quả hiển thị "Chưa xác nhận", không suy diễn thành trạng thái khỏe.
- Lỗi ở nhóm chính hoặc recovery pending khiến tổng quan yêu cầu kiểm tra/thử lại. Chỉ báo các nhóm chính thành công khi bảng tin, bài viết/media, thông báo và bài đã lưu đều có kết quả thành công còn mới.

## Quyền riêng tư và giới hạn
- Trạng thái chỉ nằm trong bộ nhớ trang; không ghi thêm localStorage, không lưu nội dung bài viết, media, email, token hoặc thông tin đăng nhập.
- Không thay đổi Supabase schema, migration, RLS, grants hoặc Realtime subscriptions.
- Đây là monitor dựa trên kết quả thao tác đã chạy, không phải phép xác minh độc lập mọi bản ghi máy chủ. Nhóm chưa có sự kiện tiếp tục hiện "Chưa xác nhận".
- Kiểm thử tĩnh không thay thế kiểm thử tài khoản thật, hai thiết bị và Android.
