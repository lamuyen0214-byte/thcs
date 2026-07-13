import streamlit as st
import os
import sys

# 1. ĐỊNH VỊ ĐƯỜNG DẪN ĐỂ IMPORT MODULES
# Đảm bảo đường dẫn gốc được thêm vào sys.path để import modules thành công
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. IMPORT CÁC MODULE BUILDER CỦA THẦY
from modules.danh_cho_giao_vien.khbd.khbd_builder import render_khbd_module
from modules.danh_cho_giao_vien.de_kt.de_kt_builder import render_de_kt_module

# 3. CẤU HÌNH GIAO DIỆN CHUNG
st.set_page_config(page_title="Hệ Sinh Thái Số Hỗ Trợ Giáo Viên", layout="wide")

# Lấy API Key từ session hoặc để trống
api_key = st.session_state.get('api_key', '')

st.title("👨‍🏫 HỆ SINH THÁI SỐ HỖ TRỢ GIÁO VIÊN")

# 4. CƠ CHẾ TABS CÁCH LY (CHỐNG CHỒNG LẤN)
tab1, tab2 = st.tabs(["📚 XD KẾ HOẠCH BÀI DẠY (KHBD)", "📝 XD ĐỀ KIỂM TRA (ĐỀ KT)"])

with tab1:
    # Container cách ly cho KHBD
    with st.container():
        render_khbd_module(api_key=api_key)

with tab2:
    # Container cách ly cho Đề Kiểm Tra
    with st.container():
        render_de_kt_module(api_key=api_key)

# 5. SIDEBAR (NẾU CẦN)
with st.sidebar:
    st.header("🔑 Cấu hình hệ thống")
    input_key = st.text_input("Nhập API Key cá nhân", type="password", key="api_key")
    st.info("Tác giả: Lê Hồng Dưỡng\nTHCS Nguyễn Chí Thanh")
