# =====================================================================
# FILE CẤU HÌNH TẬP TRUNG: config/models.py
# =====================================================================
MODEL_FLASH = "models/gemini-2.5-flash"
MODEL_PRO = "models/gemini-2.5-pro"

MODEL_MAPPING = {
    "3.1 Flash-Lite": "models/gemini-2.5-flash",
    "3.5 Flash": "models/gemini-2.5-flash",
    "3.1 Pro": "models/gemini-2.5-pro",
    "Tư duy mở rộng": "models/gemini-2.5-pro"
}

FALLBACK_MODELS = [
    "models/gemini-2.5-flash",
    "models/gemini-2.5-pro"
]

def get_fallback_queue(chosen_display_name):
    primary = MODEL_MAPPING.get(chosen_display_name, MODEL_FLASH)
    queue = [primary] + FALLBACK_MODELS
    return list(dict.fromkeys(queue))
