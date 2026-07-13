import streamlit as st
from ai_engine.layer_1_model.gemini import gemini_instance # Chỉnh đường dẫn import chuẩn
from docx import Document
from io import BytesIO
from pypdf import PdfReader

def render_quiz_generator():
    st.subheader("🎯 Trình Tạo Đề Kiểm Tra Tự Động")
    
    # Giao diện
    uploaded_file = st.file_uploader("Tải tài liệu tham khảo:", type=['pdf', 'docx', 'txt'])
    text_content = st.text_area("Nội dung bài giảng/Yêu cầu bổ sung:", height=300)
    
    col1, col2 = st.columns(2)
    with col1:
        num = st.number_input("Số câu:", min_value=1, value=5)
        q_type = st.selectbox("Dạng bài:", ["Trắc nghiệm", "Tự luận", "Trắc nghiệm kết hợp tự luận"])
    with col2:
        use_source = st.checkbox("Bám sát tài liệu", value=True)
        include_digital = st.checkbox("Tích hợp Năng lực số", value=True)
    
    if st.button("🚀 Tạo đề ngay"):
        combined = text_content
        if use_source and uploaded_file:
            # Xử lý đọc file
            if uploaded_file.type == "application/pdf": 
                combined += "\n" + "\n".join([p.extract_text() for p in PdfReader(uploaded_file).pages])
            elif "word" in uploaded_file.type: 
                combined += "\n" + "\n".join([p.text for p in Document(uploaded_file).paragraphs])
        
        if not combined: 
            st.warning("Vui lòng nhập nội dung!")
        else:
            with st.spinner("AI đang soạn đề..."):
                prompt = f"Soạn {num} câu hỏi {q_type}. {'Lồng ghép Năng lực số.' if include_digital else ''} Dựa trên: {combined}."
                
                # GỌI ĐÚNG INSTANCE ĐÃ CẤU HÌNH KEY
                result = gemini_instance.generate_content(prompt)
                
                if result:
                    st.session_state.current_quiz = result
                    st.rerun()
                else:
                    st.error("Không thể kết nối API. Vui lòng kiểm tra lại Key ở Sidebar.")

    # Hiển thị kết quả
    if "current_quiz" in st.session_state:
        st.text_area("Kết quả:", st.session_state.current_quiz, height=300)
        # Nút tải vẫn dùng file word_export.py thầy đã có sẵn trong folder
