import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
from pypdf import PdfReader

def get_stable_model():
    priority_list = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    try:
        available_models = {m.name: m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods}
        for name in priority_list:
            if name in available_models: return genai.GenerativeModel(name)
            if f"models/{name}" in available_models: return genai.GenerativeModel(f"models/{name}")
    except: return None
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
    
    # Upload và tùy chỉnh
    uploaded_file = st.file_uploader("Tải tài liệu tham khảo (PDF, DOCX, TXT):", type=['pdf', 'docx', 'txt'])
    
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.number_input("Số lượng câu hỏi:", min_value=1, value=5)
        quiz_type = st.selectbox("Hình thức câu hỏi:", ["Trắc nghiệm", "Tự luận", "Trắc nghiệm kết hợp tự luận"])
    with col2:
        use_source = st.checkbox("Bám sát nội dung tài liệu tải lên", value=True)
        include_digital_literacy = st.checkbox("Tích hợp năng lực số (AI, Tư duy tính toán)", value=True)
        
    text_content = st.text_area("Nội dung bổ sung / Yêu cầu cụ thể:", height=150)
    
    if st.button("🚀 Tạo đề kiểm tra ngay"):
        combined = text_content
        if use_source and uploaded_file:
            with st.spinner("Đang đọc tài liệu..."):
                combined += "\n\nNguồn tham khảo:\n" + extract_text_from_file(uploaded_file)
        
        if not combined:
            st.warning("Vui lòng nhập nội dung hoặc tải tài liệu.")
        else:
            with st.spinner("AI đang soạn đề..."):
                model = get_stable_model()
                prompt = f"""
                Soạn {num_questions} câu hỏi dạng {quiz_type}.
                {'Tích hợp thêm các nội dung về Năng lực số (AI, Tư duy tính toán) vào câu hỏi.' if include_digital_literacy else ''}
                Dựa trên nguồn dữ liệu: {combined}
                Trình bày rõ ràng phần CÂU HỎI và ĐÁP ÁN.
                """
                if model:
                    response = model.generate_content(prompt)
                    st.session_state.current_quiz = response.text
                    st.rerun()

    if "current_quiz" in st.session_state:
        st.markdown("---")
        st.text_area("Kết quả:", st.session_state.current_quiz, height=300)
        # Nút tải Word giữ nguyên như code trước thầy đã có
