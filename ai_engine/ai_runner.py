import logging
import json
import time
import os
# Kế thừa Client từ file config
from ai_engine.ai_config import get_ai_client

logger = logging.getLogger("AI_Engine")

# =====================================================================
# 1. TẢI CẤU HÌNH MODEL
# =====================================================================
def load_models():
    """Tải model với encoding chuẩn UTF-8."""
    path = os.path.join(os.path.dirname(__file__), 'ai_models.json')
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Không tải được ai_models.json, dùng fallback mặc định: {e}")
        return {"flash": "gemini-2.5-flash", "pro": "gemini-2.5-pro"}

# =====================================================================
# 2. ĐỘNG CƠ XỬ LÝ AI LÕI
# =====================================================================
def run_ai_with_fallback(prompt, api_key, model_mode="flash"):
    if not prompt or not prompt.strip():
        return {"success": False, "error": "Prompt rỗng"}
    
    client = get_ai_client(api_key)
    if not client:
        return {"success": False, "error": "API Key không hợp lệ"}

    models_cfg = load_models()
    
    # Lọc danh sách model an toàn (Loại bỏ giá trị None)
    raw_sequence = [models_cfg.get("flash"), models_cfg.get("pro")] if model_mode == "pro" else [models_cfg.get("flash")]
    fallback_sequence = [m for m in raw_sequence if m]
    
    if not fallback_sequence:
        return {"success": False, "error": "Cấu hình model không hợp lệ"}
    
    # Danh sách lỗi mở rộng để kích hoạt tính năng chạy lại
    error_codes = ["429", "503", "500", "RESOURCE_EXHAUSTED", "UNAVAILABLE", "Quota"]

    for m in fallback_sequence:
        for retry in range(3):
            try:
                start_time = time.time()
                response = client.models.generate_content(model=m, contents=prompt)
                
                text = getattr(response, "text", None)
                if text and text.strip():
                    duration = time.time() - start_time
                    logger.info(f"Success: {m} | Time: {duration:.2f}s")
                    return {
                        "success": True,
                        "model": m,
                        "time": duration,
                        "text": text
                    }
                raise Exception("API returned empty")

            except Exception as e:
                msg = str(e)
                if any(err in msg for err in error_codes):
                    wait_time = 2 ** retry
                    logger.warning(f"Retry {retry+1}/{m} sau {wait_time}s vì lỗi: {msg[:50]}")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"Fatal error on {m}: {msg}")
                    break 
                    
    return {"success": False, "error": "Hệ thống AI không phản hồi sau mọi nỗ lực."}
