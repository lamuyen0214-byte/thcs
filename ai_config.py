import streamlit as st
from google import genai

def render_api_config_sidebar():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 Cấu hình API Key tại máy này")
    # Luôn ưu tiên Key nhập tại Sidebar của chính máy đó
    api_key = st.sidebar.text_input("Nhập Gemini API Key:", type="password", value=st.session_state.get("gemini_api_key", ""))
    if api_key:
        st.session_state["gemini_api_key"] = api_key.strip()
    
def get_ai_client():
    # Lấy Key từ Sidebar hoặc Secrets cục bộ của máy đang chạy
    api_key = st.session_state.get("gemini_api_key") or st.secrets.get("GEMINI_API_KEY")
    if not api_key: return None
    return genai.Client(api_key=api_key)

def get_fallback_queue(model_display_name, phan_he_mode="khbd"):
    # Danh sách Model dự phòng để né lỗi Quota
    mapping = {
        "3.1 Flash-Lite": ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        "3.5 Flash": ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        "3.1 Pro": ["gemini-1.5-pro", "gemini-2.5-flash"],
        "Tư duy mở rộng": ["gemini-2.5-pro", "gemini-1.5-pro"]
    }
    return mapping.get(model_display_name, ["gemini-2.5-flash", "gemini-1.5-flash"])
