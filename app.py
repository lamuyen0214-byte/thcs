import streamlit as st
import os
import sys

# Đảm bảo thư mục gốc nằm trong path để import views
sys.path.append(os.getcwd())

# Import các phân hệ
from views import teacher_support, teaching_support, department_mgmt

st.set_page_config(layout="wide", page_title="Hệ Sinh Thái Số")

# --- SIDEBAR: Điều hướng ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: red;'>HỆ SINH THÁI SỐ</h2>", unsafe_allow_html=True)
    phan_he = st.selectbox("CHỌN PHÂN HỆ:", ["Hỗ trợ Giáo viên", "Hỗ trợ Giảng dạy", "Quản lý Tổ chuyên môn"])
    # ... (phần code API Key của bạn) ...

# --- ROUTER: Gọi hàm render_module() ---
if phan_he == "Hỗ trợ Giáo viên":
    teacher_support.render_module()
elif phan_he == "Hỗ trợ Giảng dạy":
    teaching_support.render_module()
elif phan_he == "Quản lý Tổ chuyên môn":
    department_mgmt.render_module()
