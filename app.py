import streamlit as st
from dotenv import load_dotenv

from src.task10_generation import generate_with_citation

load_dotenv()

st.set_page_config(
    page_title="RAG Tra cứu Thuế & Tài chính Doanh nghiệp",
    page_icon="⚖️",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state.messages = []


def render_sources(sources: list[dict], retrieval_source: str = "none") -> None:
    """Hiển thị nguồn tham khảo, retrieval method và score cho từng chunk."""
    if not sources:
        return

    method_badge = {
        "hybrid": "🔀 Hybrid (Dense + BM25 RRF)",
        "dense": "🧠 Dense Semantic Search",
        "bm25": "🔤 BM25 Lexical Search",
        "pageindex": "📄 PageIndex Vectorless Fallback",
        "none": "🚫 Không có nguồn",
    }.get(retrieval_source, retrieval_source)

    st.caption(f"**Phương thức truy xuất:** `{method_badge}` | **Số chunks:** `{len(sources)}`")

    with st.expander(f"📚 Xem chi tiết {len(sources)} nguồn trích dẫn & điểm số"):
        for index, chunk in enumerate(sources, 1):
            metadata = chunk.get("metadata", {})
            chunk_id = chunk.get("id", f"chunk-{index}")
            score = chunk.get("score", 0.0)
            method = chunk.get("retrieval_method", retrieval_source)
            title = metadata.get("title", "Không có tiêu đề")
            source_file = metadata.get("source", "N/A")
            doc_type = metadata.get("doc_type", "N/A")

            st.markdown(
                f"**[{index}] Chunk ID:** `{chunk_id}`  \n"
                f"- **Tài liệu:** `{source_file}` ({doc_type})  \n"
                f"- **Tiêu đề:** {title}  \n"
                f"- **Phương thức:** `{method}` | **Score:** `{score:.4f}`"
            )
            st.text_area(
                label=f"Nội dung trích đoạn ({chunk_id})",
                value=chunk.get("content", ""),
                height=120,
                key=f"chunk_view_{chunk_id}_{index}_{id(chunk)}",
                disabled=True,
            )
            st.divider()


# Sidebar cấu hình
with st.sidebar:
    st.title("⚙️ Cấu hình RAG")
    st.markdown(
        "Hệ thống RAG tra cứu văn bản pháp luật, thuế doanh nghiệp và tin tức kinh tế."
    )
    top_k = st.slider("Số lượng chunks (top_k)", min_value=1, max_value=10, value=5)

    if st.button("🗑️ Xóa lịch sử hội thoại"):
        st.session_state.messages = []
        st.rerun()

st.title("⚖️ Trợ lý Pháp luật & Thuế Doanh nghiệp")
st.caption(
    "Hệ thống trả lời dựa trên văn bản pháp quy (Nghị định 123, 126, 91, Thông tư 78, 96...) "
    "và tin tức kinh tế với đầy đủ citation truy vết và cơ chế từ chối an toàn khi ngoài phạm vi."
)

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("sources"):
            render_sources(
                message["sources"],
                retrieval_source=message.get("retrieval_source", "none"),
            )

query = st.chat_input("Nhập câu hỏi về thuế, hóa đơn hoặc chính sách tài chính...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Đang truy xuất tài liệu và tạo câu trả lời có trích dẫn..."):
            result = generate_with_citation(query, top_k=top_k)
            answer = result.get("answer", "Tôi không thể xác minh thông tin này từ nguồn hiện có.")
            sources = result.get("sources", [])
            retrieval_source = result.get("retrieval_source", "none")

            st.markdown(answer)
            if sources:
                render_sources(sources, retrieval_source=retrieval_source)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "retrieval_source": retrieval_source,
    })
