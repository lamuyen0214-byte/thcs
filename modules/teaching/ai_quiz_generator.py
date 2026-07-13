import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
import random
from pypdf import PdfReader
import time
def get_stable_model():
    """Hàm xoay vòng model để tránh lỗi 429 Quota Exceeded"""
    priority_list = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-flash-latest"]
    random.shuffle(priority_list) # Trộn để tránh dồn tải vào 1 model
    
    try:
        available_models = {m.name: m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods}
        for name in priority_list:
            if name in available_models: return genai.GenerativeModel(name)
            if f"models/{name}" in available_models: return genai.GenerativeModel(f"models/{name}")
        return genai.GenerativeModel(list(available_models.keys())[0])
    except:
        return None

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return "\n".join([page.extract_text() for page in PdfReader(uploaded_file).pages])
    elif "word" in uploaded_file.type:
        return "\n".join([p.text for p in Document(uploaded_file).paragraphs])
    return uploaded_file.getvalue().decode("utf-8", errors="ignore")

def render_quiz_generator():
    st.subheader("🎯 Trình Tạo Đề Kiểm Tra Tự Động")
    
    # Cấu hình đầu vào
    uploaded_file = st.file_uploader("Tải tài liệu tham khảo (PDF, DOCX, TXT):", type=['pdf', 'docx', 'txt'])
    text_content = st.text_area("Nội dung bài giảng/Yêu cầu bổ sung:", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.number_input("Số lượng câu hỏi:", min_value=1, value=5)
        quiz_type = st.selectbox("Hình thức câu hỏi:", ["Trắc nghiệm", "Tự luận", "Trắc nghiệm kết hợp tự luận"])
    with col2:
        use_source = st.checkbox("Bám sát tài liệu tải lên", value=True)
        include_digital_literacy = st.checkbox("Tích hợp Năng lực số (AI, Tư duy tính toán)", value=True)
    
    if st.button("🚀 Tạo đề kiểm tra ngay"):
        combined = text_content
        if use_source and uploaded_file:
            combined += "\n\nNguồn tài liệu:\n" + extract_text_from_file(uploaded_file)
            
        if not combined:
            st.warning("Vui lòng nhập nội dung hoặc tải tài liệu.")
        else:
            with st.spinner("AI đang soạn đề... (Đang xoay vòng model để tránh lỗi Quota)"):
                model = get_stable_model()
                if model:
                    prompt = f"Soạn {num_questions} câu hỏi dạng {quiz_type}. {'Tích hợp tư duy tính toán và năng lực số.' if include_digital_literacy else ''} Dựa trên: {combined}. Trình bày rõ CÂU HỎI và ĐÁP ÁN."
                    try:
                        response = model.generate_content(prompt)
                        st.session_state.current_quiz = response.text
                        st.rerun()
                    except Exception as e:
                        st.error(f"Lỗi kết nối AI: {e}. Vui lòng thử lại sau 1 phút.")

    # Hiển thị kết quả
    if "current_quiz" in st.session_state:
        st.markdown("---")
        st.text_area("Kết quả:", st.session_state.current_quiz, height=300)
        
        # Xuất Word
        doc = Document()
        doc.add_heading('ĐỀ KIỂM TRA', 0)
        doc.add_paragraph(st.session_state.current_quiz)
        bio = BytesIO()
        doc.save(bio)
        
        st.download_button("📥 Tải bộ đề (.docx)", data=bio.getvalue(), file_name="De_kiem_tra.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
