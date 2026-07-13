import streamlit as st
import sys
import os
from docx import Document
from io import BytesIO
from pypdf import PdfReader

# =====================================================================
# THUẬT TOÁN TỰ ĐỘNG DÒ TÌM "TRÁI TIM" HỆ THỐNG (ai_config.py)
# =====================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = current_dir
while not os.path.exists(os.path.join(root_dir, 'ai_config.py')) and root_dir != os.path.dirname(root_dir):
    root_dir = os.path.dirname(root_dir)

if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from ai_config import get_ai_client
except ImportError:
    st.error(f"❌ Kỹ thuật: Mất kết nối đường ống tới ai_config.py tại {root_dir}")
    def get_ai_client(): return None
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
        
        combined = ""
        if uploaded_file:
            if uploaded_file.name.endswith(".pdf"):
                reader = PdfReader(uploaded_file)
                combined += "\n".join(page.extract_text() or "" for page in reader.pages)
            elif uploaded_file.name.endswith(".docx"):
                doc = Document(uploaded_file)
                combined += "\n".join(p.text for p in doc.paragraphs)
            elif uploaded_file.name.endswith(".txt"):
                combined += uploaded_file.getvalue().decode("utf-8", errors="ignore")
                
        if text_content:
            combined += "\n" + text_content
            
        if not combined.strip():
            st.warning("⚠️ Chưa có dữ liệu để tạo đề.")
            return

        # Gọi Client từ Trái tim hệ thống
        client = get_ai_client()
        
        if client is None:
            st.error("⚠️ Gemini Client chưa được khởi tạo. Hãy kiểm tra API Key ở Sidebar!")
            return
            
        if not hasattr(client, 'models'):
            st.error("⚠️ Lỗi cấu trúc SDK. Hãy đảm bảo đã cài đặt 'google-genai'.")
            return

        with st.spinner("AI đang phân tích tài liệu và biên soạn đề..."):
            prompt = f"""
            Bạn là chuyên gia biên soạn đề kiểm tra theo Chương trình GDPT 2018 cấp THCS.

            Yêu cầu bắt buộc:
            {"- Chỉ sử dụng nội dung trong tài liệu." if use_source else "- Căn cứ vào tài liệu, có thể mở rộng kiến thức."}
            - Sinh {num_mcq} câu trắc nghiệm khách quan.
            - Sinh {num_essay} câu tự luận.
            - Trình bày rõ CÂU HỎI, ĐÁP ÁN, HƯỚNG DẪN CHẤM, MA TRẬN ĐỀ THI.
            {"- Chú trọng lồng ghép Năng lực số, AI, Tư duy tính toán." if include_digital else ""}

            Tài liệu tham khảo:
            {combined}
            """
            
            try:
                # GỌI CHUẨN SDK MỚI
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                
                result = getattr(response, "text", "")
                if not result:
                    st.warning("⚠️ AI không trả về nội dung (Có thể bị chặn bởi bộ lọc an toàn).")
                    return
                
                st.session_state.current_quiz = result
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Lỗi hệ thống AI: {str(e)}")

    if "current_quiz" in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state.current_quiz)
        
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
