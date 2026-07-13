import streamlit as st
from google import genai

def render_api_config_sidebar():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 Cấu hình API Key (Máy này)")
    # Key lưu vào Session State cục bộ của máy tính đang truy cập
    api_key = st.sidebar.text_input("Nhập Gemini API Key:", value=st.session_state.get("gemini_api_key", ""), type="password")
    if api_key:
        st.session_state["gemini_api_key"] = api_key.strip()

def get_ai_client():
    key = st.session_state.get("gemini_api_key") or st.secrets.get("GEMINI_API_KEY")
    if not key: return None
    try: return genai.Client(api_key=key)
    except Exception: return None

def run_ai_with_fallback(prompt, model_choice):
    client = get_ai_client()
    if not client: return "Lỗi: Chưa cấu hình API Key tại Sidebar!", False
    
    # Danh sách model dự phòng theo thứ tự ưu tiên
    fallback_map = {
        "3.1 Flash-Lite": ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        "3.5 Flash": ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        "3.1 Pro": ["gemini-1.5-pro", "gemini-2.5-pro"],
        "Tư duy mở rộng": ["gemini-2.5-pro", "gemini-1.5-pro"]
    }
    models = fallback_map.get(model_choice, ["gemini-2.5-flash"])
    
    for m in models:
        try:
            res = client.models.generate_content(model=m, contents=prompt)
            return res.text, True
        except Exception as e:
            if "429" in str(e): continue
            else: return f"Lỗi kỹ thuật: {str(e)}", False
    return "Lỗi: Đã hết sạch hạn mức Quota (429) trên tất cả các Model.", False
