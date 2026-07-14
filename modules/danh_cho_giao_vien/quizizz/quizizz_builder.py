import streamlit as st
import os
import docx
import io
from pypdf import PdfReader
from ai_engine.ai_config import get_api_key
from ai_engine.ai_runner import run_ai_with_fallback

def render_quizizz_module(api_key=""):
    # Tinh chỉnh CSS Giao diện
    st.markdown("""
    <style>
    div[data-testid="stAppViewBlockContainer"], .main .block-container { padding-top: 3.5rem !important; }
    .stButton>button { font-weight: bold; border-radius: 6px; }
    </style>
    """, unsafe_allow_html=True)

    # 1. GIAO DIỆN NHẬP LIỆU (Giữ nguyên)
    col1, col2, col3 = st.columns(3)
    with col1: mon_hoc = st.selectbox("Chọn Môn", ["Ngữ văn", "Toán", "Ngoại ngữ", "Giáo dục công dân", "Lịch sử và Địa lý", "Khoa học tự nhiên", "Vật Lý", "Hóa Học", "Sinh Học", "Công nghệ", "Tin học", "GDĐP", "HĐTN-HN"], index=5, key="qz_mon")
    with col2: lop = st.selectbox("Chọn Lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], index=2, key="qz_lop")
    with col3: thoi_gian_cau = st.selectbox("Thời lượng / Câu", ["30 giây", "45 giây", "60 giây", "2 phút", "3 phút"], index=1, key="qz_tg")

    col_ten, col_file = st.columns([2, 1])
    with col_ten: ten_bai = st.text_input("Chủ đề Quizizz / Tên bài học", placeholder="Ví dụ: Bài 4: Tốc độ chuyển động")
    with col_file: tai_lieu_file = st.file_uploader("Tải tài liệu tham chiếu (PDF/Docx)", type=['docx', 'pdf'])
    
    yeu_cau_khac = st.text_area("Yêu cầu chi tiết", placeholder="Ví dụ: Các câu hỏi điền khuyết phải gắn với công thức...", height=70)

    # 2. CẤU HÌNH CÂU HỎI
    with st.expander("Cấu hình Cơ cấu Dạng câu hỏi", expanded=True):
        ct1, ct2, ct3, ct4 = st.columns(4)
        sl_mcq = ct1.number_input("1 Đáp án (MCQ)", value=10, key="qz_mcq")
        sl_multi = ct2.number_input("Nhiều ĐA (Checkbox)", value=2, key="qz_multi")
        sl_dien = ct3.number_input("Điền khuyết", value=2, key="qz_dien")
        sl_ghep = ct4.number_input("Ghép đôi", value=2, key="qz_ghep")

    # 3. KHỞI TẠO AI
    if st.button("TỰ ĐỘNG SINH NGÂN HÀNG QUIZIZZ", type="primary", use_container_width=True):
        if not ten_bai.strip(): st.warning("Vui lòng nhập Chủ đề!"); st.stop()
        
        file_context = ""
        if tai_lieu_file:
            try:
                if tai_lieu_file.name.endswith('.pdf'):
                    reader = PdfReader(tai_lieu_file)
                    file_context = "\n".join([p.extract_text() for p in reader.pages[:10]])
                elif tai_lieu_file.name.endswith('.docx'):
                    doc = docx.Document(tai_lieu_file)
                    file_context = "\n".join([p.text for p in doc.paragraphs])
            except Exception as e: st.error(f"Lỗi đọc file: {e}")

        prompt = f"Soạn Quizizz môn {mon_hoc} {lop}. Chủ đề: {ten_bai}. Yêu cầu: {yeu_cau_khac}. Tạo đúng các dạng: {sl_mcq} MCQ, {sl_multi} Checkbox, {sl_dien} Điền khuyết, {sl_ghep} Ghép đôi. Dưới mỗi câu phải có ĐÁP ÁN và GIẢI THÍCH."
        
        with st.spinner("AI đang thiết kế..."):
            result = run_ai_with_fallback(prompt=prompt, api_key=api_key, model_mode="flash")
            if result.get("success"):
                st.session_state['current_quizizz_data'] = {"title": ten_bai, "content": result.get("text")}
                st.rerun()
            else: st.error(f"Lỗi: {result.get('error')}")

    # 4. XUẤT FILE WORD (ĐÃ FIX: DÙNG HÀM RIÊNG KHÔNG DÙNG WORDEXPORTENGINE GÂY LỖI)
    if 'current_quizizz_data' in st.session_state:
        st.markdown("---")
        with st.expander("Xem trước & Tải về", expanded=True):
            st.markdown(st.session_state['current_quizizz_data']['content'])
            
            # Hàm xuất file Word riêng cho Quizizz
            def export_quizizz_to_word(data):
                doc = docx.Document()
                doc.add_heading(data['title'], 0)
                doc.add_paragraph(data['content'])
                buffer = io.BytesIO()
                doc.save(buffer)
                buffer.seek(0)
                return buffer

            if st.button("📥 Tải bản in Word chuẩn", use_container_width=True):
                word_file = export_quizizz_to_word(st.session_state['current_quizizz_data'])
                st.download_button("Xác nhận Tải về", data=word_file, file_name=f"Quizizz_{ten_bai.replace(' ', '_')}.docx", use_container_width=True)
