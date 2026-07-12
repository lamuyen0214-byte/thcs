import streamlit as st
import os
import sys

# Đảm bảo đường dẫn hệ thống
sys.path.append(os.getcwd())

# Cấu hình trang
st.set_page_config(layout="wide", page_title="Hệ Sinh Thái Số - Dưỡng Education", page_icon="🌱")

# --- SIDEBAR: Điều hướng xuyên suốt ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: red;'>HỆ SINH THÁI SỐ</h2>", unsafe_allow_html=True)
    phan_he = st.selectbox(
        "CHỌN PHÂN HỆ:", 
        ["Hỗ trợ Giáo viên", "Hỗ trợ Giảng dạy", "Quản lý Tổ chuyên môn"],
        index=0
    )
    st.markdown("---")
    # API Key giữ ở Sidebar
    api_key = st.text_input("Nhập Gemini API Key:", type="password", value=st.session_state.get("user_gemini_key", ""))
    if api_key:
        st.session_state["user_gemini_key"] = api_key.strip()
        st.sidebar.success("✅ Đã kích hoạt hệ thống AI")

# --- ĐIỀU PHỐI (ROUTER) ---
def run_router():
    if phan_he == "Hỗ trợ Giáo viên":
        from views.teacher_support import render_module
        render_module()
    elif phan_he == "Hỗ trợ Giảng dạy":
        from views.teaching_support import render_module
        render_module()
    elif phan_he == "Quản lý Tổ chuyên môn":
        from views.department_mgmt import render_module
        render_module()

if __name__ == "__main__":
    run_router()
