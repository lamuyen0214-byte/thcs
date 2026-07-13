from google import genai
import streamlit as st
from functools import lru_cache


@lru_cache(maxsize=5)
def get_ai_client(api_key):
    """
    Luôn trả về tuple:
    (client_object, error_message)
    """

    if not api_key:
        return None, "API Key trống. Vui lòng nhập vào thanh bên."

    try:
        api_key = api_key.strip()

        client = genai.Client(
            api_key=api_key
        )

        return client, None

    except Exception as e:
        return None, f"Lỗi cấu hình AI: {str(e)}"



def render_api_config_sidebar():
    """
    Hiển thị vùng nhập API Key trên Sidebar.
    """

    st.sidebar.markdown("---")
    st.sidebar.subheader(
        "🔑 Cấu hình Gemini API"
    )

    current_key = st.session_state.get(
        "gemini_api_key",
        ""
    )


    key_input = st.sidebar.text_input(
        "Gemini API Key:",
        value=current_key,
        type="password"
    )


    if key_input.strip():

        st.session_state[
            "gemini_api_key"
        ] = key_input.strip()

        st.sidebar.success(
            "✅ Đã lưu API Key cho phiên làm việc"
        )


    elif "gemini_api_key" in st.session_state:

        st.session_state.pop(
            "gemini_api_key",
            None
        )



def check_connection():
    """
    Kiểm tra Client Gemini.
    """

    key = st.session_state.get(
        "gemini_api_key",
        ""
    )


    if not key:

        st.sidebar.error(
            "❌ Chưa nhập API Key"
        )

        return False


    client, error = get_ai_client(key)


    if client:

        st.sidebar.success(
            "✅ Kết nối AI sẵn sàng!"
        )

        return True


    else:

        st.sidebar.error(
            f"❌ {error}"
        )

        return False
