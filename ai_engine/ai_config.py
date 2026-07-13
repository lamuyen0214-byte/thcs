import streamlit as st
import json
import os
from google import genai

# =====================================================================
# 1. HÀM TẢI CẤU HÌNH MODEL
# =====================================================================
def load_models():
    """Tải model từ file ai_models.json với encoding chuẩn UTF-8."""
    path = os.path.join(os.path.dirname(__file__), 'ai_models.json')
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        # Fallback mặc định nếu không tìm thấy file
        return {"flash": "gemini-2.5-flash", "pro": "gemini-2.5-pro"}

# =====================================================================
# 2. HÀM KHỞI TẠO CLIENT (ĐỒNG NHẤT KIỂU TRẢ VỀ)
# =====================================================================
def get_ai_client(api_key):
    """
    Luôn trả về tuple (client_object, error_message).
    Giúp tránh lỗi TypeError: cannot unpack non-iterable.
    """
    if not api_key or not api_key.strip():
        return None, "API Key trống. Vui lòng nhập vào thanh bên."
    
    try:
        # Khởi tạo client chuẩn SDK google-genai
        client = genai.Client(api_key=api_key.strip())
        return client, None
    except Exception as e:
        return None, f"Lỗi khởi tạo AI: {str(e)}"

# =====================================================================
# 3. HÀM KIỂM TRA HỆ THỐNG (DÙNG CHO SIDEBAR)
# =====================================================================
def check_connection():
    """
    Hàm này được gọi từ Sidebar để giáo viên tự chẩn đoán lỗi.
    """
    # Lấy key từ session_state (thầy thay thế bằng biến key của thầy)
    key = st.session_state.get("gemini_api_key", "") 
    
    if not key:
        st.sidebar.error("❌ Chưa nhập API Key!")
        return False
    
    client, error = get_ai_client(key)
    if client:
        st.sidebar.success("✅ Kết nối AI sẵn sàng!")
        return True
    else:
        st.sidebar.error(f"❌ {error}")
        return False

# Hàm phụ trợ để lấy API Key từ session (nếu thầy dùng biến khác, hãy điều chỉnh ở đây)
def get_api_key():
    return st.session_state.get("gemini_api_key", "")
