import streamlit as st
from ai_engine.layer_1_model.gemini import gemini_instance

def render_sidebar():
    with st.sidebar:
        st.title("⚙️ Bảng Điều Khiển")
        
        selected_module = st.radio(
            "Chọn phân hệ làm việc:",
            ["Dành cho giáo viên", "Hỗ trợ giảng dạy", "Quản lý tổ chuyên môn"]
        )
        
        st.info("Phiên bản v1.0 - Kiến trúc 5 lớp AI")
        
    # Gọi thuật toán xử lý mã API Key của thầy hiển thị tiếp nối trên Sidebar
    gemini_instance.render_api_config_sidebar()
    
    return selected_module
