# Thành viên nhóm — Đề tài: Chính sách Pháp luật & Thuế Doanh nghiệp tại Việt Nam

> Thông tin chính xác của các thành viên trong nhóm thực hiện dự án RAG Pipeline (Day 8).

| Họ và tên | Mã học viên | Vai trò | Trọng tâm phụ trách | File / Module chính | Nhánh thực hiện |
| --- | --- | --- | --- | --- | --- |
| **Phạm Thành Trung** | 2A202602949 | TV 1 | Chunking, Embedding, Vector DB, Dense Search | `src/task4_chunking_indexing.py`, `src/task5_semantic_search.py` | `Trung` (PR #5) |
| **Nguyễn Hồng Phi** | 2A202602750 | TV 2 | BM25 Lexical Search, RRF Fusion, Fallback & Pipeline | `src/task6_lexical_search.py`, `src/task7_reranking.py`, `src/task8_pageindex_vectorless.py`, `src/task9_retrieval_pipeline.py` | `main` / `HongPhi` |
| **Từ Hoàng Giang** | 2A202602363 | TV 3 | Generation, Citation, Reordering, Safe Refusal | `src/task10_generation.py` | `TuHoangGiang_2A202602363` (PR #6) |
| **Trần Nguyễn Thái Duy** | 2A202602991 | TV 4 | Streamlit Chatbot UI, Display Citation & Interactive App | `app.py` | `ThaiDuy_TV4` / `main` |
| **Đinh Mạnh Dũng** | 2A202602975 | TV 5 (Leader) | Thu thập & Chuẩn hóa Corpus, Golden Dataset, A/B Testing, RESULT.md | `src/task1_collect_legal_docs.py`, `src/task2_crawl_news.py`, `src/task3_convert_markdown.py`, `golden_dataset.json`, `RESULT.md` | `main` / `mahndugn` |

## Phân công chi tiết và Điểm Rubric tương ứng

| Thành viên | Trọng tâm phụ trách | File chính | Điểm Rubric liên quan | Điểm Bonus tiềm năng |
| --- | --- | --- | --- | --- |
| **TV 1 (Phạm Thành Trung)** | Chunking, Embedding, Vector DB, Dense Search | `src/task4_chunking_indexing.py`, `src/task5_semantic_search.py` | 20 điểm (Chunking + Dense) | Tối ưu Embedding model |
| **TV 2 (Nguyễn Hồng Phi)** | BM25 Lexical, RRF Fusion, Fallback Pipeline | `src/task6_lexical_search.py`, `src/task7_reranking.py`, `src/task8_pageindex_vectorless.py`, `src/task9_retrieval_pipeline.py` | 30 điểm (BM25, RRF + Pipeline) | +3đ (Jina/BGE Reranker) |
| **TV 3 (Từ Hoàng Giang)** | Generation, Citation, Reordering, Safe Refusal | `src/task10_generation.py` | 15 điểm (Generation & Citation) | +3đ (HyDE / Expansion) |
| **TV 4 (Trần Nguyễn Thái Duy)** | Streamlit Chatbot UI, Display Citation & App | `app.py` | 10 điểm (Chatbot end-to-end) | +2đ (Memory), +2đ (Deploy/Highlight) |
| **TV 5 (Đinh Mạnh Dũng)** | Data Collection, Markdown, Golden Dataset, 4 Metrics, RESULT.md | `task1`, `task2`, `task3`, `golden_dataset.json`, `RESULT.md` | 25 điểm (Data 10đ + Dataset & A/B 15đ) | Thiết kế benchmark chuyên sâu |
