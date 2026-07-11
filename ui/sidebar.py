import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("⚙️ Bảng Điều Khiển")
        
        selected_module = st.radio(
            "Chọn phân hệ làm việc:",
            ["Dành cho giáo viên", "Hỗ trợ giảng dạy", "Quản lý tổ chuyên môn"]
        )
        
        st.markdown("---")
        st.info("Phiên bản v1.0 - Kiến trúc 5 lớp AI")
        
        return selected_module
