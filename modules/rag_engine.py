import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader # Hoặc PyPDFLoader nếu dùng PDF

def process_rag_engine(uploaded_file, hinh_thuc_url=None):
    st.markdown("---")
    st.markdown("#### 💬 Bước 2: Tương tác và truy vấn với AI")
    
    # Khởi tạo trạng thái nếu chưa có
    if "rag_ready" not in st.session_state: st.session_state.rag_ready = False
    if "tmp_file_path" not in st.session_state: st.session_state.tmp_file_path = None

    # Nút xác nhận để kích hoạt hệ thống
    if st.button("✅ XÁC NHẬN TÀI LIỆU / LINK", type="primary"):
        st.session_state.rag_ready = True
        # Xử lý file nếu có
        if uploaded_file:
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                st.session_state.tmp_file_path = tmp_file.name
        else:
            st.session_state.tmp_file_path = None
        st.rerun()

    # Chỉ chạy chat khi đã xác nhận
    if not st.session_state.rag_ready:
        st.info("💡 Vui lòng nhập thông tin ở Bước 1 và nhấn nút 'XÁC NHẬN' phía trên để bắt đầu.")
        return
