import streamlit as st
from google import genai
import time
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

@st.cache_resource
def create_client(api_key):
    """Khởi tạo Client an toàn, không chứa UI call."""
    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None

def get_ai_client():
    secret_key = st.secrets.get("GEMINI_API_KEY", None)
    key = st.session_state.get("gemini_api_key") or secret_key
    if not key:
        return None
    return create_client(key)

def get_fallback_queue(model_display_name):
    fallback_map = {
        "3.1 Flash-Lite": ["gemini-2.5-flash"],
        "3.5 Flash": ["gemini-2.5-flash"],
        "3.1 Pro": ["gemini-2.5-pro", "gemini-2.5-flash"],
        "Tư duy mở rộng": ["gemini-2.5-pro"]
    }
    return fallback_map.get(model_display_name, ["gemini-2.5-flash"])

def run_ai_with_fallback(prompt, model_choice):
    """Engine xử lý AI tinh gọn, trả dữ liệu, không làm phiền UI."""
    # 1. Kiểm tra độ dài prompt (Giới hạn khoảng 800k ký tự ~ 200k tokens cho Flash)
    if len(prompt) > 800000:
        return None, False, "Prompt quá dài, vui lòng rút gọn tài liệu."

    client = get_ai_client()
    if not client:
        return None, False, "Chưa cấu hình API Key."
    
    models = get_fallback_queue(model_choice)
    error_codes = ["429", "503", "500", "RESOURCE_EXHAUSTED", "UNAVAILABLE"]
    
    # Placeholder cho status update trong sidebar
    status_bar = st.sidebar.empty()

    for m in models:
        status_bar.info(f"🔄 Đang gọi: {m}...")
        
        # Thử lại 3 lần với exponential backoff
        for retry in range(3):
            try:
                start_time = time.time()
                
                # Gọi API không dùng timeout trong config
                response = client.models.generate_content(
                    model=m, 
                    contents=prompt,
                    config={"temperature": 0.4, "top_p": 0.95}
                )
                
                duration = time.time() - start_time
                text = getattr(response, "text", None)
                
                if text and text.strip():
                    logging.info(f"Success: {m} | Time: {duration:.2f}s")
                    status_bar.empty()
                    return text, True, m
                else:
                    raise Exception("API returned empty content")
                    
            except Exception as e:
                msg = str(e)
                if any(err in msg for err in error_codes):
                    wait_time = 2 ** retry
                    logging.warning(f"Retry {retry+1} for {m} after {wait_time}s due to: {msg[:50]}")
                    time.sleep(wait_time)
                    continue
                else:
                    logging.error(f"Fatal error {m}: {msg}")
                    break # Lỗi không hồi phục
    
    status_bar.empty()
    return None, False, "Hệ thống AI không phản hồi sau nhiều lần thử."

def render_api_config_sidebar():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 Cấu hình API Key")
    key_input = st.sidebar.text_input("Gemini API Key:", value=st.session_state.get("gemini_api_key", ""), type="password")
    
    if key_input.strip():
        st.session_state["gemini_api_key"] = key_input.strip()
    else:
        st.session_state.pop("gemini_api_key", None)
