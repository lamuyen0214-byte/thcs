import streamlit as st
import sys
import os

# 1. ĐỊNH TUYẾN TUYỆT ĐỐI (GỐC DỰ ÁN)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
if root_dir not in sys.path: sys.path.append(root_dir)
from ai_config import run_ai_with_fallback, render_api_config_sidebar

def render_khbd_module():
    # CSS GỐC CỦA THẦY
    st.markdown("""
        <style>
        div[data-testid="stAppViewBlockContainer"], .main .block-container {
            max-width: 98% !important; width: 98% !important;
            padding-left: 1.5rem !important; padding-right: 1.5rem !important;
        }
        .header-blue {color: #0000FF; font-weight: bold; font-size: 15px; text-align: left; margin-bottom: 2px;}
        .header-red-title {color: #FF0000; font-weight: bold; font-size: 15px; margin-bottom: 5px;}
        </style>
    """, unsafe_allow_html=True)

    # GIAO DIỆN NHẬP LIỆU GỐC
    st.markdown('<p class="header-red-title">Tên bài học / Chủ đề bài dạy:</p>', unsafe_allow_html=True)
    ten_bai = st.text_input("Tên bài", placeholder="Ví dụ: Bài 4: Tốc độ chuyển động", label_visibility="collapsed")

    col_lop, col_mau, col_tiet, col_file = st.columns([1.5, 2, 1.5, 2])
    with col_lop:
        st.markdown('<p class="header-blue">Lớp:</p>', unsafe_allow_html=True)
        lop = st.selectbox("Lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], index=2)
    with col_mau:
        st.markdown('<p class="header-blue">Mẫu thiết kế:</p>', unsafe_allow_html=True)
        mau_thiet_ke = st.selectbox("Mẫu", ["Chuẩn 5512", "Rút gọn", "STEM"])
    with col_tiet:
        st.markdown('<p class="header-blue">Thời lượng (Tiết):</p>', unsafe_allow_html=True)
        thoi_luong = st.number_input("Tiết", min_value=1, value=2)
    with col_file:
        st.markdown('<p class="header-blue">Tài liệu đính kèm:</p>', unsafe_allow_html=True)
        tai_lieu_file = st.file_uploader("Upload", type=['docx', 'pdf', 'txt'], label_visibility="collapsed")

    col_mon, col_model_core = st.columns(2)
    with col_mon:
        st.markdown('<p class="header-blue">Môn học:</p>', unsafe_allow_html=True)
        mon_hoc = st.selectbox("Môn", ["Toán", "Ngữ văn", "Khoa học tự nhiên", "Vật lý", "Hóa học", "Sinh học", "Tin học", "Công nghệ"], index=0)
    with col_model_core:
        st.markdown('<p class="header-blue">Mô hình AI:</p>', unsafe_allow_html=True)
        model_display_name = st.selectbox("Mô hình", ["3.1 Flash-Lite", "3.5 Flash", "3.1 Pro", "Tư duy mở rộng"])

    # LOGIC XỬ LÝ AI CHUẨN MỚI
    if st.button("🚀 KHỞI TẠO TIẾN TRÌNH KẾ HOẠCH BÀI DẠY", type="primary", use_container_width=True):
        if not ten_bai.strip():
            st.warning("⚠️ Vui lòng điền tên bài học.")
        else:
            # Thu thập prompt theo cấu trúc của thầy
            prompt = f"Soạn KHBD môn {mon_hoc}, lớp {lop}, thời lượng {thoi_luong} tiết. Tên bài: {ten_bai}. Mẫu: {mau_thiet_ke}."
            
            with st.spinner("🤖 Trợ lý AI đang soạn thảo..."):
                result, success = run_ai_with_fallback(prompt, model_display_name)
                
                if success:
                    st.session_state['current_khbd_data'] = result
                    st.success("✅ Thành công!")
                    st.rerun()
                else:
                    st.error(result)

    # HIỂN THỊ KẾT QUẢ GỐC
    if 'current_khbd_data' in st.session_state:
        with st.expander("🔍 Xem trước kết quả", expanded=True):
            st.markdown(st.session_state['current_khbd_data'])
