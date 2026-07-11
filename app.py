# =====================================================================
# FILE: app.py (HỆ THỐNG KHỞI CHẠY CHÍNH ĐÃ ĐỒNG BỘ ROUTER SẠCH LỖI)
# =====================================================================
import streamlit as st
from google import genai
import os

# --- 1. GIAO DIỆN NHẬP KEY BẢO MẬT TẠI SIDEBAR ---
st.sidebar.markdown("---")
st.sidebar.subheader("🔑 Cấu hình API Key Cá Nhân")

default_user_key = st.session_state.get("user_gemini_key", "")

user_key_input = st.sidebar.text_input(
    "Nhập Gemini API Key (Bắt đầu bằng AQ...):",
    value=default_user_key,
    type="password",
    help="Các thầy cô dán mã API tạo từ Google AI Studio vào đây."
)

if user_key_input:
    st.session_state["user_gemini_key"] = user_key_input.strip()

# --- 2. THUẬT TOÁN PHÂN CẤP TRÍCH XUẤT API KEY ---
final_api_key = None

if st.session_state.get("user_gemini_key"):
    final_api_key = st.session_state["user_gemini_key"]
    st.sidebar.success("🎯 Đang chạy bằng tài khoản Gemini cá nhân của bạn.")
else:
    if "GEMINI_API_KEY" in st.secrets:
        final_api_key = st.secrets["GEMINI_API_KEY"]
    elif "GOOGLE_API_KEY" in st.secrets:
        final_api_key = st.secrets["GOOGLE_API_KEY"]
    
    if final_api_key:
        st.sidebar.info("💡 Đang sử dụng API Key dự phòng của hệ thống.")

# --- 3. KHỔI TẠO BIẾN CLIENT VÀO SESSION STATE ---
if final_api_key:
    try:
        gemini_client = genai.Client(api_key=str(final_api_key))
        st.session_state["gemini_client"] = gemini_client
    except Exception as e:
        st.sidebar.error(f"❌ Lỗi kết nối máy chủ AI: {e}")
else:
    st.sidebar.warning("⚠️ Vui lòng cấu hình API Key để kích hoạt Trợ lý AI.")

# --- 4. GỌI PHÂN HỆ ROUTER THÔNG SUỐT ---
# ĐÃ HIỆU CHỈNH: Chỉ import đúng hàm route_teacher tồn tại trong core/router.py
from core.router import route_teacher

def main():
    route_teacher()

if __name__ == "__main__":
    main()
