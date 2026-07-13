import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
import time
from pypdf import PdfReader

def get_stable_model():
    # Ưu tiên các model cũ hơn hoặc lite để tránh 429
    priority = ["gemini-1.5-flash", "gemini-2.0-flash-lite", "gemini-flash-latest"]
    try:
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for name in priority:
            if name in available: return genai.GenerativeModel(name)
    except: return None
    return None

def render_quiz_generator():
    st.subheader("🎯 Trình Tạo Đề Kiểm Tra Tự Động")
    
    uploaded_file = st.file_uploader("Tải tài liệu tham khảo:", type=['pdf', 'docx', 'txt'])
    # Ô nhập liệu đã kéo dài lên 300px
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
            if uploaded_file.type == "application/pdf": combined += "\n" + "\n".join([p.extract_text() for p in PdfReader(uploaded_file).pages])
            elif "word" in uploaded_file.type: combined += "\n" + "\n".join([p.text for p in Document(uploaded_file).paragraphs])
        
        if not combined: st.warning("Vui lòng nhập nội dung!")
        else:
            with st.spinner("Đang kết nối AI..."):
                model = get_stable_model()
                prompt = f"Soạn {num} câu hỏi {q_type}. {'Lồng ghép Năng lực số.' if include_digital else ''} Dựa trên: {combined}."
                
                # Cơ chế tự thử lại 3 lần nếu lỗi 429
                for i in range(3):
                    try:
                        res = model.generate_content(prompt)
                        st.session_state.current_quiz = res.text
                        st.rerun()
                        break
                    except Exception as e:
                        if "429" in str(e) and i < 2:
                            st.warning(f"AI đang quá tải, chờ 20 giây thử lại (lần {i+1})...")
                            time.sleep(20)
                        else:
                            st.error(f"Lỗi AI: {e}")
                            break

    if "current_quiz" in st.session_state:
        st.text_area("Kết quả:", st.session_state.current_quiz, height=300)
        doc = Document()
        doc.add_paragraph(st.session_state.current_quiz)
        bio = BytesIO()
        doc.save(bio)
        st.download_button("📥 Tải bộ đề (.docx)", data=bio.getvalue(), file_name="De_kiem_tra.docx")
