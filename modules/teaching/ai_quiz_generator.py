import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
import time
from pypdf import PdfReader

def get_stable_model():
    priority = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    try:
        available = {m.name: m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods}
        for name in priority:
            if name in available: return genai.GenerativeModel(name)
    except: return None
    return None

def render_quiz_generator():
    st.subheader("🎯 Trình Tạo Đề Kiểm Tra Tự Động")
    
    uploaded_file = st.file_uploader("Tải tài liệu tham khảo:", type=['pdf', 'docx', 'txt'])
    text_content = st.text_area("Nội dung bổ sung:", height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        num = st.number_input("Số câu:", min_value=1, value=5)
    with col2:
        q_type = st.selectbox("Dạng bài:", ["Trắc nghiệm", "Tự luận"])
    
    if st.button("🚀 Tạo đề"):
        combined = text_content
        if uploaded_file:
            # Đọc nhanh file
            if uploaded_file.type == "application/pdf": combined += "\n" + "\n".join([p.extract_text() for p in PdfReader(uploaded_file).pages])
            elif "word" in uploaded_file.type: combined += "\n" + "\n".join([p.text for p in Document(uploaded_file).paragraphs])
        
        if not combined:
            st.warning("Vui lòng nhập nội dung!")
        else:
            with st.spinner("Đang soạn đề..."):
                model = get_stable_model()
                prompt = f"Soạn {num} câu hỏi {q_type} dựa trên: {combined}. Chỉ trả về CÂU HỎI và ĐÁP ÁN."
                try:
                    res = model.generate_content(prompt)
                    st.session_state.current_quiz = res.text
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi: {e}")

    if "current_quiz" in st.session_state:
        st.text_area("Kết quả:", st.session_state.current_quiz, height=300)
        doc = Document()
        doc.add_paragraph(st.session_state.current_quiz)
        bio = BytesIO()
        doc.save(bio)
        st.download_button("📥 Tải Word", data=bio.getvalue(), file_name="De_thi.docx")
