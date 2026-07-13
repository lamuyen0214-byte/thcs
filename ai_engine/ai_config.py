import logging
import json
import os
import streamlit as st
from functools import lru_cache
from google import genai

# 1. Cấu hình Logger (Không chạy lệnh gây lỗi khi import)
logger = logging.getLogger("AI_Engine")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

# 2. Hàm lấy API Key an toàn
def get_api_key():
    """Lấy key từ Session hoặc Secrets một cách an toàn."""
    session_key = st.session_state.get("gemini_api_key", None)
    
    secret_key = None
    try:
        secret_key = st.secrets.get("GEMINI_API_KEY", None)
    except Exception:
        secret_key = None
        
    return session_key or secret_key

# 3. Khởi tạo Client (Sử dụng hàm get_api_key bên trong)
@lru_cache(maxsize=5)
def get_ai_client(api_key):
    if not api_key: return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        logger.error(f"Khởi tạo Client thất bại: {e}")
        return None

# 4. Tải cấu hình Model (Safe access)
def load_models():
    """Tải model với fallback an toàn."""
    path = os.path.join(os.path.dirname(__file__), 'ai_models.json')
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {
                    "flash": data.get("flash", "gemini-2.5-flash"),
                    "pro": data.get("pro", "gemini-2.5-pro")
                }
    except Exception as e:
        logger.warning(f"Lỗi tải ai_models.json: {e}")
    
    # Fallback cứng nếu file lỗi hoặc thiếu key
    return {"flash": "gemini-2.5-flash", "pro": "gemini-2.5-pro"}

# 5. Giao diện Sidebar
def render_api_config_sidebar():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 Cấu hình API Key")
    
    current_key = st.session_state.get("gemini_api_key", "")
    key_input = st.sidebar.text_input("Gemini API Key:", value=current_key, type="password")
    
    if key_input.strip():
        st.session_state["gemini_api_key"] = key_input.strip()
    else:
        if "gemini_api_key" in st.session_state:
            st.session_state.pop("gemini_api_key")
