---
title: ShopMind — Tìm kiếm đa phương thức & RAG minh bạch
slug: shopmind
category: AI & Search
icon: ◉
status: live
period: 2026
start: 2026-10
role: Thiết kế & phát triển
stack: FastAPI · Elasticsearch · React · SigLIP2 · PostgreSQL
audience: Người đang cân nhắc dùng RAG cho catalogue sản phẩm, và người làm nghiên cứu cần số đo
summary: Trợ lý mua sắm nhìn được vào bên trong — tìm bằng chữ, bằng ảnh và kết hợp cả hai trên 1.500 sản phẩm, trợ lý RAG có citation được kiểm tra, và bộ inspector cho thấy vì sao ra kết quả đó.
tags: [RAG, Elasticsearch, FastAPI, React, SigLIP2, Tìm kiếm đa phương thức, Đánh giá, PostgreSQL]
repo: https://github.com/kt1101/shopmind-rag
featured: true

problemHeading: Vấn đề của phần lớn demo RAG
problemLede: Cho mô hình trả lời từ tài liệu của bạn mất một buổi chiều. Cho nó trả lời đúng, trích dẫn bằng chứng kiểm tra được, và biết từ chối khi không đủ căn cứ — đó mới là phần kỹ thuật thật.
problem:
  - Citation không ai kiểm :: Câu trả lời hiện ra kèm trích dẫn, và không có cách nào biết trích dẫn đó có thực sự chống đỡ cho khẳng định hay chỉ tình cờ nằm gần trong đoạn văn được truy hồi.
  - Không bao giờ nói "tôi không biết" :: Hỏi điều mà kho dữ liệu không trả lời được thì hệ thống vẫn trả lời — trong ngữ cảnh mua sắm nghĩa là bịa ra một chính sách đổi trả.
  - Không thấy được vì sao :: Khi kết quả sai, không có vết nào cho biết bước nào sinh ra nó, nên gỡ lỗi thành đoán mò.
  - "Chúng tôi cải thiện truy hồi" là một cảm giác :: Không có benchmark cố định hạt giống và tái lập được thì không chứng minh được thay đổi nào là cải thiện.

flowHeading: Một câu hỏi trở thành câu trả lời như thế nào
flow:
  - Hiểu câu hỏi :: Viết lại cho độc lập, nhận diện ý định, tự trích bộ lọc.
  - Truy hồi :: BM25 và vector dày trên sản phẩm, review và policy, hợp nhất bằng RRF.
  - Dựng context :: Chọn ứng viên theo từng nguồn và lắp đúng thứ sẽ gửi cho mô hình.
  - Sinh câu trả lời :: Trả lời theo luồng, kèm citation.
  - Kiểm tra :: Mọi ID được trích phải nằm trong đúng context đã gửi đi, nếu không thì bị loại.
  - Ghi vết :: Từng bước, điểm số và thời gian đều được ghi lại và hiện trong inspector.

capabilitiesHeading: Hệ thống làm được gì
capabilities:
  - Tìm kiếm kết hợp :: "Giống ảnh này nhưng màu đen" — ảnh neo hình dáng, chữ chỉnh thuộc tính. Gần nhất với cách người ta thực sự mua sắm.
  - Citation được kiểm tra :: Trích dẫn nào không truy ngược được về bằng chứng mô hình đã thấy thì bị loại chứ không hiển thị.
  - Có đường từ chối rõ ràng :: Khi không đủ bằng chứng, câu trả lời là `insufficient_evidence`, không phải một phương án nghe hợp lý do bịa ra.
  - Inspector minh bạch :: Câu truy vấn đã hiểu, rank BM25 / dense / RRF, từ khóa khớp, waterfall thời gian, query DSL thô và kết quả kiểm citation.
  - Lên kế hoạch mua theo ngân sách :: Tách nhu cầu, truy hồi theo từng nhu cầu, tối ưu theo ngân sách, và giải thích kết quả có trích dẫn.
  - Đo đạc chứ không khẳng định suông :: Recall@10, nDCG@10 và MRR@10 ở hạt giống cố định, kèm ablation, mỗi lần chạy ghi vào thư mục riêng.

highlights:
  - Truy hồi đa phương thức trên 1.500 sản phẩm Amazon Berkeley Objects — tìm bằng chữ, bằng ảnh và kết hợp, dùng BM25 + kNN vector dày hợp nhất bằng RRF.
  - Trợ lý RAG trả lời từ sản phẩm, review và policy, mọi citation đều được đối chiếu với đúng context đã gửi cho mô hình, và từ chối rõ ràng khi thiếu bằng chứng.
  - Inspector minh bạch sinh pipeline trace cho mọi request — từng bước, đầu vào đầu ra, điểm số, thời gian và lý do.
  - Đánh giá IR và RAG tái lập được — Recall@10, nDCG@10, MRR@10 với hạt giống cố định, kèm ablation, mỗi lần chạy ghi vào thư mục riêng.
---

## Ý tưởng

Có hai điều ở phần lớn demo RAG làm tôi khó chịu: **chúng không cho xem cách làm**, và **chúng không bao giờ chịu nói không biết**.

ShopMind là một sản phẩm mua sắm nhỏ nhưng hoàn chỉnh, dựng để làm ngược lại cả hai.

## Citation được kiểm tra thật

Quy tắc nó áp: **ID được trích phải xuất hiện trong context đã gửi đi**. Không phải "có trong kho dữ liệu" — mà có trong context của *chính request này*. Trích dẫn nào không truy ngược được về bằng chứng mô hình thực sự nhìn thấy thì bị loại chứ không hiển thị.

Và khi không có bằng chứng, câu trả lời là `insufficient_evidence`. Biết từ chối là một tính năng. Một trợ lý mua sắm bịa ra chính sách đổi trả còn tệ hơn một trợ lý nói rằng nó không biết.

## Minh bạch từng bước

Mỗi request tìm kiếm và RAG đều sinh ra một **pipeline trace**: từng bước, đầu vào đầu ra, điểm số, thời gian và lý do cho mỗi quyết định.

Đây là phần tôi sẽ giữ lại nếu phải vứt bỏ tất cả phần còn lại. Trả lời được câu *vì sao nó ra kết quả đó* biến việc gỡ lỗi một hệ truy hồi từ đoán mò thành đọc hiểu.

## Quy mô

Khoảng 40.000 dòng gồm backend FastAPI và frontend React + Vite, với khoảng 97 file test. Backend phân lớp — interfaces, application use case, domain, infrastructure adapter — kèm một pipeline engine điều khiển bằng định nghĩa YAML, nên đổi chiến lược truy hồi là việc cấu hình chứ không phải sửa code.
