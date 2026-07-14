import streamlit as st
import os
import docx
from pypdf import PdfReader
from export.export_word import WordExportEngine
from ai_engine.ai_config import get_api_key
from ai_engine.ai_runner import run_ai_with_fallback

def render_mophong_module(api_key=""):
    # Tinh chỉnh CSS đồng bộ
    st.markdown("""
    <style>
    div[data-testid="stAppViewBlockContainer"], .main .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 3rem !important;
    }
    .stSelectbox label p, .stTextInput label p, .stNumberInput label p, .stFileUploader label p, .stTextArea label p {
        color: #0000FF !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    .stMarkdown p strong {
        color: #FF0000 !important;
        font-size: 15px !important;
    }
    .stButton>button { font-weight: bold; border-radius: 6px; }
    </style>
    """, unsafe_allow_html=True)

    # 1. GIAO DIỆN NHẬP LIỆU (Đã thêm Môn học cùng hàng với Lớp)
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1: 
        lop = st.selectbox("Chọn Lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], index=0)
    with col2: 
        mon_hoc = st.selectbox("Chọn Môn", ["KHTN", "Vật Lý", "Hóa Học", "Sinh Học", "Tin học", "Công nghệ"], index=0)
    with col3: 
        chu_de = st.text_input("Chủ đề thí nghiệm / Hiện tượng", placeholder="Ví dụ: Phản ứng hóa học, Sự rơi tự do...")

    loai_mo_phong = st.selectbox("Loại kịch bản thực hành", ["Thí nghiệm ảo (từng bước)", "Quy trình an toàn phòng lab", "Giải thích hiện tượng KHTN", "Thiết kế dụng cụ STEM"])
    file_tl = st.file_uploader("Tải quy trình/tài liệu hướng dẫn (nếu có)", type=['docx', 'pdf'])
    yeu_cau = st.text_area("Yêu cầu sư phạm bổ sung", placeholder="Ví dụ: Tập trung vào tính an toàn, yêu cầu học sinh thảo luận nhóm...", height=70)

    # 2. KHỞI TẠO AI
    if st.button("TỰ ĐỘNG THIẾT KẾ KỊCH BẢN THỰC HÀNH", type="primary", use_container_width=True):
        if not chu_de.strip(): st.warning("Vui lòng nhập chủ đề!"); st.stop()
        
        file_context = ""
        if file_tl:
            try:
                if file_tl.name.endswith('.pdf'):
                    reader = PdfReader(file_tl)
                    file_context = "\n".join([p.extract_text() for p in reader.pages[:10]])
                else:
                    doc = docx.Document(file_tl)
                    file_context = "\n".join([p.text for p in doc.paragraphs])
            except: st.error("Lỗi đọc file")

        final_key = api_key if api_key else get_api_key()
        prompt = f"Bạn là chuyên gia {mon_hoc}. Hãy thiết kế kịch bản '{loai_mo_phong}' cho học sinh lớp {lop} với chủ đề '{chu_de}'. Yêu cầu: {yeu_cau}. Dữ liệu tham khảo: {file_context[:3000]}. Xuất ra gồm: Mục tiêu, Dụng cụ, Quy trình thực hiện chi tiết, Lưu ý an toàn và Câu hỏi củng cố."
        
        with st.spinner("AI đang mô phỏng kịch bản..."):
            result = run_ai_with_fallback(prompt=prompt, api_key=final_key, model_mode="flash")
            if result.get("success"):
                st.session_state['current_mophong_data'] = {"title": chu_de, "content": result.get("text")}
                st.rerun()
            else: st.error("AI không phản hồi.")

    # 3. KẾT QUẢ
    if 'current_mophong_data' in st.session_state:
        st.markdown("---")
        with st.expander("Xem kịch bản mô phỏng", expanded=True):
            st.markdown(st.session_state['current_mophong_data']['content'])
            if st.button("Tải kịch bản về máy (Word)"):
                data = WordExportEngine.export_to_word(st.session_state['current_mophong_data'])
                st.download_button("Xác nhận tải file", data=data, file_name="Kich_ban_thuc_hanh.docx", use_container_width=True)
