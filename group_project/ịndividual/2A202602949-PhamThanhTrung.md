# Individual contribution report — Phạm Thành Trung

## Thông tin

- Họ và tên: Phạm Thành Trung
- Mã học viên: 2A202602949
- Nhóm: K4-DAY08-DDGPT (Nhóm Thuế Doanh nghiệp)
- Repository/branch: `main` / branch `Trung` (PR #5)

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Task 4 — Chunking & Indexing | Đọc 11 tài liệu Markdown chuẩn hóa, triển khai chia nhỏ chunk bằng `RecursiveCharacterTextSplitter` (size 500, overlap 50) và sinh ID ổn định | `src/task4_chunking_indexing.py` / commit `cf8c950` | Done |
| Task 4 — Embedding & ChromaDB | Viết hàm `embed_texts`, `embed_chunks` hỗ trợ OpenRouter batching (32 chunks/batch), nạp 1.832 chunks vào ChromaDB với cosine space | `src/task4_chunking_indexing.py`, `chroma_db/` / commit `0b61823` | Done |
| Task 5 — Semantic Search | Viết hàm `semantic_search`, chuyển đổi cosine distance thành cosine similarity (`1.0 - distance`), sort giảm dần và validate schema `SearchResult` | `src/task5_semantic_search.py` / commit `a0e44aa` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Chọn kích thước chunk cố định 500 ký tự với overlap 50 ký tự (`RecursiveCharacterTextSplitter`).  
   **Lý do/evidence:** Tài liệu pháp luật và chính sách thuế có các điều khoản tương đối dài; kích thước 500 ký tự vừa đủ gói trọn vẹn 1 ý hoặc 1 khoản luật mà không làm loãng vector embedding; 50 ký tự overlap giúp không bị đứt gãy câu chữ giữa các ranh giới.  
   **Trade-off:** Đối với các bảng biểu danh mục ngành nghề thuế suất dài, 500 ký tự có thể cắt ngang bảng biểu (như đã phân tích trong Worst Performer #3).

2. **Quyết định:** Chọn mô hình `openai/text-embedding-3-small` (1.536 chiều) qua OpenRouter kết hợp ChromaDB `hnsw:space="cosine"`.  
   **Lý do/evidence:** Mô hình có khả năng hiểu ngữ nghĩa tiếng Việt đa tầng tốt hơn so với các mô hình local cỡ nhỏ, tốc độ sinh embedding nhanh, chi phí hợp lý và vector chuẩn hóa độ dài giúp khoảng cách cosine phản ánh đúng độ tương đồng ngữ nghĩa.  
   **Trade-off:** Phụ thuộc vào API key OpenRouter và đường truyền mạng khi thực hiện re-indexing.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng:
  + Chạy contract test: `pytest tests/test_contracts.py -k "chunk or semantic"`
  + Query kiểm tra: *"thuế suất thuế thu nhập doanh nghiệp"*, *"chi phí được trừ"*
- Kết quả trước/sau nếu có:
  + Trước: ChromaDB chưa có dữ liệu, semantic search trả về rỗng.
  + Sau: 1.832 chunks được index thành công; semantic search trả đúng top-k chunks với score cosine từ 0.63 đến 0.80 cho query in-domain.
- Lỗi đã phát hiện và cách xử lý:
  + Lỗi metadata trong ChromaDB không nhận giá trị `None` (ở trường `url` của tài liệu pháp luật). Đã xử lý bằng cách convert `None` thành chuỗi rỗng `""` khi upsert vào Chroma và chuyển ngược lại `None` khi query.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Chưa áp dụng Table-aware chunking để bảo vệ nguyên khối các bảng biểu ngành nghề thuế suất trong file Markdown.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Bổ sung bộ tách đoạn nhận diện cú pháp Markdown Table để giữ nguyên cấu trúc bảng trong cùng 1 chunk duy nhất.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 2026-09-21
- Tên thành viên: Phạm Thành Trung
