# SYNTRA Social Prototype 2.55 — Conflict Recovery

## Mục tiêu
Khôi phục an toàn khi người dùng sửa bài Cloud đã thay đổi trên thiết bị khác.

## Hành vi
- Giữ nguyên bản nháp trong ô soạn khi phát hiện nội dung máy chủ khác với phiên bản đã tải.
- Hiển thị nội dung mới nhất từ Cloud trong vùng xem riêng; không thay thế bản nháp.
- Người dùng chủ động chọn “Giữ bản nháp và dùng bản Cloud mới làm mốc”. Hành động này chỉ cập nhật baseline trong bộ nhớ giao diện, không ghi lên máy chủ.
- Người dùng phải bấm “Lưu thay đổi” lần nữa để gửi bản nháp. Lần lưu tiếp tục thực hiện preflight read và compare-and-swap bằng updated_at. Nếu có chỉnh sửa mới, xung đột được phát hiện lại.
- Nếu tài khoản thay đổi trong lúc đọc/ghi/khôi phục, thao tác cũ bị hủy và không cập nhật state của phiên mới.

## Bảo vệ dữ liệu
- Không tự động ghi đè phiên bản máy chủ.
- Không lưu bản nháp vào localStorage hoặc đồng bộ sang nơi khác.
- Không thay đổi schema, migration, RLS, grants, trigger hoặc Realtime.
- Luồng chỉnh sửa bài viết cục bộ được giữ nguyên.

## Kiểm thử
Kiểm tra tĩnh bao gồm giữ bản nháp, hiển thị bản Cloud mới, xác nhận thủ công, compare-and-swap và kiểm tra phiên tài khoản. Cần kiểm thử thực tế trên hai thiết bị trước khi coi là xác minh runtime hoàn chỉnh.
