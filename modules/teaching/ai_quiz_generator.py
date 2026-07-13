import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
import time
from pypdf import PdfReader

# Cập nhật hàm để nhận API Key vào và cấu hình nó
def get_stable_model(api_key):
    if not api_key:
        st.error("API Key chưa được cấu hình!")
        return None
    
    try:
        # BƯỚC QUAN TRỌNG: Cấu hình API Key trước khi sử dụng
        genai.configure(api_key=api_key)
        
        priority = ["gemini-1.5-flash", "gemini-2.0-flash-lite", "gemini-flash-latest"]
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        for name in priority:
            if name in available: return genai.GenerativeModel(name)
            
    except Exception as e:
        st.error(f"Lỗi khởi tạo AI: {e}")
        return None
    return None

def render_quiz_generator(api_key): # Truyền API Key từ sidebar vào
    st.subheader("🎯 Trình Tạo Đề Kiểm Tra Tự Động")
    
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
        # Kiểm tra trước khi gọi AI
        model = get_stable_model(api_key)
        if model is None:
            st.error("Không thể kết nối tới AI. Vui lòng kiểm tra lại API Key trong Sidebar.")
            st.stop() # Dừng lại nếu model lỗi, không để crash
            
        combined = text_content
        if use_source and uploaded_file:
            try:
                if uploaded_file.type == "application/pdf": 
                    combined += "\n" + "\n".join([p.extract_text() for p in PdfReader(uploaded_file).pages])
                elif "word" in uploaded_file.type: 
                    combined += "\n" + "\n".join([p.text for p in Document(uploaded_file).paragraphs])
            except Exception as e:
                st.error(f"Lỗi đọc file: {e}")
        
        if not combined: 
            st.warning("Vui lòng nhập nội dung!")
        else:
            with st.spinner("Đang kết nối AI..."):
                prompt = f"Soạn {num} câu hỏi {q_type}. {'Lồng ghép Năng lực số.' if include_digital else ''} Dựa trên: {combined}."
                
                # Gọi model đã khởi tạo thành công
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
