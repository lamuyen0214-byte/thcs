import streamlit as st
import os
import sys

# --- 1. ĐỊNH VỊ ĐƯỜNG DẪN GỐC ---
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.append(root_dir)

# --- 2. CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Hệ Sinh Thái Số - L.H.Dưỡng Education", page_icon="👨‍🏫")

# --- 3. IMPORT CÁC MODULE VÀ TRÁI TIM HỆ THỐNG ---
from ai_engine.ai_config import render_api_config_sidebar

# TÁCH RIÊNG TỪNG MODULE ĐỂ CÁCH LY LỖI
try:
    from views import teacher_support
except Exception as e:
    st.error(f"Lỗi nạp Phân hệ Giáo viên: {e}")
    teacher_support = None

try:
    from views import teaching_support
except Exception as e:
    st.error(f"Lỗi nạp Phân hệ Giảng dạy: {e}")
    teaching_support = None

try:
    from views import department_mgmt
except Exception as e:
    st.error(f"Lỗi nạp Phân hệ Tổ chuyên môn: {e}")
    department_mgmt = None

try:
    from modules.teaching.ai_quiz_generator import render_quiz_generator
except Exception as e:
    st.error(f"Lỗi nạp Trình tạo đề kiểm tra: {e}")
    render_quiz_generator = None

# --- 4. SIDEBAR - ĐIỀU KHIỂN ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: red;'>HỆ SINH THÁI SỐ<br>HỖ TRỢ GIÁO VIÊN</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Render Sidebar cấu hình API
    render_api_config_sidebar()
    
    st.markdown("---")
# Thay thế phần phan_he = st.selectbox thành st.radio
    phan_he = st.radio(
        "CHỌN PHÂN HỆ", 
        ["Hỗ trợ Giáo viên", "Hỗ trợ Giảng dạy", "Quản lý Tổ chuyên môn", "Trình tạo đề kiểm tra"],
        key="sb_phan_he_main"
    )
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: blue; font-weight: bold;'>Tác giả: Lê Hồng Dưỡng<br>THCS Nguyễn Chí Thanh</div>", unsafe_allow_html=True)

# --- 5. ĐIỀU PHỐI (ROUTER) ---
def run_router():
    mapping = {
        "Hỗ trợ Giáo viên": teacher_support.render_module if teacher_support else None,
        "Hỗ trợ Giảng dạy": teaching_support.render_module if teaching_support else None,
        "Quản lý Tổ chuyên môn": department_mgmt.render_module if department_mgmt else None,
        "Trình tạo đề kiểm tra": render_quiz_generator if render_quiz_generator else None
    }
    
    action = mapping.get(phan_he)
    if action:
        action()
    else:
        st.warning("Phân hệ này đang bị lỗi nạp hoặc đang được phát triển. Vui lòng xem log màu đỏ ở trên.")

if __name__ == "__main__":
    run_router()
