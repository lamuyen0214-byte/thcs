import streamlit as st

# Import các hàm từ thư mục con
from core.router import route_teacher
from ui.sidebar import render_sidebar

def main():
    st.set_page_config(
        page_title="Hệ Sinh Thái Giáo Dục",
        page_icon="⚛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Khởi chạy Sidebar
    selected_module = render_sidebar()

    # Điều hướng
    if selected_module == "Dành cho giáo viên":
        route_teacher()
    elif selected_module == "Hỗ trợ giảng dạy":
        route_teaching_support()
    elif selected_module == "Quản lý tổ chuyên môn":
        route_management()

if __name__ == "__main__":
    main()
