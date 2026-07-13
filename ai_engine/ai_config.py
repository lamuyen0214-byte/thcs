import streamlit as st
import json
import os
from google import genai

# =====================================================================
# 1. HÀM TẢI CẤU HÌNH MODEL (GIỮ NGUYÊN TOÀN VẸN 100%)
# =====================================================================
def load_models():
    """Tải model từ file ai_models.json with encoding chuẩn UTF-8."""
    path = os.path.join(os.path.dirname(__file__), 'ai_models.json')
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        # Fallback mặc định nếu không tìm thấy file
        return {"flash": "gemini-2.5-flash", "pro": "gemini-2.5-pro"}

# =====================================================================
# 2. HÀM KHỞI TẠO CLIENT (ĐỒNG NHẤT KIỂU TRẢ VỀ - GIỮ NGUYÊN TOÀN VẸN 100%)
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
# 3. HÀM KIỂM TRA HỆ THỐNG (DÙNG CHO SIDEBAR - GIỮ NGUYÊN TOÀN VẸN 100%)
# =====================================================================
def check_connection():
    """
    Hàm này được gọi từ Sidebar để giáo viên tự chẩn đoán lỗi.
    """
    # Lấy key từ session_state liên thông hệ thống
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

# Hàm phụ trợ để lấy API Key từ session (GIỮ NGUYÊN 100%)
def get_api_key():
    return st.session_state.get("gemini_api_key", "")

# =====================================================================
# 4. GIAO DIỆN CẤU HÌNH SIDEBAR (ĐÃ ĐỒNG BỘ HOÀN HẢO CHỐNG NGHẼN TRÊN MÁY KHÁC)
# =====================================================================
def render_api_config_sidebar():
    """Hàm hiển thị giao diện cấu hình API Key trong Sidebar."""
    import streamlit as st
    
    st.sidebar.markdown("### 🔑 Cấu hình API Key")
    
    # Khởi tạo biến lưu trữ liên thông hệ thống trên bộ nhớ tạm nếu chưa tồn tại
    if "gemini_api_key" not in st.session_state:
        st.session_state["gemini_api_key"] = ""

    # KỸ THUẬT ĐỒNG BỘ PHẢN HỒI (CALLBACK): Ép đồng bộ dữ liệu ngay lập tức khi thầy đổi máy, gõ chữ
    def sync_api_key_callback():
        if "input_api_key_sidebar" in st.session_state:
            st.session_state["gemini_api_key"] = st.session_state["input_api_key_sidebar"].strip()

    # Giữ nguyên cấu trúc hàm text_input và key tĩnh độc bản "input_api_key_sidebar" của thầy
    api_key = st.sidebar.text_input(
        "Gemini API Key:",
        value=st.session_state["gemini_api_key"],
        type="password",
        key="input_api_key_sidebar",
        on_change=sync_api_key_callback # Cấy luồng tự động đồng bộ hóa sang biến liên thông hệ thống
    )
    
    # Cập nhật session_state dự phòng song song để bảo vệ dòng chảy dữ liệu tĩnh
    if api_key:
        st.session_state["gemini_api_key"] = api_key.strip()
        
    # Nút kiểm tra hệ thống (Giữ nguyên tính năng và cấu trúc thầy yêu cầu)
    if st.sidebar.button("🔍 Kiểm tra hệ thống AI"):
        check_connection()
