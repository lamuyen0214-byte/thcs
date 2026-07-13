import logging
import streamlit as st
from functools import lru_cache
from google import genai

# =====================================================================
# 1. CẤU HÌNH LOGGER AN TOÀN
# =====================================================================
logger = logging.getLogger("AI_Engine")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

# =====================================================================
# 2. KHỞI TẠO VÀ QUẢN LÝ CLIENT TỐI ƯU
# =====================================================================
@lru_cache(maxsize=5)
def get_ai_client(api_key):
    if not api_key: return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        logger.error(f"Khởi tạo Client thất bại: {e}")
        return None

# =====================================================================
# 3. GIAO DIỆN TÍCH HỢP CHO FILE APP
# =====================================================================
def render_api_config_sidebar():
    """Hàm hiển thị thanh cấu hình API Key bên Sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 Cấu hình API Key")
    key_input = st.sidebar.text_input("Gemini API Key:", value=st.session_state.get("gemini_api_key", ""), type="password")
    
    if key_input.strip():
        st.session_state["gemini_api_key"] = key_input.strip()
    else:
        st.session_state.pop("gemini_api_key", None)
