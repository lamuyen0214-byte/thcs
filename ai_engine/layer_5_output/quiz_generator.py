import streamlit as st
from ai_engine.layer_1_model.gemini import gemini_instance 
from docx import Document
from io import BytesIO
from pypdf import PdfReader

# BỘ ĐIỀU KHIỂN ĐỊNH TUYẾN CHUẨN
def route_generate_request(prompt, system_instruction=None):
    """
    Hàm định tuyến duy nhất: Mọi chức năng chỉ gọi hàm này.
    Không khởi tạo model thủ công ở module con.
    """
    if not hasattr(gemini_instance, 'generate_content'):
        st.error("Lỗi hệ thống: Gemini Engine chưa được khởi tạo đúng cách.")
        return None
    
    # Chuyển hướng yêu cầu tới instance duy nhất
    return gemini_instance.generate_content(prompt, system_instruction=system_instruction)

def render_quiz_generator():
    st.subheader("🎯 Trình Tạo Đề Kiểm Tra Tự Động")
    
    uploaded_file = st.file_uploader("Tải tài liệu tham khảo:", type=['pdf', 'docx', 'txt'])
    text_content = st.text_area("Nội dung bài giảng:", height=200)
    
    col1, col2 = st.columns(2)
    with col1:
        num = st.number_input("Số câu:", min_value=1, value=5)
        q_type = st.selectbox("Dạng bài:", ["Trắc nghiệm", "Tự luận", "Trắc nghiệm kết hợp tự luận"])
    with col2:
        use_source = st.checkbox("Bám sát tài liệu", value=True)
        include_digital = st.checkbox("Tích hợp Năng lực số", value=True)
    
    if st.button("🚀 Tạo đề"):
        combined = text_content
        if use_source and uploaded_file:
            # Xử lý nội dung tập trung
            if uploaded_file.type == "application/pdf": 
                combined += "\n" + "\n".join([p.extract_text() for p in PdfReader(uploaded_file).pages])
            elif "word" in uploaded_file.type: 
                combined += "\n" + "\n".join([p.text for p in Document(uploaded_file).paragraphs])
        
        if not combined: 
            st.warning("Vui lòng nhập nội dung!")
        else:
            with st.spinner("AI đang xử lý qua bộ điều khiển..."):
                prompt = f"Soạn {num} câu hỏi {q_type}. {'Lồng ghép Năng lực số.' if include_digital else ''} Dựa trên: {combined}."
                
                # GỌI QUA BỘ ĐỊNH TUYẾN
                result = route_generate_request(prompt)
                
                if result:
                    st.session_state.current_quiz = result
                    st.rerun()
                else:
                    st.error("Lỗi: Không nhận được phản hồi từ AI. Hãy kiểm tra lại API Key ở Sidebar.")
