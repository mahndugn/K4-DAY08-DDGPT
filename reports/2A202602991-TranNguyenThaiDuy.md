# Individual contribution report — Trần Nguyễn Thái Duy

## Thông tin

- Họ và tên: Trần Nguyễn Thái Duy
- Mã học viên: 2A202602991
- Nhóm: K4-DAY08-DDGPT (Nhóm Thuế Doanh nghiệp)
- Repository/branch: `main` / `ThaiDuy_TV4`

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Streamlit UI Setup | Thiết lập giao diện ứng dụng Streamlit với cấu hình `layout="wide"`, thanh sidebar tùy chỉnh tham số `top_k`, hiển thị thông tin đề tài Thuế Doanh nghiệp | `app.py` | Done |
| Pipeline Integration | Tích hợp trực tiếp hàm `generate_with_citation()` từ `src.task10_generation` vào luồng chat xử lý câu hỏi của người dùng | `app.py` | Done |
| Citation & Metadata Display | Thiết kế thành phần hiển thị danh sách trích dẫn nguồn (`sources`) dạng expander, hiển thị huy hiệu phương thức tìm kiếm (`hybrid`/`dense`/`bm25`), điểm số tương quan (`score`) và đoạn trích dẫn | `app.py` | Done |
| Chat History Management | Quản lý trạng thái phiên làm việc (`st.session_state.messages`), lưu trữ câu trả lời kèm siêu dữ liệu nguồn trích dẫn để không bị mất khi tương tác lại | `app.py` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Sử dụng `st.expander` để gom nhóm các nguồn tài liệu tham chiếu (`sources`) đặt ngay bên dưới mỗi câu trả lời của trợ lý thay vì in dàn trải ra màn hình chính.  
   **Lý do/evidence:** Trong nghiệp vụ tư vấn thuế, câu trả lời pháp lý cần sự rõ ràng, mạch lạc trước tiên; việc gom các đoạn trích dẫn và điểm tương đồng vào khối có thể đóng/mở giúp người dùng đọc câu trả lời nhanh chóng nhưng vẫn dễ dàng bấm xem chi tiết từng trích đoạn khi cần đối soát số hiệu điều luật.  
   **Trade-off:** Người dùng cần thực hiện thêm thao tác bấm mở rộng nếu muốn xem ngay toàn bộ nội dung chunk gốc.

2. **Quyết định:** Bổ sung thanh trượt `top_k` trong sidebar cho phép người dùng tùy chỉnh số lượng đoạn tài liệu tham khảo từ 3 đến 10.  
   **Lý do/evidence:** Cho phép người dùng linh hoạt điều chỉnh: với câu hỏi ngắn, đơn giản chỉ cần `top_k=3` để tăng tốc độ phản hồi; với câu hỏi tổng hợp đa chính sách có thể tăng lên `top_k=8` để bao quát nhiều văn bản luật khác nhau.  
   **Trade-off:** Khi người dùng chọn `top_k` quá lớn (8-10), thời gian xử lý của LLM và chi phí token sẽ tăng lên tương ứng.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng:
  + Chạy ứng dụng nội bộ: `streamlit run app.py`
  + Thử nghiệm các câu hỏi tra cứu: *"Thuế suất thuế TNDN đối với doanh nghiệp nhỏ là bao nhiêu?"*, *"Xử lý hóa đơn viết sai tiền"*
- Kết quả trước/sau nếu có:
  + Trước: Ứng dụng chỉ có giao diện khung với câu trả lời giả lập "TODO: Itegration RAG Pipeline hêre".
  + Sau: Giao diện hiển thị trực quan, câu trả lời tiếng Việt hoàn chỉnh, danh sách nguồn hiển thị rõ tên văn bản pháp luật, phương thức truy xuất và điểm số tin cậy.
- Lỗi đã phát hiện và cách xử lý:
  + Lỗi khi reload trang làm mất danh sách nguồn trích dẫn của các câu chat cũ. Đã xử lý bằng cách lưu cả trường `sources` và `retrieval_source` vào từ điển tin nhắn trong `st.session_state.messages`.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Chưa triển khai tính năng highlight tô màu các câu trích dẫn trực tiếp trong đoạn văn bản nguồn khi người dùng bấm vào mã citation.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Xây dựng cơ chế liên kết động (clickable anchor) giữa ký hiệu citation trong văn bản (ví dụ `[chunk-12]`) và thẻ tài liệu tương ứng bên dưới.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 2026-09-21
- Tên thành viên: Trần Nguyễn Thái Duy
