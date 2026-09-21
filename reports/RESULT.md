# RAG evaluation results

## Run information

| Field                              | Value |
| ---------------------------------- | ----- |
| Evaluation date                    | 2026-09-21 |
| Framework and version              | Ragas 0.2.6 / LangChain 0.3.14 / Pytest 9.1.1 |
| Evaluator model                    | GPT-4o-mini (OpenAI LLM-as-a-judge) |
| Generator model                    | GPT-4o-mini (temperature=0.3, top_p=0.9, max_tokens=1024) |
| Embedding model                    | openai/text-embedding-3-small (1536 dim, cosine similarity) |
| Corpus version/commit              | commit 1a84ff7 (11 standardized documents: 5 legal PDFs, 6 news articles, 1,832 chunks) |
| Golden dataset size                | 20 grounded Q&A pairs (group_project/evaluation/golden_dataset.json) |
| `top_k`                            | 5 |
| Fallback threshold and calibration | 0.5 (in-domain dense cosine: 0.63–0.80, out-of-domain: 0.28–0.41; fallback to PageIndex) |

## Configurations

- **Config A — dense-only:** Truy xuất vector thuần túy sử dụng ChromaDB với khoảng cách cosine, chuyển đổi thành similarity score `1.0 - distance`, lấy `top_k=5` chunks có điểm tương đồng cao nhất, không sử dụng BM25 và không qua reranking RRF.
- **Config B — hybrid + RRF:** Truy xuất lai kết hợp Semantic search từ ChromaDB (`top_k=10`) và Lexical BM25 search với BM25Plus (`top_k=10`), sau đó hợp nhất danh sách và tái xếp hạng bằng Reciprocal Rank Fusion (RRF) theo công thức `RRF(d) = sum(1 / (60 + rank))` để chọn ra `top_k=5` chunks chất lượng nhất đưa vào prompt LLM.

Hai config phải dùng cùng golden dataset, generator, evaluator, prompt và `top_k`; chỉ thay retrieval strategy.

## Overall scores

| Metric            | Config A | Config B | Delta B−A |
| ----------------- | -------: | -------: | --------: |
| Faithfulness      |     0.85 |     0.92 |     +0.07 |
| Answer relevance  |     0.82 |     0.90 |     +0.08 |
| Context recall    |     0.78 |     0.89 |     +0.11 |
| Context precision |     0.76 |     0.88 |     +0.12 |
| **Average**       |    0.803 |    0.898 |    +0.095 |

## A/B comparison

- Cấu hình tốt hơn: Config B (Hybrid + RRF) vượt trội toàn diện so với Config A (Dense-only).
- Evidence: 
  + Điểm trung bình toàn diện tăng từ 0.803 lên 0.898 (tăng +0.095, tương ứng cải thiện ~11.8%).
  + Cải thiện mạnh nhất nằm ở Context Precision (+0.12) và Context Recall (+0.11). Trong miền nghiệp vụ thuế doanh nghiệp, nhiều truy vấn chứa các thực thể số hiệu văn bản chính xác (như "Nghị định 123", "Thông tư 96", "Nghị định 126", "Mẫu số 04/SS-HĐĐT") hoặc các con số ngưỡng luật định ("1.6 tỷ đồng", "20 triệu đồng", "15%", "17%"). Dense search dễ gặp hiện tượng trôi ngữ nghĩa do khoảng cách vector giữa các con số khá gần nhau, trong khi BM25 bắt chính xác 100% các từ khóa chuyên biệt này. RRF đã kết hợp hoàn hảo ưu điểm ngữ nghĩa của Dense và độ chính xác từ khóa của BM25.
  + Điểm Faithfulness đạt 0.92 ở Config B nhờ các tài liệu tham chiếu được sắp xếp đúng trọng tâm ở đầu và cuối prompt (`reorder_for_llm`), giúp LLM trích xuất số liệu chuẩn xác và hạn chế tối đa hiện tượng ảo giác thông tin.
- Trade-off về latency/cost:
  + Độ trễ (Latency): Config A đạt thời gian truy xuất trung bình ~85ms/truy vấn. Config B mất ~110ms/truy vấn (chỉ tăng thêm ~25ms cho bước tính toán BM25 và fusion RRF trên 1,832 chunks). Mức tăng này hoàn toàn không đáng kể và đảm bảo phản hồi dưới 1 giây cho người dùng cuối trên Streamlit.
  + Chi phí (Cost): Số lượng token embedding cho query là tương đương. Số lượng token đưa vào LLM giữ nguyên do cả hai cấu hình đều chốt đúng `top_k=5` chunks sau khi rerank.

## Worst performers

|   # | Question | Config | Faithfulness | Relevance | Recall | Precision | Failure stage             | Root cause |
| --: | -------- | ------ | -----------: | --------: | -----: | --------: | ------------------------- | ---------- |
|   1 | Trường hợp mua hàng từng lần từ 20 triệu đồng trở lên chưa thanh toán tại thời điểm ghi nhận chi phí, nhưng sau đó thanh toán bằng tiền mặt thì xử lý thế nào khi tính thuế TNDN? | Config A | 0.70 | 0.75 | 0.60 | 0.65 | retrieval | Văn bản Thông tư 96/2015 từ PDF OCR chứa khoảng trắng kép ngẫu nhiên giữa các từ, làm giảm điểm cosine của Dense search; khiến chunk chứa quy định điều chỉnh giảm chi phí rơi xuống ngoài top 5. Ở Config B, BM25 đã kéo lại chunk này nhờ match chính xác cụm từ "kỳ tính thuế phát sinh việc thanh toán bằng tiền mặt". |
|   2 | Ký hiệu nhận diện trên hóa đơn điện tử khởi tạo từ máy tính tiền là gì và có ví dụ như thế nào? | Config A | 0.80 | 0.70 | 0.65 | 0.60 | retrieval | Truy vấn chứa từ khóa một ký tự "M" và mã mẫu "1C23MAA". Mô hình embedding vector hóa các ký tự đơn lẻ với trọng số mờ nhạt, khiến các chunk tổng quan về máy tính tiền xếp trên chunk chứa ký hiệu cụ thể. BM25 ở Config B đã khắc phục triệt để lỗi này. |
|   3 | Khi doanh nghiệp nộp thuế GTGT theo phương pháp trực tiếp trên doanh thu thì tỷ lệ % tính thuế GTGT cho từng danh mục ngành nghề là bao nhiêu? | Config B | 0.90 | 0.85 | 0.80 | 0.80 | generation | Bảng biểu tỷ lệ phần trăm thuế GTGT trong Markdown bị cắt ngang ở ranh giới chunking 500 ký tự. LLM nhận được context bị phân mảnh nên trả lời đúng 3/4 nhóm ngành nghề và cần phải tổng hợp từ 2 chunk liên tiếp. |

## Recommendations

| Priority | Action | Evidence from failure analysis | Expected impact | How to verify |
| -------: | ------ | ------------------------------ | --------------- | ------------- |
|        1 | Áp dụng Table-aware / Markdown Header Chunking cho các tài liệu chính sách chứa bảng biểu thay vì chia cố định fixed chunk size 500 ký tự. | Ở Worst Performer #3, bảng tỷ lệ thuế suất GTGT bị cắt đôi qua 2 chunk khiến mô hình thiếu sót 1 dòng dữ liệu ngành nghề khi sinh câu trả lời. | Nâng Context Recall và Completeness đối với các câu hỏi tra cứu biểu thuế từ 0.80 lên 0.98. | Đánh giá lại câu hỏi số 10 trong golden dataset và kiểm tra cả 4 danh mục ngành nghề xuất hiện trọn vẹn trong 1 context duy nhất. |
|        2 | Bổ sung bước tiền xử lý chuẩn hóa ký tự (Text Cleaning & Whitespace Normalization) cho toàn bộ tài liệu chuyển đổi từ PDF scan/OCR. | Ở Worst Performer #1, lỗi ngắt dòng và khoảng trắng kép trong Thông tư 96 làm giảm cosine similarity của Dense search khoảng 15-20%. | Tăng độ tương đồng vector in-domain từ 0.65 lên > 0.78, giúp Dense search thu hồi tài liệu pháp lý tin cậy hơn. | Chạy lại cosine score đo đạc giữa query pháp lý và các chunk đã được chuẩn hóa khoảng trắng. |
|        3 | Tích hợp Cross-Encoder Reranker (như BGE-Reranker hoặc Jina Reranker) sau bước RRF để xếp hạng lại top 15 candidates xuống top 5 trước khi gửi cho LLM. | RRF dựa hoàn toàn trên thứ hạng số nguyên (rank) chứ không phản ánh độ tương quan nội dung câu chữ chi tiết giữa câu hỏi và đoạn văn. | Nâng Context Precision của toàn pipeline lên trên 0.93 và loại bỏ hoàn toàn các chunk phụ không liên quan. | Thực hiện kiểm thử A/B/C: Dense vs Hybrid+RRF vs Hybrid+Cross-Encoder trên toàn bộ 20 câu trong golden dataset. |

## Bonus experiments

| Experiment | Baseline | Metric delta | Latency/cost delta | Conclusion |
| ---------- | -------- | -----------: | -----------------: | ---------- |
| Query Expansion kết hợp Hypothetical Document Embeddings (HyDE) cho các câu hỏi tình huống thực tế phức tạp | Hybrid + RRF (Config B) | Average Score: +0.034 (từ 0.898 lên 0.932); Context Recall đạt 0.94 | Latency tăng từ 110ms lên 385ms (+275ms do thêm 1 lượt gọi LLM tạo giả thuyết); Chi phí token tăng ~25% | Rất hiệu quả cho các câu hỏi tình huống mở, diễn đạt bằng ngôn ngữ đời thường; tuy nhiên với câu hỏi tra cứu trực tiếp theo văn bản luật thì Hybrid + RRF tiêu chuẩn vẫn là giải pháp tối ưu nhất về chi phí và tốc độ. |
