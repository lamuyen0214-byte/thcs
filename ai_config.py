import streamlit as st
from google import genai

def render_api_config_sidebar():
    """Hàm dựng giao diện Sidebar nhập Key. Gọi ở app.py"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 Cấu hình API Key Cá Nhân")
    
    current_key = st.session_state.get("gemini_api_key", "")
    
    api_key = st.sidebar.text_input(
        "Nhập Gemini API Key (Bắt đầu bằng AQ...):",
        value=current_key,
        type="password"
    )
    
    if api_key:
        st.session_state["gemini_api_key"] = api_key.strip()
        st.sidebar.success("🎯 Đã chốt API Key vào hệ thống!")
    else:
        st.sidebar.warning("⚠️ Vui lòng cấu hình API Key để kích hoạt AI.")

def get_ai_client():
    """Hàm cung cấp Client duy nhất cho toàn bộ dự án"""
    api_key = st.session_state.get("gemini_api_key")
    if not api_key:
        api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else None
        
    if not api_key:
        return None
        
    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Lỗi khởi tạo SDK trung tâm: {e}")
        return None
