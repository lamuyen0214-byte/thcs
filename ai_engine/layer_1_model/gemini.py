# File: ai_engine/layer_1_model/gemini.py
import google.generativeai as genai
from config.model_config import ModelConfig
import streamlit as st

class GeminiEngine:
    def __init__(self):
        # Khởi tạo kết nối với API Key
        api_key = ModelConfig.GEMINI_API_KEY
        if not api_key:
            st.error("⚠️ Chưa tìm thấy GEMINI_API_KEY. Vui lòng kiểm tra lại file .env")
            return
            
        genai.configure(api_key=api_key)
        
        # Thiết lập model và cấu hình
        self.model_name = ModelConfig.DEFAULT_MODEL
        self.generation_config = ModelConfig.get_generation_config()
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config
        )

    def generate_content(self, prompt, system_instruction=None):
        """
        Hàm cốt lõi để sinh nội dung văn bản.
        - prompt: Câu lệnh hoặc yêu cầu chi tiết (ví dụ: yêu cầu sinh giáo án)
        - system_instruction: Định hướng vai trò của AI (tùy chọn)
        """
        try:
            # Nếu có hướng dẫn hệ thống (ví dụ: "Bạn là chuyên gia giáo dục STEM...")
            if system_instruction:
                # Với Gemini 1.5, system instruction có thể được cấu hình ngay khi gọi
                model_with_sys = genai.GenerativeModel(
                    model_name=self.model_name,
                    generation_config=self.generation_config,
                    system_instruction=system_instruction
                )
                response = model_with_sys.generate_content(prompt)
            else:
                response = self.model.generate_content(prompt)
                
            return response.text
            
        except Exception as e:
            st.error(f"❌ Lỗi khi kết nối với AI Engine: {str(e)}")
            return None

# Khởi tạo một instance duy nhất (Singleton) để dùng chung cho toàn dự án
gemini_instance = GeminiEngine()
