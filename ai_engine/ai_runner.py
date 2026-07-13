import logging
import time

from ai_engine.ai_config import (
    get_ai_client,
    load_models
)


# ============================================================
# LOGGER
# ============================================================

logger = logging.getLogger("AI_Engine")

if not logger.handlers:
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()

    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    )

    logger.addHandler(handler)



# ============================================================
# AI ENGINE CORE
# ============================================================

def run_ai_with_fallback(
        prompt,
        api_key,
        model_mode="flash"
):
    """
    Engine gọi Gemini có fallback.

    Return:
    {
        success: True/False,
        text: nội dung AI,
        model: model sử dụng,
        time: thời gian xử lý,
        error: thông báo lỗi
    }
    """


    # --------------------------------------------------------
    # 1. Kiểm tra Prompt
    # --------------------------------------------------------

    if not prompt or not prompt.strip():

        return {
            "success": False,
            "error": "Prompt rỗng"
        }



    # --------------------------------------------------------
    # 2. Khởi tạo Gemini Client
    # --------------------------------------------------------

    client, error_msg = get_ai_client(api_key)


    if not client:

        return {
            "success": False,
            "error": error_msg
        }



    # --------------------------------------------------------
    # 3. Load danh sách Model
    # --------------------------------------------------------

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


    # loại bỏ None

    fallback_sequence = [
        m for m in fallback_sequence
        if m
    ]


    if not fallback_sequence:

        return {
            "success": False,
            "error": "Không có model hợp lệ"
        }



    # --------------------------------------------------------
    # 4. Danh sách lỗi cho phép retry
    # --------------------------------------------------------

    retry_errors = [

        "429",
        "RESOURCE_EXHAUSTED",

        "503",
        "UNAVAILABLE",

        "500",

        "TIMEOUT",

        "INTERNAL"
    ]



    # --------------------------------------------------------
    # 5. Gọi Model
    # --------------------------------------------------------

    for model in fallback_sequence:


        for attempt in range(3):

            try:

                start = time.time()



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

                    duration = time.time() - start


                    logger.info(
                        f"SUCCESS {model} - {duration:.2f}s"
                    )


                    return {

                        "success": True,

                        "model": model,

                        "time": duration,

                        "text": text

                    }



                raise Exception(
                    "Gemini trả về nội dung rỗng"
                )



            except Exception as e:


                msg = str(e)



                # lỗi có thể retry

                if any(
                    err in msg
                    for err in retry_errors
                ):


                    wait = 2 ** attempt


                    logger.warning(

                        f"{model} lỗi lần "
                        f"{attempt+1}/3: "
                        f"{msg[:80]}"

                    )


                    time.sleep(wait)


                    continue



                else:


                    logger.error(

                        f"Lỗi không phục hồi "
                        f"{model}: {msg}"

                    )


                    break



    # --------------------------------------------------------
    # 6. Không model nào chạy được
    # --------------------------------------------------------

    return {

        "success": False,

        "error":
        "Gemini không phản hồi. "
        "Kiểm tra API Key, quyền truy cập hoặc quota."

    }
