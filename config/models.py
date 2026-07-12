# =====================================================================
# FILE CẤU HÌNH TẬP TRUNG: config/models.py (QUẢN LÝ CORE AI MODEL 2026)
# =====================================================================

# 1. Định nghĩa hằng số mô hình chính hãng hiện hành của Google AI Studio
MODEL_FLASH = "models/gemini-2.5-flash"
MODEL_PRO = "models/gemini-2.5-pro"

# 2. Ánh xạ nhãn hiển thị giao diện sang mã hiệu API kỹ thuật chuẩn xác
MODEL_MAPPING = {
    "3.1 Flash-Lite": "models/gemini-2.5-flash",
    "3.5 Flash": "models/gemini-2.5-flash",
    "3.1 Pro": "models/gemini-2.5-pro",
    "Tư duy mở rộng": "models/gemini-2.5-pro"
}

# 3. Chuỗi dự phòng liên hoàn tối cao chống nghẽn mạng vĩnh viễn (Sạch lỗi 404/503)
FALLBACK_MODELS = [
    "models/gemini-2.5-flash",
    "models/gemini-2.5-pro"
]

def get_fallback_queue(chosen_display_name):
    """Hàm tự động tính toán hàng đợi dự phòng dựa trên lựa chọn thủ công của thầy"""
    primary = MODEL_MAPPING.get(chosen_display_name, MODEL_FLASH)
    # Gộp mô hình chọn thủ công vào đầu chuỗi và dọn sạch trùng lặp
    queue = [primary] + FALLBACK_MODELS
    return list(dict.fromkeys(queue))
