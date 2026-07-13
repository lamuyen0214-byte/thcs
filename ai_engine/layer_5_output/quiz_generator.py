import streamlit as st
import sys
import os
from docx import Document
from io import BytesIO
from pypdf import PdfReader

# =====================================================================
# CẤU HÌNH ĐƯỜNG DẪN & KẾT NỐI
# =====================================================================
# Đảm bảo có thể import ai_config từ bất kỳ đâu
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = current_dir
while not os.path.exists(os.path.join(root_dir, 'ai_config.py')) and root_dir != os.path.dirname(root_dir):
    root_dir = os.path.dirname(root_dir)

if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from ai_config import get_ai_client
except ImportError:
    st.error("❌ Lỗi cấu trúc: Không tìm thấy 'ai_config.py'.")
    def get_ai_client(): return None

# =====================================================================
# HÀM XỬ LÝ DỮ LIỆU
# =====================================================================
def extract_text_from_file(uploaded_file):
    """Trích xuất văn bản từ file PDF, DOCX hoặc TXT"""
    try:
        if uploaded_file.name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        elif uploaded_file.name.endswith(".docx"):
            doc = Document(uploaded_file)
            return "\n".join(p.text for p in doc.paragraphs)
        elif uploaded_file.name.endswith(".txt"):
            return uploaded_file.getvalue().decode("utf-8", errors="ignore")
    except Exception as e:
        st.error(f"Lỗi đọc file: {e}")
    return ""

# =====================================================================
# GIAO DIỆN CHÍNH
# =====================================================================
def render_quiz_generator():
    st.subheader("🎯 Trình Tạo Đề Kiểm Tra Tự Động")
    
    uploaded_file = st.file_uploader("Tải tài liệu tham khảo (PDF, DOCX, TXT):", type=['pdf', 'docx', 'txt'])
    text_content = st.text_area("Nội dung bài giảng / Yêu cầu cụ thể:", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        num_mcq = st.number_input("Số câu trắc nghiệm:", min_value=0, value=20)
        num_essay = st.number_input("Số câu tự luận:", min_value=0, value=5)
    with col2:
        use_source = st.checkbox("Tuyệt đối bám sát tài liệu", value=True)
        include_digital = st.checkbox("Tích hợp Năng lực số", value=True)
    
    if st.button("🚀 Tạo đề ngay", type="primary", use_container_width=True):
        # 1. Tổng hợp dữ liệu
        combined = extract_text_from_file(uploaded_file) if uploaded_file else ""
        if text_content:
            combined += "\n" + text_content
            
        if not combined.strip():
            st.warning("⚠️ Chưa có dữ liệu đầu vào.")
            return

        # 2. Khởi tạo Client
        client = get_ai_client()
        if client is None:
            st.error("⚠️ Không thể kết nối AI. Kiểm tra API Key.")
            return

        # 3. Thực thi
        with st.spinner("AI đang biên soạn..."):
            prompt = f"""
            Bạn là chuyên gia giáo dục. Hãy soạn đề kiểm tra dựa trên nội dung sau:
            - Số câu trắc nghiệm: {num_mcq}
            - Số câu tự luận: {num_essay}
            - Yêu cầu: {'Bám sát tài liệu cung cấp.' if use_source else 'Tham khảo tài liệu.'}
            - Lồng ghép năng lực số: {'Có' if include_digital else 'Không'}.
            
            Nội dung: {combined}
            """
            
            try:
                # Sử dụng mô hình ổn định gemini-1.5-flash
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=prompt
                )
                
                result = getattr(response, "text", "")
                if result:
                    st.session_state.current_quiz = result
                    st.rerun()
                else:
                    st.error("⚠️ AI không trả về nội dung.")
                    
            except Exception as e:
                st.error(f"❌ Lỗi hệ thống: {str(e)}")

    # 4. Hiển thị kết quả
    if "current_quiz" in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state.current_quiz)
        
        # Logic tải file
        doc = Document()
        doc.add_heading("ĐỀ KIỂM TRA", level=1)
        doc.add_paragraph(st.session_state.current_quiz)
        
        bio = BytesIO()
        doc.save(bio)
        bio.seek(0)
        
        st.download_button(
            label="⬇️ Tải file Word (.docx)",
            data=bio,
            file_name="De_kiem_tra_GDPT2018.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
