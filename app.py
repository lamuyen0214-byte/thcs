import streamlit as st
import os
import sys
from ai_engine.ai_config import render_api_config_sidebar
# --- 1. ĐỊNH VỊ ĐƯỜNG DẪN TUYỆT ĐỐI (TRÁNH LỖI KEYERROR) ---
# Lấy đường dẫn thư mục chứa file app.py hiện tại làm gốc
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.append(app_dir)

# --- 2. CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Hệ Sinh Thái Số - L.H.Dưỡng Education", page_icon="👨‍🏫")

# --- 3. IMPORT CÁC MODULE VÀ TRÁI TIM HỆ THỐNG ---
from ai_config import render_api_config_sidebar

try:
    from modules.teaching.ai_quiz_generator import render_quiz_generator
    from views import teacher_support, teaching_support, department_mgmt
except Exception as e:
    st.error(f"Lỗi nạp module (kiểm tra lại cấu trúc thư mục): {e}")

# --- 4. SIDEBAR - ĐIỀU KHIỂN ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: red;'>HỆ SINH THÁI SỐ<br>HỖ TRỢ GIÁO VIÊN</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Render Sidebar cấu hình API từ ai_config.py
    render_api_config_sidebar()
    
    st.markdown("---")
    phan_he = st.selectbox(
        "CHỌN PHÂN HỆ", 
        ["Hỗ trợ Giáo viên", "Hỗ trợ Giảng dạy", "Quản lý Tổ chuyên môn", "Trình tạo đề kiểm tra"],
        key="sb_phan_he_main"
    )
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: blue; font-weight: bold;'>Tác giả: Lê Hồng Dưỡng<br>THCS Nguyễn Chí Thanh</div>", unsafe_allow_html=True)

# --- 5. ĐIỀU PHỐI (ROUTER) ---
def run_router():
    mapping = {
        "Hỗ trợ Giáo viên": teacher_support.render_module,
        "Hỗ trợ Giảng dạy": teaching_support.render_module,
        "Quản lý Tổ chuyên môn": department_mgmt.render_module,
        "Trình tạo đề kiểm tra": render_quiz_generator
    }
    
    # Thực thi module được chọn
    action = mapping.get(phan_he)
    if action:
        action()
    else:
        st.info("Phân hệ này đang được phát triển.")

if __name__ == "__main__":
    run_router()
