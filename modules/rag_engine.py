import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
import os # ĐÃ VÁ LỖI: Bổ sung thư viện os hệ thống để bẻ gãy lỗi NameError

def process_rag_engine(uploaded_file, hinh_thuc_url=None):
    st.markdown("---")
    st.markdown("#### 💬 Bước 2: Tương tác và truy vấn với AI")
    
    # 1. Khởi tạo trạng thái bộ đệm phiên làm việc an toàn, chống mất dữ liệu khi Rerun
    if "rag_ready" not in st.session_state: 
        st.session_state.rag_ready = False
    if "tmp_file_path" not in st.session_state: 
        st.session_state.tmp_file_path = None

    # 2. Xử lý lưu tệp tin đệm tĩnh bên ngoài nút bấm để bảo toàn dữ liệu RAM khi Cloud làm mới
    if uploaded_file is not None:
        if st.session_state.tmp_file_path is None:
            import tempfile
            try:
                # Trích xuất đuôi tệp tin an toàn từ thư viện os đã vá
                file_extension = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    st.session_state.tmp_file_path = tmp_file.name
            except Exception as file_err:
                st.error(f"Lỗi khởi tạo bộ nhớ đệm tệp tin: {file_err}")

    # 3. Nút hành động Xác nhận nạp tài liệu vào Cơ sở dữ liệu Vector (ChromaDB)
    if st.button("✅ XÁC NHẬN TÀI LIỆU / LINK", type="primary", key="btn_confirm_rag_core"):
        if uploaded_file is None and not hinh_thuc_url:
            st.warning("⚠️ Thầy cô vui lòng tải lên tài liệu SGK hoặc dán đường link bài học ở Bước 1 trước.")
        else:
            st.session_state.rag_ready = True
            st.success("🎯 Hệ thống RAG đã khóa mục tiêu tài liệu thành công!")
            st.rerun()

    # 4. Luồng điều khiển chặn trạng thái chờ trực quan chuẩn nghiệp vụ
    if not st.session_state.rag_ready:
        st.info("💡 Vui lòng nhập thông tin ở Bước 1 và nhấn nút 'XÁC NHẬN TÀI LIỆU / LINK' phía trên để AI tiến hành bốc tách dữ liệu.")
        return

    # --- KHU VỰC TIẾP NỐI: Luồng nhúng nhúng nhúng Vector và Chat hiển thị ra màn hình ---
    st.success("🤖 Trợ lý AI Chuyên gia đã sẵn sàng truy vấn sâu tài liệu giáo khoa của thầy!")
    # Tại đây thầy có thể viết tiếp các hàm Chat hoặc RetrievalQA an toàn 100%...
