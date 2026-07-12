import streamlit as st
import os  # Đã sửa lỗi: Import đầy đủ os
import tempfile
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader, PyPDFLoader

def process_rag_engine(uploaded_file, hinh_thuc_url=None):
    st.markdown("---")
    
    # 1. Khởi tạo trạng thái an toàn (Tránh đứng hình)
    if "rag_ready" not in st.session_state: st.session_state.rag_ready = False
    if "tmp_file_path" not in st.session_state: st.session_state.tmp_file_path = None

    # 2. Xử lý logic nút bấm an toàn
    if st.button("✅ XÁC NHẬN TÀI LIỆU", type="primary"):
        if uploaded_file:
            # Tạo file tạm và xóa file cũ nếu có để tránh kẹt RAM
            if st.session_state.tmp_file_path and os.path.exists(st.session_state.tmp_file_path):
                os.remove(st.session_state.tmp_file_path)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                tmp.write(uploaded_file.getvalue())
                st.session_state.tmp_file_path = tmp.name
            st.session_state.rag_ready = True
            st.rerun() # Chỉ rerun khi đã có dữ liệu hợp lệ
        else:
            st.warning("Vui lòng tải lên tài liệu trước khi xác nhận.")

    # 3. Luồng RAG xử lý thông minh (Tiết kiệm RAM)
    if st.session_state.rag_ready and st.session_state.tmp_file_path:
        st.success("Tài liệu đã sẵn sàng để truy vấn.")
        
        # Sử dụng API Key từ session
        api_key = st.session_state.get("user_gemini_key")
        
        try:
            # Chọn Loader tự động dựa trên đuôi file
            loader = PyPDFLoader(st.session_state.tmp_file_path) if st.session_state.tmp_file_path.endswith('.pdf') else TextLoader(st.session_state.tmp_file_path)
            documents = loader.load()
            
            # Cấu hình Vector Store gọn nhẹ (Giảm chunk_size nếu file lớn để tránh lỗi RAM Cloud)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            texts = text_splitter.split_documents(documents)
            
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
            vectorstore = Chroma.from_documents(texts, embeddings, collection_name="local_rag_store")
            
            # Khởi tạo Chain
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
            qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())

            # Chat Interface
            prompt = st.chat_input("Nhập câu hỏi về tài liệu...")
            if prompt:
                with st.chat_message("user"): st.markdown(prompt)
                with st.chat_message("assistant"):
                    response = qa_chain.invoke({"query": prompt})
                    st.markdown(response["result"])
                    
        except Exception as e:
            st.error(f"Lỗi hệ thống: {e}")
            # Reset nếu lỗi để tránh kẹt
            if st.button("🔄 Reset lại hệ thống"):
                st.session_state.rag_ready = False
                st.rerun()
