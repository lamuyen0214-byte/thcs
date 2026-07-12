import streamlit as st
from modules.rag_engine import process_rag_engine

def render_module():
    st.markdown("## 📚 Hỗ trợ Giảng dạy")
    tabs = st.tabs(["Hỏi-Đáp (RAG)", "Trò chơi", "Chấm bài"])
    
    with tabs[0]: # Tab RAG
        uploaded_file = st.file_uploader("Tải tài liệu giảng dạy:", type=['txt', 'pdf'])
        query = st.text_input("Nhập câu hỏi của thầy:")
        
        if st.button("Phân tích tài liệu"):
            with st.spinner("Đang truy xuất..."):
                result = process_rag_engine(uploaded_file, query)
                st.write(result)
                
    with tabs[1]: # Tab Trò chơi
        st.write("Chức năng tạo trò chơi...")
