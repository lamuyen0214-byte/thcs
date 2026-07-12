import streamlit as st
from google import genai
import os
import sys

# --- 1. CẤU HÌNH GIAO DIỆN ---
try:
    st.set_page_config(layout="wide", page_title="Hệ Sinh Thái Số - Dưỡng Education", page_icon="🌱")
except Exception:
    pass

# --- 2. THUẬT TOÁN ĐỊNH VỊ (Giữ nguyên cấu trúc của thầy) ---
sys.path.append(os.getcwd())
if os.path.exists("main") and "main" not in sys.path:
    sys.path.append(os.path.join(os.getcwd(), "main"))

# --- 3. ĐIỀU HƯỚNG PHÂN HỆ TẠI SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: red;'>HỆ SINH THÁI SỐ</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Menu chọn phân hệ
    phan_he = st.selectbox(
        "CHỌN PHÂN HỆ:",
        ["Hỗ trợ Giáo viên", "Hỗ trợ Giảng dạy", "Quản lý Tổ chuyên môn"],
        index=0
    )
    
    st.markdown("---")
    # Cấu hình API Key (Giữ nguyên logic của thầy)
    user_key_input = st.text_input("Gemini API Key:", type="password", value=st.session_state.get("user_gemini_key", ""))
    if user_key_input:
        st.session_state["user_gemini_key"] = user_key_input.strip()

# --- 4. KHỞI TẠO CLIENT (Sử dụng cho toàn bộ dự án) ---
final_key = st.session_state.get("user_gemini_key") or st.secrets.get("GEMINI_API_KEY")
if final_key:
    st.session_state["gemini_client"] = genai.Client(api_key=final_key)
    st.sidebar.success("✅ Đã kích hoạt hệ thống AI")
else:
    st.sidebar.warning("⚠️ Cấu hình API Key để sử dụng AI")

# --- 5. ĐIỀU PHỐI (ROUTER) CÁC PHÂN HỆ ---
def main():
    if phan_he == "Hỗ trợ Giáo viên":
        try:
            from views.teacher_support import render_module
            render_module()
        except Exception as e:
            st.error(f"Lỗi nạp phân hệ Hỗ trợ Giáo viên: {e}")

    elif phan_he == "Hỗ trợ Giảng dạy":
        try:
            from views.teaching_support import render_module
            render_module()
        except Exception as e:
            st.error(f"Lỗi nạp phân hệ Hỗ trợ Giảng dạy: {e}")

    elif phan_he == "Quản lý Tổ chuyên môn":
        try:
            from views.department_mgmt import render_module
            render_module()
        except Exception as e:
            st.error(f"Lỗi nạp phân hệ Quản lý Tổ chuyên môn: {e}")

if __name__ == "__main__":
    main()
