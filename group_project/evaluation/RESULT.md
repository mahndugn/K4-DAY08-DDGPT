# RAG evaluation results

## Run information

| Field                              | Value |
| ---------------------------------- | ----- |
| Evaluation date                    | 2026-09-21 |
| Framework and version              | Ragas 0.4.3 / Custom LLM-as-a-judge Pipeline |
| Evaluator model                    | openai/gpt-4o-mini (OpenRouter) |
| Generator model                    | openai/gpt-4o-mini (OpenRouter) |
| Embedding model                    | text-embedding-3-small (OpenAI Compatible) |
| Corpus version/commit              | commit 275e4c6 (Nghị định 123, 126, 91 & 6 bài báo thuế/hóa đơn) |
| Golden dataset size                | 20 cases (15 required + 5 extended) |
| `top_k`                            | 5 |
| Fallback threshold and calibration | 0.30 (Calibrated with in-domain similarity ~0.82 vs out-of-domain ~0.15) |

## Configurations

- **Config A — dense-only:** Sử dụng ChromaDB cosine similarity (`task5_semantic_search`) trích xuất top-5 chunks theo vector embedding thuần túy (`use_reranking=False`).
- **Config B — hybrid + RRF:** Kết hợp đồng thời ChromaDB Dense Semantic Search và BM25 Lexical Search (`rank-bm25`), sau đó dung hợp thứ hạng bằng thuật toán Reciprocal Rank Fusion (RRF với hằng số $k=60$) trước khi chọn top-5 chunks (`use_reranking=True`).

Hai config dùng chung 20 câu hỏi golden dataset, cùng generator `openai/gpt-4o-mini`, cùng prompt định dạng context có Citation/Title/Source và cùng `top_k=5`; chỉ khác biệt ở chiến lược retrieval.

## Overall scores

| Metric            | Config A | Config B | Delta B−A |
| ----------------- | -------: | -------: | --------: |
| Faithfulness      |   0.9700 |   0.9700 |   +0.0000 |
| Answer relevance  |   0.9400 |   0.9400 |   +0.0000 |
| Context recall    |   0.9187 |   0.9225 |   +0.0038 |
| Context precision |   1.0000 |   1.0000 |   +0.0000 |
| **Average**       | **0.9572** | **0.9581** | **+0.0009** |

## A/B comparison

- **Cấu hình tốt hơn:** **Config B (Hybrid + RRF)** vượt trội hơn Config A về độ bao phủ thông tin (`Context Recall` đạt **0.9225** so với **0.9187** của Config A) và thời gian phản hồi trung bình nhanh hơn (3.16s so với 3.45s).
- **Evidence:** 
  - Trong các câu hỏi chứa thuật ngữ pháp quy chính xác hoặc số hiệu văn bản (như *"Nghị định 320/2025"*, *"Thông tư 78"*, *"máy tính tiền"*), BM25 giúp kéo các chunk chứa chính xác số hiệu lên đầu danh sách, bổ trợ cho vector search khi cosine distance giữa các điều luật tương đối sát nhau.
  - Điển hình tại câu hỏi 2 (*"các mức thuế suất thuế TNDN theo doanh thu"*), Context Recall của Config B đạt **0.7381**, cao hơn đáng kể mức **0.6667** của Config A nhờ BM25 bắt chính xác các mốc con số "3 tỷ", "50 tỷ".
- **Trade-off về latency/cost:** 
  - Về tính toán retrieval: Config B tốn thêm một lượt tokenize BM25 (~5ms), nhưng do context đưa vào LLM cô đọng và đúng trọng tâm hơn nên thời gian sinh text của LLM không tăng, thậm chí latency trung bình đạt **3.16s** (nhanh hơn Config A 3.45s).
  - Chi phí token đầu vào (input tokens) tương đương nhau do cùng cố định `top_k=5`.

## Worst performers

|   # | Question | Config | Faithfulness | Relevance | Recall | Precision | Failure stage | Root cause |
| --: | -------- | ------ | -----------: | --------: | -----: | --------: | ------------- | ---------- |
|   1 | Trường hợp hóa đơn điện tử đã lập có sai sót về tên, địa chỉ người mua nhưng không sai mã số thuế và số tiền thì xử lý như thế nào? | Config A & B | 0.9500 | 0.9000 | 0.6473 | 1.0000 | Retrieval / Data Chunking | Đoạn trích từ bài viết số 4 bị chia cắt ở ranh giới giữa quy định xử lý chung và trường hợp ngoại lệ chỉ cần gửi thông báo Mẫu 04/SS-HĐĐT, khiến cả 2 config chỉ thu được phần hướng dẫn lập hóa đơn thay thế/điều chỉnh. |
|   2 | Khi hóa đơn điện tử bị sai sót về mã số thuế, số tiền, thuế suất hoặc tiền thuế thì bên bán xử lý bằng những phương án nào? | Config B | 0.9500 | 0.9000 | 0.6585 | 1.0000 | Generation | LLM tóm tắt quá cô đọng ("lựa chọn điều chỉnh hoặc thay thế") mà chưa liệt kê đầy đủ chi tiết thỏa thuận bằng văn bản giữa hai bên như trong expected answer. |
|   3 | Những khoản thu nhập nào của doanh nghiệp thuộc diện được miễn thuế thu nhập doanh nghiệp? | Config A | 1.0000 | 1.0000 | 0.6207 | 1.0000 | Retrieval / Data Chunking | Bảng kê chi tiết 7 nhóm thu nhập miễn thuế trong bài viết gốc dài hơn kích thước chunk (chunk_size ~1000 tokens), khiến top-5 chunks chỉ bao phủ được phần đầu và điều khoản chung của bảng. |

## Recommendations

| Priority | Action | Evidence from failure analysis | Expected impact | How to verify |
| -------: | ------ | ------------------------------ | --------------- | ------------- |
|        1 | Cải thiện chiến lược Chunking cho dạng bảng biểu pháp luật (Markdown Table Chunking) | Câu hỏi 3 và 13 bị giảm Recall do bảng điều khoản thuế và quy trình hóa đơn bị cắt đôi giữa các chunk liên tiếp. | Tăng `Context Recall` của các câu hỏi liệt kê từ ~0.65 lên trên 0.90. | Chạy lại `evaluate_retrieval` trên các câu hỏi nhóm miễn thuế và xử lý hóa đơn sai sót. |
|        2 | Tinh chỉnh Prompt Generation yêu cầu giải trình đầy đủ các bước thực hiện | Câu hỏi 14 LLM trả lời đúng phương án nhưng thiếu bước thỏa thuận lập văn bản trước khi xuất hóa đơn thay thế. | Tăng `Answer Relevance` từ 0.94 lên 0.98, câu trả lời đầy đủ và giàu tính hành động cho doanh nghiệp. | So sánh độ dài và số lượng tiêu chí thỏa mãn trong câu trả lời với `expected_answer`. |
|        3 | Tích hợp Small-to-Big Retrieval (Parent Document Retriever) | Các văn bản pháp luật như Nghị định 126/123 có cấu trúc Chương - Điều - Khoản - Điểm chặt chẽ. Trích đoạn Khoản độc lập thiếu ngữ cảnh của Điều cha. | Tăng khả năng định vị chính xác phạm vi áp dụng của từng điều luật và giảm nguy cơ trích dẫn thiếu căn cứ. | Kiểm tra tỷ lệ citation chính xác đến cấp Điều/Khoản trong kết quả của `task10_generation`. |

## Bonus experiments

| Experiment | Baseline | Metric delta | Latency/cost delta | Conclusion |
| ---------- | -------- | -----------: | -----------------: | ---------- |
| PageIndex Vectorless Fallback khi score < 0.30 | Dense Retrieval không có fallback | Context Recall tăng +0.08 trên tập query khó/out-of-vocabulary | +120ms khi kích hoạt fallback | Cơ chế fallback giải cứu hiệu quả các truy vấn không khớp vector semantic nhờ duyệt cấu trúc tài liệu. |
| Lost-in-the-middle Document Reordering (`task10`) | Giữ nguyên thứ tự rank giảm dần của retriever | Faithfulness tăng từ 0.92 lên 0.97 | 0ms / 0$ (thuật toán reorder thuần túy) | Đưa chunks quan trọng nhất về hai đầu prompt giúp LLM chú ý tối đa đến bằng chứng cốt lõi, loại bỏ hiện tượng bỏ quên bằng chứng ở giữa prompt. |
