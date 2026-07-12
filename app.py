import streamlit as st
import os
import sys

# Đảm bảo đường dẫn hệ thống
sys.path.append(os.getcwd())
# Cấu hình trang
st.set_page_config(layout="wide", page_title="Hệ Sinh Thái Số -L.H.Dưỡng Education")
from views import teacher_support, teaching_support, department_mgmt
# --- SIDEBAR: Giao diện cố định xuyên suốt ---
    with st.sidebar:
    st.markdown("""
        <h2 style='text-align: center; color: red; font-size: 24px; margin-bottom: 5px;'>
        HỆ SINH THÁI SỐ<br>HỖ TRỢ GIÁO VIÊN
        </h2>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<h4 style='text-align: center; color: blue;'>CHỌN PHÂN HỆ</h4>", unsafe_allow_html=True)
    phan_he = st.selectbox(
        "Hỗ trợ giáo viên", 
        ["Hỗ trợ Giáo viên", "Hỗ trợ Giảng dạy", "Quản lý Tổ chuyên môn"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("🔑 **Cấu hình API Key Cá Nhân**")
    api_key = st.text_input("Nhập Gemini API Key:", type="password", value=st.session_state.get("user_gemini_key", ""))
    if api_key:
        st.session_state["user_gemini_key"] = api_key.strip()
        st.markdown("<p style='font-size: 12px; color: green;'>🎯 Đang chạy bằng tài khoản Gemini cá nhân.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
        <div style='text-align: center; color: blue; font-weight: bold; font-size: 13px;'>
        Tác giả: Lê Hồng Dưỡng<br>
        Đơn vị: Trường THCS Nguyễn Chí Thanh
        </div>
    """, unsafe_allow_html=True)

# --- ĐIỀU PHỐI (ROUTER) ---
def run_router():
    if phan_he == "Hỗ trợ Giáo viên":
        teacher_support.render_module()
    elif phan_he == "Hỗ trợ Giảng dạy":
        teaching_support.render_module()
    elif phan_he == "Quản lý Tổ chuyên môn":
        department_mgmt.render_module()

if __name__ == "__main__":
    run_router()
