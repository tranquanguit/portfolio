---
title: SofaFlow — Quản lý khách hàng & tự động sinh chứng từ
slug: sofaflow
category: ERP & Business Systems
icon: ◫
status: private
period: 2026
start: 2026-03
role: Thiết kế & phát triển
stack: Flask · PostgreSQL · SQLAlchemy · docxtpl
audience: Xưởng sửa chữa và sản xuất sofa, nhân viên kinh doanh và chủ xưởng
summary: SaaS đa công ty chạy trọn vòng đời khách hàng cho xưởng sofa — từ báo giá, hợp đồng, bàn giao đến thanh toán — và tự sinh mọi chứng từ tiếng Việt trên đường đi.
tags: [Flask, PostgreSQL, SQLAlchemy, Multi-Tenant, Sinh chứng từ DOCX, RBAC, Bootstrap]
illustration: docflow
repo:
featured: true

problemHeading: Vấn đề
problemLede: Nghề sofa là nghề thủ công. Tay nghề thật, biên lợi nhuận thật, nhưng giấy tờ thì gần như toàn bộ làm tay.
problem:
  - Cùng một thông tin, gõ lại bốn lần :: Báo giá, hợp đồng, biên bản bàn giao và phiếu thanh toán đều lặp lại tên khách, kích thước và giá. Mỗi lần gõ lại là một lần có thể sai.
  - Không ai biết đơn đang ở đâu :: Hợp đồng ký chưa? Bàn giao chưa? Khách trả hết chưa? Câu trả lời nằm trong trí nhớ ai đó hoặc một cuốn sổ.
  - Mỗi xưởng một bộ giấy tờ riêng :: Logo riêng, điều khoản riêng, cách liệt kê riêng. Phần mềm đại trà buộc họ bỏ mẫu giấy tờ mà khách đã quen.
  - Nhiều cửa hàng, một chủ :: Mỗi cửa hàng chạy đơn của mình, nhưng chủ cần nhìn được tất cả mà các cửa hàng không thấy của nhau.

flowHeading: Một hồ sơ, bốn chứng từ
flow:
  - Nhận đơn :: Khách hàng, cửa hàng, kích thước, hạng mục và giá nhập một lần duy nhất.
  - Báo giá :: Sinh ra từ đơn, theo đúng mẫu của xưởng.
  - Hợp đồng :: Cùng bộ dữ liệu đó, khách ký, không gõ lại.
  - Sản xuất và bàn giao :: Biên bản bàn giao sinh ra khi giao hàng.
  - Thanh toán :: Đặt cọc và phần còn lại theo dõi ngay trên đơn, không cần sổ riêng.
  - Dòng thời gian :: Mọi giai đoạn hiện trên một màn hình, cho mọi đơn.

capabilitiesHeading: Hệ thống làm được gì
capabilities:
  - Chứng từ theo đúng mẫu của bạn :: Mỗi công ty tự tải lên mẫu DOCX có biến. Kết quả in ra là đúng bộ giấy tờ doanh nghiệp đang dùng, đã điền sẵn.
  - Dòng thời gian trực quan :: Báo giá → hợp đồng → bàn giao → thanh toán cuối, nhìn là biết đang ở bước nào.
  - Nhiều cửa hàng trong một công ty :: Cửa hàng chạy độc lập, công ty nhìn xuyên suốt.
  - Phân quyền đúng với cách xưởng làm :: Quản trị công ty, quản lý cửa hàng và nhân viên, mỗi người thấy đúng phần việc của mình.
  - Giao diện song ngữ :: Tiếng Việt cho xưởng, tiếng Anh khi cần, chuyển được ở mọi trang.
  - Tách biệt dữ liệu hoàn toàn :: Dữ liệu công ty này không bao giờ lọt sang công ty khác.

highlights:
  - Kiến trúc đa công ty, tách dữ liệu hoàn toàn giữa các công ty, mỗi công ty hỗ trợ nhiều cửa hàng.
  - Vòng đời đơn hàng theo dòng thời gian trực quan, từ báo giá qua hợp đồng, bàn giao đến thanh toán cuối.
  - Sinh chứng từ DOCX từ mẫu riêng của từng công ty, để mỗi doanh nghiệp giữ nguyên bộ giấy tờ của mình.
  - Phân quyền theo vai trò quản trị công ty, quản lý cửa hàng và nhân viên, giao diện Việt/Anh xuyên suốt.
---

## Vì sao có sản phẩm này

Mọi chứng từ trong nghề sofa đều lặp lại cùng một thông tin khách hàng và đơn hàng. Mỗi lần gõ lại là một cơ hội sai giá hoặc sai kích thước — và không ai phát hiện ra cho đến khi khách đứng trước bộ sofa đã hoàn thiện.

SofaFlow thay chỗ đó bằng **một hồ sơ chạy suốt vòng đời**.

## Quyết định thiết kế quan trọng nhất

**Mẫu chứng từ thuộc về công ty, không thuộc về phần mềm.**

Đây là điều làm sản phẩm khả thi. Mỗi doanh nghiệp có bộ giấy tờ riêng. Thay vì ép một bố cục chung, mỗi công ty tự tải lên **mẫu DOCX** có biến, và hệ thống điền dữ liệu đơn hàng vào. Thứ in ra là đúng bộ giấy tờ họ vẫn dùng.

Tôi từng nghĩ phần theo dõi vòng đời mới là lõi còn sinh chứng từ chỉ là tính năng phụ. Thực tế ngược lại — thứ khiến người ta chịu đổi cách làm là lấy được đúng giấy tờ của mình ra một cách tự động.

## Kiến trúc

Một ứng dụng Flask phân lớp có chủ ý là "nhàm chán" — khoảng 9.000 dòng Python, 35 model ORM:

| Lớp | Trách nhiệm |
| --- | --- |
| `models` | SQLAlchemy ORM — dữ liệu |
| `repositories` | Truy cập dữ liệu, tách khỏi nghiệp vụ |
| `services` | Nghiệp vụ — nơi ứng dụng thực sự ra quyết định |
| `routes` | Chỉ là endpoint HTTP, cố tình mỏng |
| `utils/template_engine` | Thay biến trong DOCX |

Nhàm chán là chủ đích. Một xưởng sofa không cần kiến trúc mới lạ; họ cần thứ hai năm sau vẫn còn người hiểu được để sửa.

Triển khai bằng Docker Compose với Nginx và Gunicorn, có file compose riêng cho production, tài liệu triển khai và sổ tay vận hành.
