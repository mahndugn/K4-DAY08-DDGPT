# Individual contribution report — Từ Hoàng Giang

## Thông tin

- Họ và tên: Từ Hoàng Giang
- Mã học viên: 2A202602363
- Nhóm: K4-DAY08-DDGPT (Nhóm Thuế Doanh nghiệp)
- Repository/branch: `main` / branch `TuHoangGiang_2A202602363` (PR #6)

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Task 10 — Document Reordering | Viết hàm `reorder_for_llm` đan xen chunks quan trọng về 2 đầu danh sách (`front + back[::-1]`) để giải quyết hiện tượng lost-in-the-middle | `src/task10_generation.py` / commit `a4ab590` | Done |
| Task 10 — Citation & Formatting | Viết hàm `format_context` chuẩn hóa nhãn `[Document index \| Citation: chunk_id \| Title \| Source]` để LLM tạo trích dẫn chính xác | `src/task10_generation.py` / commit `a4ab590` | Done |
| Task 10 — Multi-Provider LLM | Xây dựng hàm `call_llm` hỗ trợ linh hoạt 3 nhà cung cấp: OpenAI, Google Gemini, Anthropic Claude qua biến môi trường | `src/task10_generation.py` / commit `a4ab590` | Done |
| Task 10 — Pipeline End-to-End | Hoàn thiện hàm `generate_with_citation` trả về `GenerationResult`, tích hợp cơ chế safe refusal khi thiếu bằng chứng | `src/task10_generation.py` / commit `a4ab590` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Áp dụng chiến thuật tái sắp xếp vị trí tài liệu (`reorder_for_llm`) đưa các chunk xếp hạng cao nhất vào đầu và cuối prompt context.  
   **Lý do/evidence:** Theo nghiên cứu "Lost in the Middle", các mô hình ngôn ngữ lớn chú ý tốt nhất ở phần đầu và phần cuối context, dễ bỏ sót thông tin ở giữa. Bằng cách lấy các phần tử vị trí chẵn xếp từ đầu và phần tử vị trí lẻ đảo ngược xếp ở cuối, các bằng chứng cốt lõi luôn nằm trong vùng chú ý cao nhất của LLM.  
   **Trade-off:** Thứ tự xuất hiện trong prompt khác với thứ tự rank của Retrieval, nhưng trường `sources` trả về cho client vẫn bảo toàn nguyên vẹn thứ hạng ban đầu.

2. **Quyết định:** Thiết lập cơ chế Từ chối an toàn (Safe Refusal) với câu trả lời mặc định *"Tôi không thể xác minh thông tin này từ nguồn hiện có."* khi `chunks` rỗng hoặc LLM gặp sự cố.  
   **Lý do/evidence:** Trong lĩnh vực tư vấn pháp lý và thuế doanh nghiệp, thông tin bịa đặt (hallucination) có thể gây rủi ro pháp lý và tổn thất tài chính cho người nộp thuế. Thà từ chối khi không đủ tài liệu còn hơn trả lời sai.  
   **Trade-off:** Chatbot sẽ từ chối các câu hỏi nằm ngoài phạm vi 11 tài liệu đã nạp trong corpus.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng:
  + Chạy contract test: `pytest tests/test_contracts.py -k "reorder or generation"`
  + Query kiểm tra: *"Doanh nghiệp nộp thuế TNDN theo thuế suất bao nhiêu?"*, câu hỏi ngoài lề: *"Cách làm bánh pizza"*
- Kết quả trước/sau nếu có:
  + Trước: Chưa có logic generation, hàm trả về giá trị mock.
  + Sau: LLM trả lời chính xác kèm citation `[news/article_01.md::chunk-20]`; câu hỏi ngoài lề được từ chối an toàn đúng chuẩn `SAFE_REFUSAL`.
- Lỗi đã phát hiện và cách xử lý:
  + Lỗi SDK của Google Gemini và Anthropic có cấu trúc response khác với OpenAI (`response.text` vs `response.content[0].text`). Đã viết hàm trích xuất text riêng `_response_text()` cho từng provider để đảm bảo output luôn là chuỗi thuần nhất.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Chưa hỗ trợ lưu trữ ngữ cảnh hội thoại đa lượt (Conversation Memory) để nhớ câu hỏi trước khi hỏi tiếp (follow-up).
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Bổ sung lớp `ChatMemoryBuffer` để hỗ trợ giải quyết đại từ thay thế trong các câu hỏi nối tiếp.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 2026-09-21
- Tên thành viên: Từ Hoàng Giang
