import streamlit as st
from google import genai

def render_api_config_sidebar():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 Cấu hình API Key")
    current_key = st.session_state.get("gemini_api_key", "")
    api_key = st.sidebar.text_input("Nhập Gemini API Key:", value=current_key, type="password")
    if api_key:
        st.session_state["gemini_api_key"] = api_key.strip()
        st.sidebar.success("🎯 API Key đã cập nhật!")

def get_ai_client():
    api_key = st.session_state.get("gemini_api_key") or st.secrets.get("GEMINI_API_KEY")
    if not api_key: return None
    try:
        return genai.Client(api_key=api_key)
    except Exception: return None
