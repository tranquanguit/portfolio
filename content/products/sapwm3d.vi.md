---
title: sapwm3d — Nền tảng trực quan hóa kho hàng
slug: sapwm3d
category: SAP Platform & Visualisation
icon: ⬢
status: building
period: 2026 – Nay
start: 2026-04
role: Thiết kế & phát triển
stack: TypeScript monorepo · mô hình kho chuẩn hóa · viewer 2.5D
audience: Giám sát kho, nhân viên kiểm soát tồn, quản lý vận hành
summary: Nền tảng SaaS biến dữ liệu kho thành một bản đồ vận hành — mô hình 2.5D dạng khối hiển thị độ đầy, quá tải, ô bị khóa và các điểm dữ liệu lệch nhau, dựng trên mô hình chuẩn hóa không phụ thuộc SAP.
tags: [TypeScript, Monorepo, Kho hàng, Trực quan 2.5D, SAP EWM, Multi-Tenant, Nhập Excel]
illustration: warehouse
repo: https://github.com/tranquanguit/warehouse-3d-4erp
featured: true
current: true

problemHeading: Vấn đề
problemLede: Dữ liệu kho nằm trong ERP, WMS, bảng tính và các API riêng. Tất cả đều chính xác, và gần như không có gì mang tính không gian.
problem:
  - Bảng biểu không thể hiện được một cái kho :: Giám sát hỏi "chỗ nào đang quá tải" thì nhận về mã ô và số lượng, rồi phải tự hình dung mặt bằng trong đầu.
  - Kho của mỗi khách một kiểu :: Cấu trúc, cách đặt tên và độ sạch dữ liệu khác nhau quá nhiều, nên bản trực quan làm riêng không bao giờ tái sử dụng được.
  - Dữ liệu tự mâu thuẫn :: Hàng ghi ở chỗ này nhưng không có ở chỗ kia, ô bị khóa mà không ai đánh dấu, bản ghi không map được nằm ngoài mô hình.
  - Công cụ chỉ chạy cho SAP thì loại phần lớn kho :: Rất nhiều kho vận hành bằng bảng tính và một WMS, không phải bằng EWM đã cấu hình đầy đủ.

flowHeading: Thiết kế một lần, sau đó chỉ việc theo dõi
flow:
  - Dựng mô hình kho :: Cấu hình cấu trúc và bố trí các khối ở chế độ thiết kế.
  - Map dữ liệu :: Khai báo dữ liệu đầu vào ứng với phần nào của mô hình chuẩn.
  - Nạp dữ liệu :: Excel và API trước; SAP, S/4HANA và EWM là hướng tích hợp dự kiến.
  - Trực quan hóa :: Vị trí hàng, độ đầy và sức chứa hiển thị ngay trên mặt bằng.
  - Phát hiện vấn đề :: Quá tải, ô bị khóa, dữ liệu chưa map và điểm lệch được đẩy lên, không phải đi tìm.
  - Xuất mẫu kho :: Chia sẻ hoặc tái sử dụng một cấu hình kho.

capabilitiesHeading: Hệ thống làm được gì
capabilities:
  - Bản đồ 2.5D dạng khối :: Đọc nhanh, render nhẹ, không phải xoay camera và không bị che khuất.
  - Mô hình chuẩn hóa, không phải mô hình SAP :: Lõi độc lập với cấu trúc SAP, nên phục vụ được khách ở mọi mức độ trưởng thành dữ liệu.
  - Cấu hình thay vì viết lại :: Khách mới với kho khác là việc cấu hình, không phải dự án mới.
  - Ưu tiên Excel và API :: Vì thành thật mà nói, đó là nơi dữ liệu kho thực sự nằm.
  - Phát hiện điểm lệch :: Chỗ dữ liệu tự mâu thuẫn được hiển thị, không bị giấu đi.
  - Thiết kế đa khách hàng từ đầu :: Một nền tảng phục vụ nhiều khách.

highlights:
  - Chế độ thiết kế để cấu hình cấu trúc kho, bố cục, thiết lập hiển thị và quy tắc map; chế độ vận hành để xem tồn, sức chứa và điểm lệch.
  - Phân cấp kho chuẩn hóa độc lập với cấu trúc riêng của SAP, nên cùng một lõi phục vụ được khách ở nhiều mức độ dữ liệu khác nhau.
  - Ưu tiên nạp dữ liệu qua Excel và API, còn SAP, S/4HANA, EWM và BTP là hướng tích hợp dự kiến chứ không phải điều kiện bắt buộc.
  - Monorepo tách riêng app web và API trên năm package dùng chung — mô hình chuẩn, schema nhập liệu, schema mẫu kho, hợp đồng viewer và design token.
---

## Quyết định quan trọng nhất

**Lõi không gắn với SAP.**

Tôi làm SAP cả ngày, và nước đi hiển nhiên sẽ là dựng thẳng trên cấu trúc EWM — storage type, section, bin, `/SCWM/LAGP`. Làm vậy sẽ ra bản demo nhanh hơn, và sẽ chặn sản phẩm lại ở nhóm khách vừa chạy EWM vừa cấu hình tử tế.

Thay vào đó lõi dùng một **phân cấp kho chuẩn hóa**, còn SAP chỉ là một nguồn map vào đó. Excel và API được ưu tiên trước, vì đó là nơi dữ liệu kho của phần lớn khách hàng thực sự nằm.

Cách này khiến bài toán khó trở nên tường minh — lớp map giữa dữ liệu khách đang có và mô hình mà viewer hiểu được — thay vì giấu nó sau giả định rằng dữ liệu của ai cũng sạch.

## Cấu trúc

Monorepo TypeScript:

| | |
| --- | --- |
| `apps/web` | Viewer và giao diện cấu hình |
| `apps/api` | Dịch vụ backend |
| `packages/canonical-model` | Phân cấp kho mà mọi phần còn lại đều dựa vào |
| `packages/import-schemas` | Schema có kiểm tra cho dữ liệu Excel và API |
| `packages/template-schema` | Mẫu kho xuất/nhập được |
| `packages/viewer-contracts` | Hợp đồng giữa dữ liệu và bộ render |
| `packages/ui-tokens` | Design token |

Tách `viewer-contracts` ra sớm là có chủ đích: bộ render và luồng dữ liệu tiến hóa với tốc độ khác nhau, và một hợp đồng có kiểu giữa chúng là thứ ngăn một thay đổi bên này âm thầm làm hỏng bên kia.

## Vì sao 2.5D chứ không phải 3D

Kho 3D đầy đủ trông ấn tượng khi demo và khó dùng hơn khi làm việc thật. Nhân viên vận hành cần tìm một ô và đọc trạng thái, mà bản 2.5D dạng khối làm việc đó nhanh hơn — không phải xoay camera, không bị che khuất, và render được trên đúng loại máy có sẵn ở kho.
