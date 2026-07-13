import streamlit as st
import os
import sys

# Định vị thư mục gốc
sys.path.append(os.getcwd())
from ai_config import render_api_config_sidebar

st.set_page_config(layout="wide", page_title="Hệ Sinh Thái Số - L.H.Dưỡng Education", page_icon="👨‍🏫")

# Import các module đã được chuẩn hóa
try:
    from modules.teaching.ai_quiz_generator import render_quiz_generator
    from views import teacher_support, teaching_support, department_mgmt
except Exception as e:
    st.error(f"Lỗi nạp module: {e}")

# Sidebar đồng bộ
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: red;'>HỆ SINH THÁI SỐ</h2>", unsafe_allow_html=True)
    render_api_config_sidebar()
    phan_he = st.selectbox("CHỌN PHÂN HỆ", ["Hỗ trợ Giáo viên", "Hỗ trợ Giảng dạy", "Quản lý Tổ chuyên môn", "Trình tạo đề kiểm tra"])
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: blue;'>Tác giả: Lê Hồng Dưỡng</div>", unsafe_allow_html=True)

def run_router():
    mapping = {
        "Hỗ trợ Giáo viên": teacher_support.render_module,
        "Hỗ trợ Giảng dạy": teaching_support.render_module,
        "Quản lý Tổ chuyên môn": department_mgmt.render_module,
        "Trình tạo đề kiểm tra": render_quiz_generator
    }
    mapping.get(phan_he, lambda: st.write("Đang phát triển..."))()

if __name__ == "__main__":
    run_router()
