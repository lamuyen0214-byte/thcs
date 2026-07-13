import streamlit as st
from google import genai
import time

@st.cache_resource
def create_client(api_key):
    """Khởi tạo Client với cơ chế Cache để tối ưu hiệu năng."""
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Lỗi khởi tạo Gemini Client: {e}")
        return None

def get_ai_client():
    """Lấy client từ session hoặc secrets một cách an toàn."""
    secret_key = st.secrets.get("GEMINI_API_KEY", None)
    key = st.session_state.get("gemini_api_key") or secret_key
    if not key:
        return None
    return create_client(key)

def get_fallback_queue(model_display_name):
    """Danh sách model ưu tiên theo cấu trúc mới của Google."""
    fallback_map = {
        "3.1 Flash-Lite": ["gemini-2.5-flash"],
        "3.5 Flash": ["gemini-2.5-flash"],
        "3.1 Pro": ["gemini-2.5-pro", "gemini-2.5-flash"],
        "Tư duy mở rộng": ["gemini-2.5-pro"]
    }
    return fallback_map.get(model_display_name, ["gemini-2.5-flash"])

def run_ai_with_fallback(prompt, model_choice):
    """Điều phối AI với cơ chế Fallback, Retry, Timeout và Báo cáo model thành công."""
    client = get_ai_client()
    if not client:
        return "⚠️ Chưa cấu hình API Key!", False, None
    
    models = get_fallback_queue(model_choice)
    error_codes = ["429", "503", "500", "RESOURCE_EXHAUSTED", "UNAVAILABLE"]

    for m in models:
        st.sidebar.info(f"🔄 Đang thử model: {m}...")
        
        # Cơ chế Retry (thử lại 2 lần cho mỗi model)
        for retry in range(2):
            try:
                # Sử dụng config cho timeout
                response = client.models.generate_content(
                    model=m, 
                    contents=prompt,
                    config={"timeout": 60} 
                )
                
                text = getattr(response, "text", None)
                if text and text.strip():
                    return text, True, m
                else:
                    raise Exception("Phản hồi rỗng từ API.")
                    
            except Exception as e:
                msg = str(e)
                if any(err in msg for err in error_codes):
                    st.warning(f"Lỗi {m} (Lần thử {retry+1}): {msg[:50]}...")
                    time.sleep(2) # Đợi một chút trước khi thử tiếp
                    continue
                else:
                    st.error(f"Lỗi không thể phục hồi từ {m}: {msg}")
                    break # Thoát retry, thử model tiếp theo
                    
    return "❌ Tất cả model đều không phản hồi hoặc hết hạn mức.", False, None

def render_api_config_sidebar():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 Cấu hình API Key")
    key_input = st.sidebar.text_input("Gemini API Key:", value=st.session_state.get("gemini_api_key", ""), type="password")
    if key_input:
        st.session_state["gemini_api_key"] = key_input.strip()
