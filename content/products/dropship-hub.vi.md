---
title: Dropship Hub — Phần mềm vận hành kho dropship
slug: dropship-hub
category: ERP & Business Systems
icon: ⬓
status: building
period: 2026 – Nay
start: 2026-10
role: Thiết kế sản phẩm & phát triển
stack: React 19 · Fastify 5 · TypeScript · PostgreSQL
audience: Kho dropship, các đại lý gửi hàng, và bộ phận kế toán của cả hai bên
summary: Nhận nhãn vận đơn của đại lý, đọc thẳng từ file PDF, bung combo, quét đóng hàng, bàn giao đơn vị vận chuyển và theo dõi công nợ trên cùng một hệ thống. Đại lý có portal riêng.
tags: [TypeScript, Fastify, React, PostgreSQL, Multi-Tenant, Metadata-Driven, Workflow Engine, Tồn kho]
cover: assets/img/products/dropship-hub/01-tong-quan.jpg
imageAlt: Màn hình tổng quan của công ty
repo:
featured: true
current: true

problemHeading: Vấn đề
problemLede: Mỗi ngày kho dropship xử lý hàng trăm nhãn từ hàng chục đại lý. Khi việc chạy bằng nhóm chat, Excel và sổ tay, lỗi thường rơi vào đúng sáu chỗ sau.
problem:
  - Nhãn gửi qua nhóm chat :: Mỗi sàn, mỗi đơn vị vận chuyển một mẫu nhãn khác nhau. Nhân viên phải mở từng file, gõ lại mã vận đơn và hàng trong kiện.
  - Tên hàng mỗi đại lý một kiểu :: Cùng một combo, mỗi shop đặt một tên. Kho phải đoán, nên dễ đóng thiếu hoặc nhầm thành phần.
  - Đơn đã hủy vẫn bị đóng :: Người mua hủy trên sàn khi kho đã in nhãn. Không ai báo kịp, kiện vẫn được đóng và giao đi, mất phí hai chiều.
  - Bàn giao đếm tay :: Không biết kiện nào của đại lý nào, của yêu cầu nào đã đi. Cuối ngày đối chiếu với đơn vị vận chuyển rất mất thời gian.
  - Công nợ ghi sổ :: Tiền hàng, phí dịch vụ, hàng hoàn, chiết khấu tính tay theo từng đại lý. Cuối tháng đối chiếu kéo dài nhiều ngày.
  - Ai cũng thấy giá :: Nhân viên kho cần biết trong kiện có gì, nhưng lại thấy cả giá bán, phí và chiết khấu của từng đại lý.

flowHeading: Một luồng từ nhãn vận đơn đến công nợ
flow:
  - Tải file nhãn PDF :: Trên portal, một hoặc nhiều file, nhãn của nhiều sàn trộn lẫn.
  - Đọc nhãn, tạo yêu cầu :: Lấy mã vận đơn, đơn vị vận chuyển và hàng trong từng kiện. Trùng mã thì chặn.
  - Duyệt và xác nhận :: Kinh doanh kiểm tra, đại lý xác nhận. Hàng được giữ trong kho ngay lúc đó.
  - In nhãn, dán, quét :: In tất cả nhãn của yêu cầu theo thứ tự kiện, dán lên kiện, quét mã vận đơn là xong kiện đó.
  - Bàn giao vận chuyển :: Một biên bản cho nhiều yêu cầu. Chốt biên bản là xuất kho và lập phiếu công nợ.
  - Công nợ, thu tiền :: Sao kê theo đại lý, tuổi nợ, phiếu thu. Hàng hoàn quét nhập lại kho.

capabilitiesHeading: Hệ thống làm được gì
capabilities:
  - Đọc nhãn PDF không cần mẫu :: Đọc chữ trực tiếp trong file PDF, không chụp ảnh, không nhập tay. Có sẵn quy cách cho Shopee (SPX), Lazada, TikTok Shop, Viettel Post và SuperShip; nhãn khác đọc theo cách chung. :: assets/img/products/dropship-hub/04-nhan-van-don.jpg
  - Dạy một lần, lần sau tự nhận ra :: Tải nhãn mẫu, kéo chuột quanh thông tin cần đọc. Vùng đọc bám theo chữ in sẵn gần nhất, nên nhãn có thêm dòng vẫn đọc đúng. :: assets/img/products/dropship-hub/07-quy-cach-nhan.jpg
  - Hiểu cách đại lý gọi tên hàng :: Khai "cách gọi trong tin nhắn" để đại lý dán "30 combo A, 20 B" là hệ thống ra đúng mặt hàng, đúng số lượng. :: assets/img/products/dropship-hub/08-quy-tac-san-pham.jpg
  - Bung combo đúng thành phần :: Combo không cần tồn riêng; số bộ ráp được tính từ thành phần ít nhất trong kho. Kho thấy rõ cần cho gì vào kiện. :: assets/img/products/dropship-hub/41-combo.jpg
  - Bắt đơn hủy ngay tại trạm quét :: Đơn đã hủy trên sàn, quét tới là hiện cảnh báo đỏ và kiện không được tính là đã đóng. :: assets/img/products/dropship-hub/22-kho-don-huy.jpg
  - Tồn kho luôn khớp thực tế :: Không ai sửa thẳng con số tồn. Mọi thay đổi đi qua chứng từ và để lại dấu vết — nhập mua, xuất bàn giao, chuyển kho, nhập hoàn, kiểm kê. :: assets/img/products/dropship-hub/50b-ton-kho-combo.jpg
  - Tách tiền khỏi hàng :: Quyền "xem tiền" tách riêng. Tiền được ẩn ở mọi nơi — danh sách, chi tiết, bộ lọc, xuất Excel, tổng quan, thông báo — với người không có quyền. :: assets/img/products/dropship-hub/21-kho-chi-tiet.jpg
  - Mỗi tối mỗi đại lý nhận báo cáo riêng :: Tự gửi vào giờ công ty chọn, trên portal và qua email hoặc Zalo, kèm mã QR có sẵn số tiền và nội dung chuyển khoản. :: assets/img/products/dropship-hub/53-portal-sao-ke.jpg
  - Khuyến mãi thay cho PDF trong nhóm chat :: Phát hành bảng giá và quà theo kênh bán, đại lý bấm tham gia, quà tự gắn vào đúng kiện và xuất kho cùng hàng. :: assets/img/products/dropship-hub/43-khuyen-mai.jpg
  - Mọi trao đổi ở một chỗ :: Mỗi đại lý một luồng trao đổi với công ty, biết bên kia đã đọc chưa, giao được người phụ trách — thay cho hàng chục nhóm chat. :: assets/img/products/dropship-hub/45-tin-nhan.jpg

galleryHeading: Thêm màn hình
gallery:
  - assets/img/products/dropship-hub/03-chi-tiet-yeu-cau.jpg :: Một yêu cầu đóng hàng — nhãn, kiện, tiến độ và chứng từ ở một chỗ
  - assets/img/products/dropship-hub/22a-kho-quet.jpg :: Trạm đóng gói sau khi quét
  - assets/img/products/dropship-hub/52-kiem-cuoi-ca.jpg :: Kiểm cuối ca
  - assets/img/products/dropship-hub/10-bien-ban.jpg :: Biên bản bàn giao đơn vị vận chuyển cho nhiều yêu cầu
  - assets/img/products/dropship-hub/11-cong-no.jpg :: Công nợ theo đại lý — số dư, hạn mức, tuổi nợ
  - assets/img/products/dropship-hub/48-bao-cao-cuoi-ngay.jpg :: Báo cáo công nợ cuối ngày phía công ty
  - assets/img/products/dropship-hub/30-portal-tong-quan.jpg :: Trang tổng quan của đại lý
  - assets/img/products/dropship-hub/33-portal-catalog.jpg :: Sản phẩm và giá riêng của đại lý trên portal
  - assets/img/products/dropship-hub/37-portal-dien-thoai-yc.jpg :: Yêu cầu trên điện thoại
  - assets/img/products/dropship-hub/44-portal-khuyen-mai.jpg :: Chương trình khuyến mãi trên portal đại lý
  - assets/img/products/dropship-hub/46-thong-bao.jpg :: Ai đã đọc và xác nhận thông báo
  - assets/img/products/dropship-hub/47-portal-thong-bao.jpg :: Đại lý đọc và xác nhận thông báo
  - assets/img/products/dropship-hub/14-thiet-lap.jpg :: Trang thiết lập — công ty tự chỉnh, không cần lập trình
highlights:
  - Đọc nhãn vận đơn thẳng từ chữ trong PDF theo quy tắc riêng từng đại lý, chặn trùng mã vận đơn giữa các file, các yêu cầu và các đại lý.
  - Đóng hàng theo quét mã, tiến độ từng phần ("đã đóng 4/10", "đã giao 0/10") và trạng thái từng kiện, nên đóng một phần vẫn giao được.
  - Sổ kho chỉ ghi thêm với tồn thực / đang giữ / khả dụng, khóa dòng khi nhiều người quét cùng lúc, kèm bộ kiểm tra toàn vẹn dữ liệu.
  - Nền tảng chạy theo metadata — định nghĩa DocType sinh ra validate API, truy vấn danh sách, giao diện form, mẫu Excel và OpenAPI, nên trường riêng của khách là cấu hình chứ không phải bản phát hành.
---

## Dành cho ai

Kho dropship đóng và giao hàng thay cho nhiều đại lý — và chính các đại lý đó, vốn được dùng portal riêng thay vì nhắn tin vào nhóm chat.

## Ý tưởng thiết kế

**Mọi thứ gắn vào một yêu cầu.** Nhãn, nhóm kiện, hàng xuất kho, tin nhắn xác nhận và chứng từ liên quan đều nằm trong yêu cầu đóng hàng đó. Không có chỗ thứ hai để tra.

Chính điều đó làm phần còn lại khả thi: tiến độ có thể là một phần mà vẫn chính xác ("đã đóng 4/10, đã giao 2/10"), mọi màn hình đều hiện được **việc tiếp theo** để ai mở yêu cầu cũng biết đang chờ ai, và phiếu công nợ cuối cùng được lập từ những gì thực sự đã bàn giao chứ không phải từ những gì đã đặt.

## Kiến trúc

| Thành phần | Lựa chọn |
| --- | --- |
| Giao diện | React 19 + Ant Design, một khung UI cho cả app công ty và portal đại lý |
| API | Node 24 + Fastify 5, TypeScript chạy trực tiếp, không bước build |
| Metadata | Định nghĩa DocType sinh ra validate API, truy vấn danh sách, giao diện form, mẫu Excel và OpenAPI |
| Engine | CRUD dùng chung, workflow engine định nghĩa trong cơ sở dữ liệu, dãy số, cài đặt, audit và outbox |
| Đọc nhãn | Trích chữ từ PDF theo quy tắc riêng từng đại lý, kèm ghép/tách trang và sinh PDF |
| Tích hợp | Bộ kết nối ERP dạng plugin, kết nối sàn và đơn vị vận chuyển, outbox → webhook ký HMAC |

**Lớp metadata mới là điểm mấu chốt.** Định nghĩa thực thể nằm trong cơ sở dữ liệu chứ không nằm trong code, nên hợp đồng API, bộ lọc danh sách, bố cục form và mẫu nhập Excel đều sinh ra từ một định nghĩa duy nhất. Thêm một trường riêng cho khách hàng là việc cấu hình, không phải một bản phát hành.

**Tồn kho là sổ, không phải con số.** Tồn thực, đang giữ và khả dụng đều được tính ra từ chứng từ. Hàng được giữ ngay khi đại lý xác nhận. Mỗi dòng tồn được khóa khi ghi, nên nhiều người quét cùng lúc vẫn ra đúng số. Có bộ kiểm tra toàn vẹn chạy được bất cứ lúc nào: tồn = sổ kho, hàng giữ = đơn đang mở, không tồn âm, công nợ = sổ công nợ.

## Tách biệt và an toàn

Dữ liệu từng công ty, từng đại lý được tách **ngay trong cơ sở dữ liệu**, không phải bằng một bộ lọc mà ứng dụng phải nhớ áp vào. Thông tin người mua được giữ kín, mọi thao tác đều có nhật ký, và sổ đã chốt kỳ thì không sửa được.

> **Đang phát triển.** v2 là bản viết lại hoàn toàn; app Flask cũ được giữ ở `legacy/` chỉ để tham chiếu. Em sẽ bổ sung mô hình DocType và hợp đồng tích hợp khi chúng ổn định.
