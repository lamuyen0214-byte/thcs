# =====================================================================
# FILE ĐỘC LẬP: ai_config.py (VÁ TRIỆT ĐỂ LỖI 401 CHO MÃ API KEY AQ...)
# =====================================================================
import streamlit as st
from google import genai
import os

def init_ai_session():
    """Hàm độc lập dựng ô nhập liệu Sidebar và khởi tạo Client an toàn"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 Cấu hình API Key Cá Nhân")

    default_user_key = st.session_state.get("user_gemini_key", "")

    user_key_input = st.sidebar.text_input(
        "Nhập Gemini API Key (Bắt đầu bằng AQ...):",
        value=default_user_key,
        type="password",
        help="Các thầy cô dán mã API tạo từ Google AI Studio (định dạng mới bắt đầu bằng AQ...) vào đây."
    )

    if user_key_input:
        st.session_state["user_gemini_key"] = user_key_input.strip()

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

    # KHỞI TẠO ĐỐI TƯỢNG KẾT NỐI VỚI GIẢI PHÁP ÉP CHUỖI AN TOÀN TRÁNH LỖI 401
    if final_api_key:
        try:
            # SỬA TRIỆT ĐỂ: Ép kiểu chuỗi thô str() để thư viện SDK ngăn việc nhận nhầm luồng OAuth2
            raw_key_string = str(final_api_key).strip()
            
            # Ép Client nhận diện tham số api_key tường minh 100%
            gemini_client = genai.Client(api_key=raw_key_string)
            
            st.session_state["gemini_client"] = gemini_client
            return gemini_client
        except Exception as e:
            st.sidebar.error(f"❌ Lỗi cấu hình máy chủ AI: {e}")
            return None
    else:
        st.sidebar.warning("⚠️ Vui lòng cấu hình API Key để kích hoạt Trợ lý AI.")
        return None

def get_ai_client():
    """Hàm hỗ trợ lấy nhanh đối tượng client ở bất kỳ file nào trong dự án"""
    return st.session_state.get("gemini_client")
