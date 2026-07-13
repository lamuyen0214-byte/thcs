import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
import time
from pypdf import PdfReader

# 1. Ham khoi tao AI an toan
def get_stable_model(api_key):
    if not api_key:
        st.error("API Key chua duoc cau hinh!")
        return None
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        available = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
        
        # Uu tien cac model Flash
        for name in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-lite"]:
            if name in available:
                return genai.GenerativeModel(name)
        
        if available:
            return genai.GenerativeModel(available[0])
            
        st.error("Khong tim thay model AI kha dung.")
        return None
    except Exception as e:
        st.error(f"Loi he thong AI: {e}")
        return None

# 2. Giao dien chuc nang Quiz Generator
def render_quiz_generator(api_key):
    st.subheader("Trinh Tao De Kiem Tra Tu Dong")
    
    # Khu vuc nhap lieu
    uploaded_file = st.file_uploader("Tai tai lieu tham khao (PDF, DOCX, TXT):", type=['pdf', 'docx', 'txt'])
    text_content = st.text_area("Noi dung bai giang / Yeu cau bo sung:", height=300)
    
    col1, col2 = st.columns(2)
    with col1:
        num = st.number_input("So cau:", min_value=1, value=5)
        q_type = st.selectbox("Dang bai:", ["Trac nghiem", "Tu luan", "Trac nghiem ket hop tu luan"])
    with col2:
        use_source = st.checkbox("Bam sat tai lieu", value=True)
        include_digital = st.checkbox("Tich hop Nang luc so", value=True)
    
    if st.button("Tao de ngay"):
        model = get_stable_model(api_key)
        if model is None:
            st.stop()
            
        combined = text_content
        # Doc file neu co
        if use_source and uploaded_file:
            try:
                if uploaded_file.type == "application/pdf": 
                    reader = PdfReader(uploaded_file)
                    combined += "\n" + "\n".join([p.extract_text() for p in reader.pages])
                elif "word" in uploaded_file.type or uploaded_file.name.endswith('.docx'): 
                    doc = Document(uploaded_file)
                    combined += "\n" + "\n".join([p.text for p in doc.paragraphs])
                elif uploaded_file.type == "text/plain":
                    combined += "\n" + uploaded_file.getvalue().decode("utf-8", errors="ignore")
            except Exception as e:
                st.error(f"Loi doc file: {e}")
        
        if not combined: 
            st.warning("Vui long nhap noi dung hoac tai tai lieu!")
        else:
            with st.spinner("AI dang soan de..."):
                prompt = f"Soan {num} cau hoi {q_type}. {'Long ghep Nang luc so.' if include_digital else ''} Dua tren: {combined}."
                
                # Logic thu lai 3 lan neu qua tai
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
                            st.error(f"Loi AI: {e}")
                            break

    # Hien thi ket qua va tai file
    if "current_quiz" in st.session_state:
        st.markdown("---")
        st.text_area("Ket qua:", st.session_state.current_quiz, height=300)
        
        doc = Document()
        doc.add_paragraph(st.session_state.current_quiz)
        bio = BytesIO()
        doc.save(bio)
        st.download_button("Tai bo de (.docx)", data=bio.getvalue(), file_name="De_kiem_tra.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
