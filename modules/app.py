import streamlit as st
import os
import sys

# 1. ĐỊNH VỊ ĐƯỜNG DẪN
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. IMPORT (Chỉ giữ lại module KHBD)
from modules.danh_cho_giao_vien.khbd.khbd_builder import render_khbd_module

# 3. CẤU HÌNH GIAO DIỆN
st.set_page_config(page_title="Hệ Sinh Thái Số Hỗ Trợ Giáo Viên", layout="wide")
api_key = st.session_state.get('api_key', '')

st.title("👨‍🏫 HỆ SINH THÁI SỐ HỖ TRỢ GIÁO VIÊN")

# 4. CẤU HÌNH TABS (Chỉ còn KHBD)
tab1 = st.tabs(["📚 XD KẾ HOẠCH BÀI DẠY (KHBD)"])

with tab1[0]:
    with st.container():
        render_khbd_module(api_key=api_key)

# 5. SIDEBAR
with st.sidebar:
    st.header("🔑 Cấu hình hệ thống")
    input_key = st.text_input("Nhập API Key cá nhân", type="password", key="api_key")
    st.info("Tác giả: Lê Hồng Dưỡng\nTHCS Nguyễn Chí Thanh")
