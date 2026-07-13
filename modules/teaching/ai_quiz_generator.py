import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
from pypdf import PdfReader # Dùng pypdf thay cho PyPDF2

def get_stable_model():
    priority_list = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    try:
        available_models = {m.name: m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods}
        for name in priority_list:
            if name in available_models: return genai.GenerativeModel(name)
    except:
        return None
    return None

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        return "\n".join([page.extract_text() for page in reader.pages])
    elif "word" in uploaded_file.type:
        doc = Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])
    return uploaded_file.getvalue().decode("utf-8", errors="ignore")

def render_quiz_generator():
    st.subheader("🎯 Trình Tạo Đề Kiểm Tra Tự Động")
    uploaded_file = st.file_uploader("Tải tài liệu tham khảo (PDF, DOCX, TXT):", type=['pdf', 'docx', 'txt'])
    text_content = st.text_area("Nội dung bổ sung:", height=150)
    
    if st.button("🚀 Tạo đề kiểm tra ngay"):
        combined = text_content
        if uploaded_file:
            combined += "\n\n" + extract_text_from_file(uploaded_file)
            
        if not combined:
            st.warning("Vui lòng nhập nội dung.")
        else:
            model = get_stable_model()
            if model:
                response = model.generate_content(f"Soạn đề dựa trên: {combined}")
                st.session_state.current_quiz = response.text
                st.rerun()

    if "current_quiz" in st.session_state:
        st.text_area("Kết quả:", st.session_state.current_quiz, height=300)
