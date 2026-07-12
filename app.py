import streamlit as st
import os
import sys

# Đảm bảo đường dẫn hệ thống
sys.path.append(os.getcwd())

# Cấu hình trang
st.set_page_config(layout="wide", page_title="Hệ Sinh Thái Số - Dưỡng Education")

# --- SIDEBAR: Giao diện cố định xuyên suốt ---
with st.sidebar:
    # 1. Tiêu đề thương hiệu
    st.markdown("<h3 style='text-align: center; color: red;'>HỆ SINH THÁI SỐ<br>HỖ TRỢ GIÁO VIÊN</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 2. CHỌN PHÂN HỆ
    st.markdown("<h4 style='text-align: center; color: blue;'>CHỌN PHÂN HỆ</h4>", unsafe_allow_html=True)
    phan_he = st.selectbox(
        "Hỗ trợ giáo viên", 
        ["Hỗ trợ Giáo viên", "Hỗ trợ Giảng dạy", "Quản lý Tổ chuyên môn"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # 3. Cấu hình API Key
    st.markdown("🔑 **Cấu hình API Key Cá Nhân**")
    api_key = st.text_input("Nhập Gemini API Key (Bắt đầu bằng AQ...):", type="password", value=st.session_state.get("user_gemini_key", ""))
    if api_key:
        st.session_state["user_gemini_key"] = api_key.strip()
        st.success("🎯 Đang chạy bằng tài khoản Gemini cá nhân của bạn.")
    
    st.markdown("---")
    
    # 4. Thông tin tác giả (Cố định dưới cùng)
    st.markdown("<div style='text-align: center; color: blue; font-weight: bold;'>"
                "Tác giả: Lê Hồng Dưỡng<br>"
                "Đơn vị: Trường THCS Nguyễn Chí Thanh</div>", unsafe_allow_html=True)

# --- ĐIỀU PHỐI (ROUTER) ---
def run_router():
    # Gọi các file views đã xây dựng
    from views import teacher_support, teaching_support, department_mgmt
    
    if phan_he == "Hỗ trợ Giáo viên":
        teacher_support.render_module()
    elif phan_he == "Hỗ trợ Giảng dạy":
        teaching_support.render_module()
    elif phan_he == "Quản lý Tổ chuyên môn":
        department_mgmt.render_module()

if __name__ == "__main__":
    run_router()
