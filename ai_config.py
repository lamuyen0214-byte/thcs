import streamlit as st
from google import genai

def render_api_config_sidebar():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 Cấu hình API Key cá nhân")
    current_key = st.session_state.get("gemini_api_key", "")
    api_key = st.sidebar.text_input("Nhập API Key tại máy này:", value=current_key, type="password")
    if api_key:
        st.session_state["gemini_api_key"] = api_key.strip()
        st.sidebar.success("✅ API Key đã được áp dụng cho máy này!")

def get_ai_client():
    api_key = st.session_state.get("gemini_api_key") or st.secrets.get("GEMINI_API_KEY")
    if not api_key: return None
    try: return genai.Client(api_key=api_key)
    except Exception: return None

def get_fallback_queue(model_display_name):
    mapping = {
        "3.1 Flash-Lite": ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        "3.5 Flash": ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        "3.1 Pro": ["gemini-1.5-pro", "gemini-2.5-pro"],
        "Tư duy mở rộng": ["gemini-2.5-pro", "gemini-1.5-pro"]
    }
    return mapping.get(model_display_name, ["gemini-2.5-flash", "gemini-1.5-flash"])
