import streamlit as st
import os
import sys

# --- 1. ĐỊNH VỊ HỆ THỐNG ---
current_working_dir = os.getcwd()
if current_working_dir not in sys.path:
    sys.path.append(current_working_dir)

# --- 2. CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Hệ Sinh Thái Số - L.H.Dưỡng Education", page_icon="👨‍🏫")

# --- 3. IMPORT CÁC MODULE ---
# Đảm bảo các file trong thư mục 'modules/teaching' đã sẵn sàng
try:
    from modules.teaching.ai_quiz_generator import render_quiz_generator
    from views import teacher_support, teaching_support, department_mgmt
except Exception as e:
    st.error(f"Lỗi nạp module: {e}")

# --- 4. SIDEBAR - ĐIỀU KHIỂN ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: red;'>HỆ SINH THÁI SỐ<br>HỖ TRỢ GIÁO VIÊN</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Menu chọn phân hệ bao gồm cả chức năng mới
    phan_he = st.selectbox(
        "CHỌN PHÂN HỆ", 
        ["Hỗ trợ Giáo viên", "Hỗ trợ Giảng dạy", "Quản lý Tổ chuyên môn", "Trình tạo đề kiểm tra"],
        key="sb_phan_he_main"
    )
    
    st.markdown("---")
    st.markdown("🔑 **Cấu hình API Key Cá Nhân**")
    api_key = st.text_input("Nhập Gemini API Key:", type="password", value=st.session_state.get("user_gemini_key", ""))
    
    if api_key:
        st.session_state["user_gemini_key"] = api_key.strip()
        st.success("🎯 Đã cập nhật API Key.")

    # Khởi tạo client dùng chung cho toàn bộ App
    if "user_gemini_key" in st.session_state:
        try:
            import google.generativeai as genai
            genai.configure(api_key=st.session_state["user_gemini_key"])
            st.session_state["gemini_ready"] = True
        except Exception:
            st.session_state["gemini_ready"] = False

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: blue; font-weight: bold;'>Tác giả: Lê Hồng Dưỡng<br>THCS Nguyễn Chí Thanh</div>", unsafe_allow_html=True)

# --- 5. ĐIỀU PHỐI (ROUTER) ---
def run_router():
    try:
        if phan_he == "Hỗ trợ Giáo viên":
            teacher_support.render_module()
        elif phan_he == "Hỗ trợ Giảng dạy":
            teaching_support.render_module()
        elif phan_he == "Quản lý Tổ chuyên môn":
            department_mgmt.render_module()
        elif phan_he == "Trình tạo đề kiểm tra":
            render_quiz_generator()
    except Exception as run_err:
        st.error(f"Hệ thống đang đồng bộ: {run_err}")

if __name__ == "__main__":
    run_router()
