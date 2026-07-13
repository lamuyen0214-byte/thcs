import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
from pypdf import PdfReader

def get_stable_model():
    priority = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    try:
        # Lấy danh sách model từ client đã khởi tạo ở app.py
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for name in priority:
            if name in available: return genai.GenerativeModel(name)
            if f"models/{name}" in available: return genai.GenerativeModel(f"models/{name}")
        return genai.GenerativeModel(available[0]) if available else None
    except: return None

def render_quiz_generator():
    st.subheader("🎯 Trình Tạo Đề Kiểm Tra Tự Động")
    
    uploaded_file = st.file_uploader("Tải tài liệu tham khảo (PDF, DOCX, TXT):", type=['pdf', 'docx', 'txt'])
    text_content = st.text_area("Nội dung bài giảng/Yêu cầu bổ sung:", height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        num = st.number_input("Số câu:", min_value=1, value=5)
        q_type = st.selectbox("Dạng bài:", ["Trắc nghiệm", "Tự luận", "Trắc nghiệm kết hợp tự luận"])
    with col2:
        use_source = st.checkbox("Bám sát tài liệu tải lên", value=True)
        include_digital = st.checkbox("Tích hợp Năng lực số (AI, Tư duy tính toán)", value=True)
    
    if st.button("🚀 Tạo đề"):
        combined = text_content
        if use_source and uploaded_file:
            if uploaded_file.type == "application/pdf": combined += "\n" + "\n".join([p.extract_text() for p in PdfReader(uploaded_file).pages])
            elif "word" in uploaded_file.type: combined += "\n" + "\n".join([p.text for p in Document(uploaded_file).paragraphs])
            else: combined += "\n" + uploaded_file.getvalue().decode("utf-8", errors="ignore")
        
        if not combined: st.warning("Vui lòng nhập nội dung hoặc tải tài liệu!")
        else:
            with st.spinner("AI đang soạn đề..."):
                model = get_stable_model()
                if model:
                    prompt = f"Soạn {num} câu hỏi {q_type}. {'Hãy lồng ghép Năng lực số (AI, Tư duy tính toán).' if include_digital else ''} Dựa trên nội dung: {combined}."
                    try:
                        res = model.generate_content(prompt)
                        st.session_state.current_quiz = res.text
                        st.rerun()
                    except Exception as e: st.error(f"Lỗi AI: {e}")
                else: st.error("Không tìm thấy Model khả dụng. Vui lòng kiểm tra API Key!")

    if "current_quiz" in st.session_state:
        st.text_area("Kết quả:", st.session_state.current_quiz, height=300)
        doc = Document()
        doc.add_paragraph(st.session_state.current_quiz)
        bio = BytesIO()
        doc.save(bio)
        st.download_button("📥 Tải bộ đề (.docx)", data=bio.getvalue(), file_name="De_kiem_tra.docx")
