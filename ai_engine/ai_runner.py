import logging
import time

from ai_engine.ai_client import get_ai_client
from ai_engine.ai_config import load_models


logger = logging.getLogger("AI_Engine")


def run_ai_with_fallback(
        prompt,
        api_key,
        model_mode="flash"
):

    if not prompt or not prompt.strip():
        return {
            "success": False,
            "error": "Prompt rỗng"
        }


    client, error_msg = get_ai_client(api_key)

    if not client:
        return {
            "success": False,
            "error": error_msg
        }


    models_cfg = load_models()


    if model_mode == "pro":

        fallback_sequence = [
            models_cfg.get("pro"),
            models_cfg.get("flash")
        ]

    else:

        fallback_sequence = [
            models_cfg.get("flash"),
            models_cfg.get("pro")
        ]


    fallback_sequence = [
        m for m in fallback_sequence if m
    ]


    error_codes = [
        "429",
        "503",
        "500",
        "RESOURCE_EXHAUSTED",
        "UNAVAILABLE",
        "PERMISSION_DENIED",
        "403",
        "INVALID_ARGUMENT"
    ]


    for model in fallback_sequence:

        for retry in range(2):

            try:

                start_time = time.time()

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )


                text = getattr(
                    response,
                    "text",
                    None
                )


                if text and text.strip():

                    return {
                        "success": True,
                        "model": model,
                        "time": time.time()-start_time,
                        "text": text
                    }


                raise Exception(
                    "API trả về nội dung rỗng"
                )


            except Exception as e:

                msg = str(e)


                if any(
                    err in msg
                    for err in error_codes
                ):

                    logger.warning(
                        f"{model} lỗi lần {retry+1}: {msg[:80]}"
                    )

                    time.sleep(2)

                else:

                    logger.error(
                        f"Lỗi nghiêm trọng {model}: {msg}"
                    )

                    break


    return {
        "success": False,
        "error":
        "Gemini không phản hồi. Kiểm tra API Key, quota hoặc quyền truy cập."
    }
