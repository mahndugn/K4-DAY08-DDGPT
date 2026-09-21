# Individual contribution report — Nguyễn Hồng Phi

## Thông tin

- Họ và tên: Nguyễn Hồng Phi
- Mã học viên: 2A202602750
- Nhóm: K4-DAY08-DDGPT (Nhóm Thuế Doanh nghiệp)
- Repository/branch: `main` / commit `f49ef6c`

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Task 6 — BM25 Lexical Search | Triển khai hàm `tokenize` (chuẩn hóa NFD, tách từ, loại bỏ dấu tiếng Việt) và `BM25Plus` trên corpus 1.832 chunks | `src/task6_lexical_search.py` | Done |
| Task 7 — RRF Fusion | Cài đặt thuật toán Reciprocal Rank Fusion theo công thức `RRF(d) = sum(1 / (k + rank))` với hằng số $k=60$ để hợp nhất 2 danh sách rank | `src/task7_reranking.py` | Done |
| Task 8 & 9 — Fallback & Pipeline | Xây dựng pipeline `retrieve()`, tích hợp cơ chế fallback PageIndex khi dense cosine score < threshold và bắt ngoại lệ an toàn | `src/task8_pageindex_vectorless.py`, `src/task9_retrieval_pipeline.py` | Done |
| Fallback Threshold Calibration | Thực nghiệm đo điểm cosine trên query in-domain và out-domain để chốt ngưỡng `SCORE_THRESHOLD=0.5` | `.env.example` / commit `f49ef6c` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Sử dụng thuật toán `BM25Plus` thay vì `BM25Okapi` và tiền xử lý bỏ dấu tiếng Việt trong bước tokenize.  
   **Lý do/evidence:** `BM25Okapi` bị lỗi điểm IDF bằng 0 hoặc âm khi từ khóa xuất hiện trong hơn 50% số document/chunk; `BM25Plus` có thêm hằng số làm mượt $\delta$ giúp luôn duy trì điểm dương. Việc bỏ dấu giúp người dùng gõ không dấu (*"thue tndn"*) vẫn truy xuất đúng *"thuế TNDN"*.  
   **Trade-off:** Khả năng phân biệt một số từ đồng âm khác nghĩa không dấu có thể giảm nhẹ, nhưng trải nghiệm tìm kiếm tiếng Việt thực tế tăng lên đáng kể.

2. **Quyết định:** Quyết định kích hoạt fallback bằng điểm Cosine Score gốc của Dense Search thay vì RRF Score, và chốt ngưỡng ở mức `0.5`.  
   **Lý do/evidence:** RRF score chỉ là điểm số xếp hạng tương đối phụ thuộc vào độ dài danh sách (thường dao động trong khoảng $0.01 - 0.03$), không phản ánh độ tương đồng nội dung thực tế; trong khi đó Dense Cosine đo chính xác góc ngữ nghĩa. Đo đạc thực nghiệm cho thấy query in-domain đạt 0.63–0.80, out-of-domain đạt 0.28–0.41, do đó ngưỡng 0.5 là ranh giới phân tách an toàn và tối ưu.  
   **Trade-off:** Cần duy trì mô hình embedding ổn định để không làm lệch ngưỡng hiệu chỉnh 0.5.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng:
  + Chạy contract test: `pytest tests/test_contracts.py -k "bm25 or rrf or retrieve"`
  + Query kiểm tra: *"Nghị định 123/2020/NĐ-CP"*, *"Mẫu 04/SS-HĐĐT"*, query out-domain: *"thời tiết hôm nay thế nào"*
- Kết quả trước/sau nếu có:
  + Trước: Dense search không tìm ra đúng tài liệu cho các mã hiệu văn bản viết tắt.
  + Sau: BM25 bắt chính xác 100% các mã văn bản và đưa lên đầu bảng xếp hạng RRF; query out-domain kích hoạt fallback hoặc trả điểm < 0.5.
- Lỗi đã phát hiện và cách xử lý:
  + Lỗi PageIndex API trả lỗi hoặc không có API key làm gián đoạn retrieval pipeline. Đã bọc khối `try...except` để nếu fallback lỗi thì pipeline vẫn tự động trả về kết quả Hybrid an toàn mà không làm crash ứng dụng.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Hàm `build_bm25_index` hiện tại được gọi lại ở mỗi lượt truy vấn, làm tốn khoảng 0.8–1 giây xử lý cho mỗi câu hỏi.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Bổ sung bộ nhớ đệm (caching singleton) cho đối tượng BM25 index để chỉ khởi tạo một lần duy nhất lúc ứng dụng khởi động.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 2026-09-21
- Tên thành viên: Nguyễn Hồng Phi
