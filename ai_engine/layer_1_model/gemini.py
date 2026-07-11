import streamlit as st
import requests

class GeminiEngine:
    def __init__(self):
        # Mặc định sử dụng model 1.5 Pro
        self.model_name = "gemini-1.5-pro" 
        
    def render_api_config_sidebar(self):
        """
        =====================================================================
        CẤU HÌNH HỆ THỐNG & API CHUẨN ĐỒNG BỘ ĐỊNH DẠNG MÃ GEMINI MỚI (AQ...)
        =====================================================================
        """
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔑 Cấu hình API Key Cá Nhân")

        default_user_key = st.session_state.get("user_gemini_key", "")

        user_key_input = st.sidebar.text_input(
            "Nhập Gemini API Key (AQ... hoặc AIza...):",
            value=default_user_key,
            type="password",
            help="Các thầy cô dán mã API tạo từ Google AI Studio vào đây."
        )

        if user_key_input:
            st.session_state["user_gemini_key"] = user_key_input.strip()

        final_api_key = None

        if st.session_state.get("user_gemini_key"):
            final_api_key = st.session_state["user_gemini_key"]
            st.sidebar.success("🎯 Đang chạy bằng tài khoản Gemini cá nhân.")
        else:
            if "GEMINI_API_KEY" in st.secrets:
                final_api_key = st.secrets["GEMINI_API_KEY"]
            elif "GOOGLE_API_KEY" in st.secrets:
                final_api_key = st.secrets["GOOGLE_API_KEY"]
            
            if final_api_key:
                st.sidebar.info("💡 Đang sử dụng API Key dự phòng của hệ thống.")

        # Lưu key vào session để dùng cho giao thức REST API ở hàm bên dưới
        if final_api_key:
            st.session_state["active_api_key"] = final_api_key
        else:
            st.session_state["active_api_key"] = None
            st.sidebar.warning("⚠️ Vui lòng cấu hình API Key để kích hoạt Trợ lý AI.")

    def generate_content(self, prompt, system_instruction=None):
        """Hàm sinh nội dung gọi trực tiếp REST API để không bị lỗi định dạng khóa"""
        api_key = st.session_state.get("active_api_key")
        if not api_key:
            return None
            
        # Gọi trực tiếp qua URL của Google (Bypass hoàn toàn lỗi SDK)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        
        # Đóng gói dữ liệu
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 8192
            }
        }
        
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}
            
        try:
            # Gửi yêu cầu HTTP POST
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Bắt các lỗi HTTP (như 400, 401, 500)
            
            data = response.json()
            # Trích xuất đoạn text trả về từ Google
            return data['candidates'][0]['content']['parts'][0]['text']
            
        except requests.exceptions.HTTPError as err:
            st.error(f"❌ Máy chủ Google từ chối truy cập: {err.response.text}")
            return None
        except Exception as e:
            st.error(f"❌ Lỗi hệ thống: {str(e)}")
            return None

# Khởi tạo instance duy nhất
gemini_instance = GeminiEngine()
