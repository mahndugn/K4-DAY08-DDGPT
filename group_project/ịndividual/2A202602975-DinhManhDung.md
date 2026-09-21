# Individual contribution report — Đinh Mạnh Dũng

## Thông tin

- Họ và tên: Đinh Mạnh Dũng
- Mã học viên: 2A202602975
- Nhóm: K4-DAY08-DDGPT (Trưởng nhóm — Nhóm Thuế Doanh nghiệp)
- Repository/branch: `main` / `mahndugn`

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Task 1 — Thu thập PDF Pháp chế | Tìm kiếm, kiểm tra tính hợp lệ và tải 5 văn bản PDF chính sách pháp luật về Thuế TNDN, Hóa đơn và Quản lý thuế vào `data/landing/legal/` | `src/task1_collect_legal_docs.py`, `data/landing/legal/` | Done |
| Task 2 — Crawl Bài viết Nghiệp vụ | Sử dụng Crawl4AI crawl 6 bài viết nghiệp vụ chuyên sâu từ MISA SME/meInvoice vào `data/landing/news/` kèm đầy đủ siêu dữ liệu | `src/task2_crawl_news.py`, `data/landing/news/` | Done |
| Task 3 — Chuẩn hóa Markdown | Ứng dụng `MarkItDown` chuyển đổi toàn bộ 11 tài liệu sang Markdown chuẩn tại `data/standardized/legal/` và `data/standardized/news/` | `src/task3_convert_markdown.py`, `data/standardized/` | Done |
| Evaluation — Golden Dataset | Đọc toàn bộ 11 tài liệu, biên soạn 20 cặp Q&A thực tế có trích đoạn dẫn chứng trực tiếp từ ngữ cảnh gốc vào `golden_dataset.json` | `group_project/evaluation/golden_dataset.json` | Done |
| Evaluation — Báo cáo RESULT.md | Thiết kế và hoàn thiện toàn bộ báo cáo đánh giá A/B, đo lường 4 metric (Faithfulness, Relevance, Recall, Precision), phân tích lỗi và kiến nghị | `group_project/evaluation/RESULT.md`, `reports/RESULT.md` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Mở rộng bộ dữ liệu đánh giá chuẩn (Golden Dataset) lên 20 cặp câu hỏi - câu trả lời thay vì mức tối thiểu 15 câu, bao phủ toàn bộ 5 chủ đề cốt lõi.  
   **Lý do/evidence:** Bộ dữ liệu kiểm thử quyết định độ tin cậy của toàn bộ quá trình benchmark. 20 câu hỏi được phân bổ đều cho: Công thức tính thuế TNDN, 3 bậc thuế suất 15-17-20%, chi phí hợp lý và chi phí bị loại, xử lý sai sót hóa đơn điện tử, và thuế GTGT. Mỗi câu đều trích xuất chính xác đoạn văn bản ngữ cảnh (`expected_context`) từ Markdown chuẩn hóa để làm ground truth khách quan.  
   **Trade-off:** Tốn nhiều thời gian đọc và đối soát tỉ mỉ từng điều khoản trong văn bản luật để đảm bảo câu trả lời chuẩn xác 100%.

2. **Quyết định:** Sử dụng công cụ tự động hóa `Crawl4AI` và `MarkItDown` kết hợp tiền xử lý metadata để chuyển đổi dữ liệu thô sang Markdown có cấu trúc đồng nhất.  
   **Lý do/evidence:** Dữ liệu đầu vào từ trang web và PDF của Bộ Tài chính chứa nhiều định dạng phức tạp (bảng biểu, ký tự đặc biệt). Việc chuẩn hóa về định dạng Markdown với các trường tiêu đề `# Title`, `**Source:**`, `**Crawled:**` giúp module chunking của TV 1 bóc tách siêu dữ liệu hoàn toàn tự động mà không bị lỗi runtime.  
   **Trade-off:** Một số file PDF scan lâu năm của cơ quan nhà nước khi convert sang Markdown bị lỗi khoảng trắng kép, cần lưu ý trong quá trình tiền xử lý vector.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng:
  + Kiểm thử chấp nhận toàn diện: `pytest tests/test_acceptance.py -v`
  + Đo lường kết quả đánh giá 4 metrics trên 20 câu hỏi trong `golden_dataset.json`
- Kết quả trước/sau nếu có:
  + Trước: Chưa có dữ liệu, các bài test acceptance đều fail; file `RESULT.md` chứa đầy `TODO`.
  + Sau: Đạt **5/5 tests acceptance passed 100%**; hoàn thiện báo cáo thực nghiệm so sánh chi tiết giữa Dense-only (Avg: 0.803) và Hybrid+RRF (Avg: 0.898).
- Lỗi đã phát hiện và cách xử lý:
  + Phát hiện bài test `test_evaluation_report_is_completed` bị fail do thiếu 4 tiêu đề bắt buộc (`overall scores`, `a/b comparison`, `worst performers`, `recommendations`) và còn sót placeholder `TODO`. Đã hoàn thiện toàn diện nội dung báo cáo để vượt qua bài test.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Các file PDF scan dung lượng lớn (như Nghị định 126 hơn 5.500 dòng) chưa được lọc bỏ các phụ lục mẫu biểu hành chính rườm rà trước khi đưa vào kho dữ liệu standardized.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Xây dựng bộ lọc loại bỏ các trang bìa, mục lục và biểu mẫu thủ tục hành chính không chứa thông tin quy định để tinh gọn kho ngữ liệu, giảm dung lượng index.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 2026-09-21
- Tên thành viên: Đinh Mạnh Dũng
