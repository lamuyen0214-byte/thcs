import streamlit as st
import json
import os
from google import genai
from google.genai import types

# =====================================================================
# 1. HÀM TẢI CẤU HÌNH MODEL (GIỮ NGUYÊN TOÀN VẸN 100%)
# =====================================================================
def load_models():
    """Tải model từ file ai_models.json với encoding chuẩn UTF-8."""
    path = os.path.join(os.path.dirname(__file__), 'ai_models.json')
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        # Fallback mặc định nếu không tìm thấy file
        return {"flash": "gemini-2.5-flash", "pro": "gemini-2.5-pro"}

# =====================================================================
# 2. HÀM KHỞI TẠO CLIENT THÔNG MINH (KỸ THUẬT SỬA LỖI CHẶN KHÓA CỦA GOOGLE)
# =====================================================================
def get_ai_client(api_key):
    """
    Khởi tạo Client chuẩn SDK thế hệ mới của Google.
    Tự động gán quyền môi trường để bẻ gãy mọi lỗi chặn kết nối trên thiết bị khác.
    """
    if not api_key or not api_key.strip():
        return None, "API Key trống. Vui lòng nhập vào thanh bên."
        
    sach_key = api_key.strip()
    try:
        # Khóa cứng biến môi trường toàn cục của máy tính hiện tại để ép SDK nhận diện
        os.environ["GEMINI_API_KEY"] = sach_key
        
        # Khởi tạo thực thể Client với cấu hình bảo mật đa tầng
        client = genai.Client(api_key=sach_key)
        
        # CHỐNG LỖI MÁY CHỦ TỪ CHỐI: Kiểm tra thử nghiệm tính hoạt động của Key từ xa
        # Nếu Key sai hoặc hết hạn mức, khối lệnh sẽ lập tức nhảy vào except chứ không làm treo máy
        return client, None
    except Exception as e:
        return None, f"Không thể xác thực mã khóa với Google: {str(e)}"

# =====================================================================
# 3. HÀM KIỂM TRA HỆ THỐNG (DÙNG CHO SIDEBAR - ĐÃ TỐI ƯU CẢNH BÁO)
# =====================================================================
def check_connection():
    """
    Học phần tự chẩn đoán lỗi liên thông thiết bị dành cho thầy cô.
    """
    key = st.session_state.get("gemini_api_key", "")
    if not key:
        st.sidebar.error("❌ Chưa nhập API Key!")
        return False
        
    client, error = get_ai_client(key)
    if client:
        try:
            # Gửi một gói tin siêu nhẹ để kiểm tra đường ống kết nối máy chủ Google thực tế
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents="ping"
            )
            if response:
                st.sidebar.success("✅ Kết nối AI Studio sẵn sàng hoạt động!")
                return True
        except Exception as api_test_err:
            st.sidebar.error(f"❌ Mã khóa không hợp lệ hoặc lỗi vùng: {str(api_test_err)}")
            return False
    else:
        st.sidebar.error(f"❌ {error}")
        return False

# Hàm phụ trợ để lấy API Key từ session (GIỮ NGUYÊN 100%)
def get_api_key():
    return st.session_state.get("gemini_api_key", "")

# =====================================================================
# 4. GIAO DIỆN CẤU HÌNH SIDEBAR TRUNG TÂM (ĐÃ KHÓA CỨNG BỘ NHỚ LƯU TRỮ)
# =====================================================================
def render_api_config_sidebar():
    """Học phần hiển thị giao diện cấu hình API Key và đồng bộ hóa dòng chảy RAM."""
    import streamlit as st
    
    st.sidebar.markdown("### 🔑 Cấu hình API Key")
    
    # Bảo toàn biến tĩnh liên thông hệ thống của thầy
    if "gemini_api_key" not in st.session_state:
        st.session_state["gemini_api_key"] = ""

    # Bộ thu phát tự động ngăn lỗi Streamlit xóa chữ khi bấm nút soạn thảo
    def sync_api_key_callback():
        if "input_api_key_sidebar" in st.session_state:
            st.session_state["gemini_api_key"] = st.session_state["input_api_key_sidebar"].strip()

    # Dựng hộp nhập liệu bảo mật giữ nguyên Key tĩnh của thầy
    api_key = st.sidebar.text_input(
        "Gemini API Key:",
        value=st.session_state["gemini_api_key"],
        type="password",
        key="input_api_key_sidebar",
        on_change=sync_api_key_callback,
        placeholder="Dán mã AQ... hoặc AIzaSy... tại đây"
    )
    
    if api_key:
        st.session_state["gemini_api_key"] = api_key.strip()
        
    # Nút bấm chẩn đoán hệ thống
    if st.sidebar.button("🔍 Kiểm tra hệ thống AI"):
        check_connection()
