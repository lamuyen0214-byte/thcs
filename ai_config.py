import streamlit as st
from google import genai # CHUẨN SDK MỚI

def render_api_config_sidebar():
    """Hàm hiển thị Sidebar để nhập Key"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 Cấu hình API Key Cá Nhân")
    
    # Bước 2: Lấy đúng biến gemini_api_key
    current_key = st.session_state.get("gemini_api_key", "")
    
    api_key = st.sidebar.text_input(
        "Nhập Gemini API Key (AQ...):",
        value=current_key,
        type="password"
    )
    
    # Lưu chặt chẽ vào session_state
    if api_key:
        st.session_state["gemini_api_key"] = api_key.strip()
        st.sidebar.success("🎯 Đã lưu API Key!")
    else:
        st.sidebar.warning("⚠️ Vui lòng cấu hình API Key.")

def get_ai_client():
    """Bước 1: Hàm trung tâm cung cấp Client"""
    # Lấy key từ session (ưu tiên) hoặc secrets
    api_key = st.session_state.get("gemini_api_key")
    if not api_key:
        api_key = st.secrets.get("GEMINI_API_KEY") 
        
    if not api_key:
        return None
        
    try:
        # Khởi tạo Client chuẩn SDK mới
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Lỗi khởi tạo SDK: {e}")
        return None
