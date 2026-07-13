import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
import time
from pypdf import PdfReader

# 1. Khởi tạo AI an toàn (Hàm này dùng chung cho toàn dự án)
def get_stable_model(api_key):
    if not api_key:
        st.error("API Key chưa được cấu hình!")
        return None
    try:
        genai.configure(api_key=api_key)
        priority = ["gemini-1.5-flash", "gemini-2.0-flash-lite", "gemini-flash-latest"]
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        for name in priority:
            if name in available_models: 
                return genai.GenerativeModel(name)
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        st.error(f"Lỗi khởi tạo mô hình: {e}")
        return None

# 2. Render giao diện chức năng Quiz Generator (Đúng theo module thcs/modules/teaching/ai_quiz_generator.py)
def render_quiz_generator(api_key):
    st.subheader("Trình Tạo Đề Kiểm Tra Tự Động")
    
    # Khu vực nhập liệu
    uploaded_file = st.file_uploader("Tải tài liệu tham khảo (PDF, DOCX, TXT):", type=['pdf', 'docx', 'txt'])
    text_content = st.text_area("Nội dung bài giảng/Yêu cầu bổ sung:", height=300)
    
    # Cấu hình câu hỏi
    col1, col2 = st.columns(2)
    with col1:
        num = st.number_input("Số câu:", min_value=1, value=5)
        q_type = st.selectbox("Dạng bài:", ["Trắc nghiệm", "Tự luận", "Trắc nghiệm kết hợp tự luận"])
    with col2:
        use_source = st.checkbox("Bám sát tài liệu", value=True)
        include_digital = st.checkbox("Tích hợp Năng lực số", value=True)
    
    # Nút thực thi
    if st.button("Tạo đề ngay"):
        model = get_stable_model(api_key)
        if model is None:
            st.stop()
            
        combined = text_content
        # Đọc file nếu có
        if use_source and uploaded_file:
            try:
                if uploaded_file.type == "application/pdf": 
                    reader = PdfReader(uploaded_file)
                    combined += "\n" + "\n".join([p.extract_text() for p in reader.pages])
                elif "word" in uploaded_file.type or uploaded_file.name.endswith('.docx'): 
                    doc = Document(uploaded_file)
                    combined += "\n" + "\n".join([p.text for p in doc.paragraphs])
                elif uploaded_file.type == "text/plain":
                    combined += "\n" + uploaded_file.getvalue().decode("utf-8")
            except Exception as e:
                st.error(f"Lỗi đọc file: {e}")
        
        if not combined: 
            st.warning("Vui lòng nhập nội dung bài giảng hoặc tải tài liệu lên!")
        else:
            with st.spinner("AI đang soạn đề..."):
                prompt = f"Soạn {num} câu hỏi {q_type}. {'Lồng ghép Năng lực số.' if include_digital else ''} Dựa trên: {combined}."
                
                # Logic thử lại 3 lần nếu quá tải
                for i in range(3):
                    try:
                        res = model.generate_content(prompt)
                        st.session_state.current_quiz = res.text
                        st.rerun()
                        break
                    except Exception as e:
                        if "429" in str(e) and i < 2:
                            time.sleep(20)
                        else:
                            st.error(f"Lỗi AI: {e}")
                            break

    # Hiển thị kết quả và tải file
    if "current_quiz" in st.session_state:
        st.markdown("---")
        st.text_area("Kết quả:", st.session_state.current_quiz, height=300)
        
        doc = Document()
        doc.add_paragraph(st.session_state.current_quiz)
        bio = BytesIO()
        doc.save(bio)
        st.download_button("Tải bộ đề (.docx)", data=bio.getvalue(), file_name="De_kiem_tra.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
