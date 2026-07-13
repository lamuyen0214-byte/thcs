import streamlit as st
import os
import sys

# 1. Đảm bảo đường dẫn gốc của dự án luôn nằm trong sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.append(root_dir)

# 2. Cấu hình trang trước khi import module con
st.set_page_config(layout="wide", page_title="Hệ Sinh Thái Số - L.H.Dưỡng Education", page_icon="👨‍🏫")

# 3. Import sau khi đã thêm path
try:
    from ai_engine.ai_config import render_api_config_sidebar
    from ai_engine.ai_runner import run_ai_with_fallback
except ImportError as e:
    st.error(f"Lỗi Import: {e}. Vui lòng kiểm tra thư mục ai_engine và file __init__.py")
    st.stop()
try:
    from modules.teaching.ai_quiz_generator import render_quiz_generator
    from views import teacher_support, teaching_support, department_mgmt
except Exception as e:
    st.error(f"Lỗi nạp module: {e}")

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
