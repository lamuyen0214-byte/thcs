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

# --- 6. ROUTER PHÂN CẤP CHUẨN XÁC ---
# Lấy giá trị hiện tại của selectbox
phan_he_selected = phan_he 

if phan_he_selected == "Hỗ trợ Giáo viên":
    try:
        from views.teacher_support import render_module
        render_module()
    except Exception as e:
        st.error(f"Lỗi nạp Hỗ trợ Giáo viên: {e}")

elif phan_he_selected == "Hỗ trợ Giảng dạy":
    try:
        from views.teaching_support import render_module
        render_module()
    except Exception as e:
        st.error(f"Lỗi nạp Hỗ trợ Giảng dạy: {e}")

elif phan_he_selected == "Quản lý Tổ chuyên môn":
    try:
        from views.department_mgmt import render_module
        render_module()
    except Exception as e:
        st.error(f"Lỗi nạp Quản lý Tổ chuyên môn: {e}")
