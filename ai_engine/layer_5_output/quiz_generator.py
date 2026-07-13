import streamlit as st
from ai_config import get_ai_client # Lấy client từ file cấu hình chuẩn
from docx import Document
from io import BytesIO
from pypdf import PdfReader

def render_quiz_generator():
    st.subheader("🎯 Trình Tạo Đề Kiểm Tra Tự Động")
    
    # ... (giữ nguyên phần upload file và input) ...

    if st.button("🚀 Tạo đề ngay"):
        # ... (xử lý nội dung combined) ...
        
        # 1. LẤY CLIENT CHUẨN TỪ BỘ ĐIỀU PHỐI
        client = get_ai_client()
        if not client:
            st.error("⚠️ Gemini Client chưa được khởi tạo. Hãy kiểm tra API Key ở Sidebar!")
            return

        with st.spinner("AI đang soạn đề..."):
            prompt = f"Soạn đề dựa trên: {combined}"
            
            try:
                # 2. GỌI DÙNG CÚ PHÁP CỦA SDK MỚI (google.genai.Client)
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=prompt
                )
                st.session_state.current_quiz = response.text
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi hệ thống AI: {str(e)}")

    # Hiển thị kết quả
    if "current_quiz" in st.session_state:
        st.markdown("---")
        st.text_area("Kết quả:", st.session_state.current_quiz, height=300)
