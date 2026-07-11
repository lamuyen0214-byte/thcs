# File: config/model_config.py
import os
from dotenv import load_dotenv

# Tải các biến từ file .env
load_dotenv()

class ModelConfig:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Cấu hình mặc định cho Gemini
    DEFAULT_MODEL = "gemini-1.5-pro"  # Hoặc gemini-1.5-flash tùy nhu cầu tốc độ
    TEMPERATURE = 0.7                 # Độ sáng tạo (0.0 - 1.0)
    TOP_P = 0.9
    TOP_K = 40
    MAX_OUTPUT_TOKENS = 8192          # Đủ dài để sinh toàn bộ giáo án hoặc tài liệu STEM
    
    @classmethod
    def get_generation_config(cls):
        return {
            "temperature": cls.TEMPERATURE,
            "top_p": cls.TOP_P,
            "top_k": cls.TOP_K,
            "max_output_tokens": cls.MAX_OUTPUT_TOKENS,
        }
