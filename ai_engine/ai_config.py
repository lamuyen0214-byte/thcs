from google import genai
import streamlit as st

def get_ai_client(api_key):
    """
    Luôn trả về tuple (client_object, error_message).
    """
    if not api_key:
        return None, "API Key trống. Vui lòng nhập vào thanh bên."
    
    try:
        client = genai.Client(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Lỗi cấu hình AI: {str(e)}"

# Hàm hỗ trợ cho Sidebar
def check_connection():
    key = st.session_state.get("gemini_api_key", "") # Hoặc hàm lấy key của thầy
    if not key:
        st.sidebar.error("❌ Chưa nhập API Key")
        return False
    
    client, error = get_ai_client(key)
    if client:
        st.sidebar.success("✅ Kết nối AI sẵn sàng!")
        return True
    else:
        st.sidebar.error(f"❌ {error}")
        return False
