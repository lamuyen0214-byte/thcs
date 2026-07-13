import streamlit as st
import os
import sys

# --- 1. ĐỊNH VỊ ĐƯỜNG DẪN GỐC ---
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.append(root_dir)

# --- 2. CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Hệ Sinh Thái Số - L.H.Dưỡng Education", page_icon="👨‍🏫")

# --- 3. IMPORT CÁC MODULE ---
from ai_engine.ai_config import render_api_config_sidebar

# Tách riêng từng module để cách ly lỗi
try:
    from views import teacher_support, teaching_support, department_mgmt
except Exception as e:
    st.error(f"Lỗi nạp View: {e}")
    teacher_support = teaching_support = department_mgmt = None

try:
    from modules.teaching.ai_quiz_generator import render_quiz_generator
except Exception as e:
    st.error(f"Lỗi nạp Trình tạo đề kiểm tra: {e}")
    render_quiz_generator = None

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: red;'>HỆ SINH THÁI SỐ<br>HỖ TRỢ GIÁO VIÊN</h2>", unsafe_allow_html=True)
    
    phan_he = st.radio(
        "CHỌN PHÂN HỆ", 
        ["Hỗ trợ Giáo viên", "Hỗ trợ Giảng dạy", "Quản lý Tổ chuyên môn", "Trình tạo đề kiểm tra"],
        key="sb_phan_he_main"
    )
    
    # Render API Config và nút kiểm tra hệ thống
    render_api_config_sidebar()
    
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center;'>
            <p style='font-style: italic; font-size: 13px; color: #555;'>
                Tác giả: Lê Hồng Dưỡng<br>
                THCS Nguyễn Chí Thanh
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# ... (Phần import và sidebar giữ nguyên) ...

# --- 5. ĐIỀU PHỐI (ROUTER) ---
def run_router():
    current_key = st.session_state.get("gemini_api_key", "")
    mapping = {
        "Hỗ trợ Giáo viên": teacher_support.render_module if teacher_support else None,
        "Hỗ trợ Giảng dạy": teaching_support.render_module if teaching_support else None,
        "Quản lý Tổ chuyên môn": department_mgmt.render_module if department_mgmt else None,
        "Trình tạo đề kiểm tra": render_quiz_generator if render_quiz_generator else None
    }
    
    action = mapping.get(phan_he)
    if action:
        # Truyền api_key xuống phân hệ con
        action(api_key=current_key) 
    else:
        st.warning("Phân hệ này đang bị lỗi nạp hoặc đang được phát triển.")

if __name__ == "__main__":
    run_router()
