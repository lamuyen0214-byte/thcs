import streamlit as st
import os
import sys
from export.export_word import WordExportEngine
from ai_engine.ai_config import get_api_key
from ai_engine.ai_runner import run_ai_with_fallback

# 1. ĐỊNH VỊ ĐƯỜNG DẪN GỐC
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = current_dir
while not os.path.exists(os.path.join(root_dir, 'ai_engine')) and root_dir != os.path.dirname(root_dir):
    root_dir = os.path.dirname(root_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

def render_de_kt_module(api_key=""):
    # CẤU HÌNH CSS GỌN HƠN
    st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
    div[data-testid="column"] { gap: 0.5rem; }
    .stButton>button { height: 2.5em; }
    </style>
    """, unsafe_allow_html=True)

    # 2. KHU VỰC ĐIỀU KHIỂN CHÍNH (Rất gọn)
    col1, col2, col3 = st.columns(3)
    with col1: mon_hoc = st.selectbox("Môn học", ["Ngữ văn", "Toán", "Ngoại ngữ", "Giáo dục công dân", "Lịch sử và Địa lý", "Khoa học tự nhiên", "Vật Lý", "Hóa Học", "Sinh Học", "Công nghệ", "Tin học", "GDĐP", "HĐTN-HN"], key="sb_mon_de_kt")
    with col2: lop = st.selectbox("Lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], key="sb_lop_de_kt")
    with col3: thoi_gian = st.selectbox("Thời gian", ["45 phút", "60 phút", "90 phút", "120 phút"], key="sb_tg_de_kt")

    ten_bai = st.text_input("Tên bài kiểm tra / Đề số", placeholder="Ví dụ: Kiểm tra cuối kì I", key="txt_ten_bai")

    # 3. CẤU HÌNH NÂNG CAO (Gom vào Expander để tiết kiệm diện tích)
    with st.expander("⚙️ Cấu hình chi tiết (Tỷ lệ & Điểm số)", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<b>Tỷ lệ nhận thức (%)</b>", unsafe_allow_html=True)
            cc1, cc2, cc3, cc4 = st.columns(4)
            nb = cc1.number_input("NB", value=40, key="nb_kt")
            th = cc2.number_input("TH", value=30, key="th_kt")
            vd = cc3.number_input("VD", value=20, key="vd_kt")
            vdc = cc4.number_input("VDC", value=10, key="vdc_kt")
        with c2:
            st.markdown("<b>Thông số đề</b>", unsafe_allow_html=True)
            ccc1, ccc2 = st.columns(2)
            sl1 = ccc1.number_input("SL Trắc nghiệm", value=12, key="sl1")
            d1 = ccc2.number_input("Điểm TN", value=3.0, step=0.25, key="d1")
            sl_tl = ccc1.number_input("Số câu Tự luận", value=4, key="sl_tl")
            d_tl = ccc2.number_input("Tổng điểm TL", value=7.0, step=0.25, key="d_tl")

    # 4. NÚT KHỞI TẠO (To và rõ)
    if st.button("🚀 TỰ ĐỘNG KHỞI TẠO MA TRẬN VÀ ĐỀ THI", type="primary", use_container_width=True):
        final_key = api_key if api_key else get_api_key()
        if not final_key: st.error("Lỗi: Thiếu API Key"); st.stop()
        
        prompt = f"Soạn đề {mon_hoc} {lop}, chủ đề {ten_bai}."
        result = run_ai_with_fallback(prompt=prompt, api_key=final_key, model_mode="flash")
        
        if result.get("success"):
            st.session_state['current_exam_data'] = {
                "is_khbd": False, "title": ten_bai,
                "ai_generated_content": result.get("text")
            }
            st.rerun()

    # 5. XUẤT WORD
    exam_cache = st.session_state.get('current_exam_data')
    if exam_cache:
        st.markdown("---")
        with st.expander("Kết quả đề thi", expanded=True):
            st.markdown(exam_cache["ai_generated_content"])
            if st.button("Tải file Đề thi (Word)", type="primary"):
                try:
                    word_file = WordExportEngine.export_to_word(exam_cache)
                    st.download_button("Tải ngay", data=word_file, file_name="De_Thi.docx", use_container_width=True)
                except Exception as e:
                    st.error(f"Lỗi xuất Word: {e}")

# Gọi hàm
render_de_kt_module()
