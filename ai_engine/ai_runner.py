import logging
import time
from ai_engine.ai_config import get_ai_client, load_models

logger = logging.getLogger("AI_Engine")

def run_ai_with_fallback(prompt, api_key, model_mode="flash"):
    if not prompt or not prompt.strip():
        return {"success": False, "error": "Prompt rỗng"}
    
    # Unpack an toàn từ tuple (client, error)
    client, error_msg = get_ai_client(api_key)
    if not client:
        return {"success": False, "error": error_msg}

    # Cấu hình danh sách model
    models_cfg = load_models()
    raw_sequence = [models_cfg.get("flash"), models_cfg.get("pro")] if model_mode == "pro" else [models_cfg.get("flash")]
    fallback_sequence = [m for m in raw_sequence if m]
    
    error_codes = ["429", "503", "500", "RESOURCE_EXHAUSTED", "UNAVAILABLE", "Quota", "PERMISSION_DENIED", "403", "API key"]

    for m in fallback_sequence:
        for retry in range(2): 
            try:
                start_time = time.time()
                # Gọi SDK chuẩn
                response = client.models.generate_content(model=m, contents=prompt)
                
                if response and getattr(response, "text", None):
                    return {
                        "success": True, 
                        "model": m, 
                        "time": time.time() - start_time, 
                        "text": response.text
                    }
                raise Exception("API returned empty")

            except Exception as e:
                msg = str(e)
                # Kiểm tra lỗi chặn hoặc lỗi hệ thống
                if any(err in msg for err in error_codes):
                    logger.warning(f"Retry {retry+1} trên {m} vì lỗi: {msg[:50]}")
                    time.sleep(2)
                    continue
                else:
                    logger.error(f"Fatal error on {m}: {msg}")
                    break # Chuyển sang model tiếp theo nếu lỗi không phải do quota
                    
    return {"success": False, "error": "Hệ thống không phản hồi. Vui lòng kiểm tra lại API Key hoặc quyền truy cập."}
