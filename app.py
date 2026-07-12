# =====================================================================
# FILE: app.py (HỆ THỐNG KHỞI CHẠY CHÍNH ĐÃ ĐỒNG BỘ ROUTER CHUẨN ĐỒ HỌA 2026)
# =====================================================================
import streamlit as st
from google import genai
import os
import sys

# --- 1. KHÓA CẤU HÌNH TỐI CAO ĐẦU FILE: Bắt buộc phải là câu lệnh đầu tiên để bung sát lề laptop ---
try:
    st.set_page_config(layout="wide", page_title="Trợ Lý Giáo Viên AI", page_icon="👨‍🏫")
except Exception:
    pass

# --- 2. THUẬT TOÁN ĐỊNH VỊ TỰ ĐỘNG: Ép Python nạp thư mục con 'main' vào luồng tìm kiếm hệ thống ---
current_working_dir = os.getcwd()
if current_working_dir not in sys.path:
    sys.path.append(current_working_dir)

# Nếu chạy trên cấu trúc GitHub có folder con 'main', tự động nhúng đường dẫn con sạch lỗi KeyError
sub_main_path = os.path.join(current_working_dir, "main")
if os.path.exists(sub_main_path) and sub_main_path not in sys.path:
    sys.path.append(sub_main_path)

# --- 3. GIAO DIỆN NHẬP KEY BẢO MẬT TẠI SIDEBAR ---
st.sidebar.markdown("---")
st.sidebar.subheader("🔑 Cấu hình API Key Cá Nhân")

default_user_key = st.session_state.get("user_gemini_key", "")

user_key_input = st.sidebar.text_input(
    "Nhập Gemini API Key (Bắt đầu bằng AQ...):",
    value=default_user_key,
    type="password",
    help="Các thầy cô dán mã API tạo từ Google AI Studio vào đây."
)

if user_key_input:
    st.session_state["user_gemini_key"] = user_key_input.strip()

# --- 4. THUẬT TOÁN PHÂN CẤP TRÍCH XUẤT API KEY ---
final_api_key = None

if st.session_state.get("user_gemini_key"):
    final_api_key = st.session_state["user_gemini_key"]
    st.sidebar.success("🎯 Đang chạy bằng tài khoản Gemini cá nhân của bạn.")
else:
    if "GEMINI_API_KEY" in st.secrets:
        final_api_key = st.secrets["GEMINI_API_KEY"]
    elif "GOOGLE_API_KEY" in st.secrets:
        final_api_key = st.secrets["GOOGLE_API_KEY"]
    
    if final_api_key:
        st.sidebar.info("💡 Đang sử dụng API Key dự phòng của hệ thống.")

# --- 5. KHỞI TẠO BIẾN CLIENT VÀ INTO SESSION STATE ---
if final_api_key:
    try:
        gemini_client = genai.Client(api_key=str(final_api_key))
        st.session_state["gemini_client"] = gemini_client
    except Exception as e:
        st.sidebar.error(f"❌ Lỗi kết nối máy chủ AI: {e}")
else:
    st.sidebar.warning("⚠️ Vui lòng cấu hình API Key để kích hoạt Trợ lý AI.")

# --- 6. GỌI PHÂN HỆ ROUTER THÔNG SUỐT VÀ THỰC THI CHƯƠNG TRÌNH ---
def main():
    try:
        # Gọi chính xác tên hàm định tuyến từ lõi hệ thống core/router.py
        from core.router import route_teacher
        route_teacher()
    except (ModuleNotFoundError, ImportError, KeyError):
        try:
            # Luồng dự phòng nếu cấu trúc thư mục chứa folder con main/ ngầm
            from main.core.router import route_teacher
            route_teacher()
        except Exception as router_err:
            st.error(f"🛑 Trục trặc khởi chạy phân hệ: Không thể nạp cấu trúc định tuyến hệ thống.")
            st.info(f"💡 Chi tiết kỹ thuật: {router_err}. Vui lòng rà soát lại tệp 'core/router.py' trên GitHub.")

if __name__ == "__main__":
    main()
