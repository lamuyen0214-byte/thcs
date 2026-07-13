import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
import PyPDF2 # Cần cài đặt: pip install PyPDF2

# Hàm đọc nội dung từ file
def extract_text_from_file(uploaded_file):
    text = ""
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        text = uploaded_file.getvalue().decode("utf-8")
    return text

def render_quiz_generator():
    st.subheader("🎯 Trình Tạo Đề Kiểm Tra Tự Động")
    
    # 1. Thêm chức năng tải tài liệu
    uploaded_file = st.file_uploader("Tải lên đề cương/tài liệu tham khảo (PDF, DOCX, TXT):", type=['pdf', 'docx', 'txt'])
    
    # 2. Ô nhập văn bản bổ sung
    text_content = st.text_area("Hoặc nhập nội dung bổ sung/yêu cầu cụ thể cho AI:", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.number_input("Số lượng câu hỏi:", min_value=1, value=5)
    with col2:
        quiz_type = st.selectbox("Dạng bài:", ["Trắc nghiệm", "Tự luận", "Trắc nghiệm & Tự luận"])
    
    if st.button("🚀 Tạo đề kiểm tra ngay"):
        # Kết hợp nội dung từ file và từ ô nhập text
        combined_content = text_content
        if uploaded_file:
            with st.spinner("Đang đọc tài liệu..."):
                combined_content += "\n\nNội dung từ tài liệu:\n" + extract_text_from_file(uploaded_file)
        
        if not combined_content:
            st.warning("Vui lòng tải file hoặc nhập nội dung.")
        else:
            with st.spinner("AI đang soạn đề bám sát tài liệu..."):
                # Gọi model (giữ nguyên hàm get_stable_model của thầy)
                model = get_stable_model()
                prompt = f"Dựa trên nội dung sau: {combined_content}. Hãy soạn {num_questions} câu hỏi {quiz_type}."
                response = model.generate_content(prompt)
                st.session_state.current_quiz = response.text
                st.rerun()

    # (Phần hiển thị kết quả và xuất Word giữ nguyên như cũ)
