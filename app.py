import streamlit as st
import os
import sys

# 1. Đảm bảo đường dẫn gốc của dự án luôn nằm trong sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.append(root_dir)

# 2. Cấu hình trang trước khi import module con
st.set_page_config(layout="wide", page_title="Hệ Sinh Thái Số - L.H.Dưỡng Education", page_icon="👨‍🏫")

# --- 3. IMPORT CÁC MODULE VÀ TRÁI TIM HỆ THỐNG ---
from ai_engine.ai_config import render_api_config_sidebar

# KHÔNG GỘP CHUNG NỮA - TÁCH RIÊNG TỪNG MODULE ĐỂ CÁCH LY LỖI
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
# ... (Phần Sidebar của thầy giữ nguyên) ...

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
