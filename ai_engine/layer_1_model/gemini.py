import streamlit as st
from google import genai
from google.genai import types

class GeminiEngine:
    def __init__(self):
        self.client = None
        self.model_name = "gemini-1.5-pro" # Thầy có thể đổi thành gemini-2.0-flash nếu muốn
        
    def render_api_config_sidebar(self):
        """
        =====================================================================
        CẤU HÌNH HỆ THỐNG & API CHUẨN ĐỒNG BỘ ĐỊNH DẠNG MÃ GEMINI MỚI (AQ...)
        =====================================================================
        """
        # 1. Thiết lập ô nhập liệu bảo mật ở Sidebar
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔑 Cấu hình API Key Cá Nhân")

        default_user_key = st.session_state.get("user_gemini_key", "")

        user_key_input = st.sidebar.text_input(
            "Nhập Gemini API Key (Bắt đầu bằng AQ...):",
            value=default_user_key,
            type="password", # Ẩn mã khóa an toàn dưới dạng dấu chấm
            help="Các thầy cô dán mã API tạo từ Google AI Studio (định dạng mới bắt đầu bằng AQ...) vào đây."
        )

        # Xử lý cắt khoảng trắng và lưu chuỗi vào bộ nhớ phiên
        if user_key_input:
            st.session_state["user_gemini_key"] = user_key_input.strip()

        # 2. Thuật toán phân cấp trích xuất API Key hợp lệ
        final_api_key = None

        # Ưu tiên 1: Lấy mã khóa định dạng AQ... do thầy cô tự nhập trên giao diện
        if st.session_state.get("user_gemini_key"):
            final_api_key = st.session_state["user_gemini_key"]
            st.sidebar.success("🎯 Đang chạy bằng tài khoản Gemini cá nhân.")
        # Ưu tiên 2: Lấy mã khóa dự phòng trong Streamlit Secrets của hệ thống
        else:
            if "GEMINI_API_KEY" in st.secrets:
                final_api_key = st.secrets["GEMINI_API_KEY"]
            elif "GOOGLE_API_KEY" in st.secrets:
                final_api_key = st.secrets["GOOGLE_API_KEY"]
            
            if final_api_key:
                st.sidebar.info("💡 Đang sử dụng API Key dự phòng của hệ thống.")

        # 3. Khởi tạo đối tượng Client đồng bộ mã hóa
        if final_api_key:
            try:
                # BIỆN PHÁP ÉP LUỒNG: Ép SDK nhận biến final_api_key chứa chuỗi AQ... dưới dạng chuỗi thô
                self.client = genai.Client(api_key=str(final_api_key))
            except Exception as e:
                st.sidebar.error(f"❌ Lỗi khởi tạo kết nối: {e}")
        else:
            st.sidebar.warning("⚠️ Vui lòng cấu hình API Key để kích hoạt Trợ lý AI.")

    def generate_content(self, prompt, system_instruction=None):
        """Hàm sinh nội dung sử dụng SDK google-genai mới"""
        if not self.client:
            return None
            
        try:
            if system_instruction:
                config = types.GenerateContentConfig(system_instruction=system_instruction)
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config
                )
            else:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
            return response.text
        except Exception as e:
            st.error(f"❌ Lỗi khi sinh nội dung: {str(e)}")
            return None

# Khởi tạo instance duy nhất
gemini_instance = GeminiEngine()
