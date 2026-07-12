# =====================================================================
# FILE: app.py (HỆ THỐNG KHỞI CHẠY CHÍNH ĐÃ ĐỒNG BỘ ROUTER SẠCH LỖI)
# =====================================================================
import streamlit as st
from google import genai
import os
import sys

# --- 0. THUẬT TOÁN ĐỊNH VỊ TỰ ĐỘNG: Ép Python nạp thư mục con 'main' vào luồng tìm kiếm hệ thống ---
current_working_dir = os.getcwd()
if current_working_dir not in sys.path:
    sys.path.append(current_working_dir)

# Nếu chạy trên cấu trúc GitHub có folder con 'main', tự động nhúng đường dẫn con sạch lỗi KeyError
sub_main_path = os.path.join(current_working_dir, "main")
if os.path.exists(sub_main_path) and sub_main_path not in sys.path:
    sys.path.append(sub_main_path)

# --- 1. GIAO DIỆN NHẬP KEY BẢO MẬT TẠI SIDEBAR ---
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

# --- 2. THUẬT TOÁN PHÂN CẤP TRÍCH XUẤT API KEY ---
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

# --- 3. KHỞI TẠO BIẾN CLIENT VÀO SESSION STATE ---
if final_api_key:
    try:
        gemini_client = genai.Client(api_key=str(final_api_key))
        st.session_state["gemini_client"] = gemini_client
    except Exception as e:
        st.sidebar.error(f"❌ Lỗi kết nối máy chủ AI: {e}")
else:
    st.sidebar.warning("⚠️ Vui lòng cấu hình API Key để kích hoạt Trợ lý AI.")

# --- 4. GỌI PHÂN HỆ ROUTER THÔNG SUỐT ---
# ĐÃ HIỆU CHỈNH: Tích hợp cơ chế tìm kiếm đa cấp bẻ gãy hoàn toàn bẫy lỗi KeyError
# SỬA LẠI ĐOẠN NÀY TRONG FILE app.py (Dòng 63 - 68):
# =====================================================================
# ĐOẠN MÃ SỬA ĐỔI HOÀN CHỈNH CHO FILE: app.py (Thay thế dòng 63 - 69)
# =====================================================================
try:
    # 1. Gọi chính xác tên hàm định tuyến từ lõi hệ thống core/router.py
    from core.router import route_teacher
    
    # 2. Thực thi kích hoạt giao diện phân hệ Giáo viên
    route_teacher()
    
except (ModuleNotFoundError, ImportError, KeyError) as router_err:
    # Luồng dự phòng tối cao hiển thị cảnh báo trực quan nếu trục trặc cấu trúc tệp tin
    st.error(f"🛑 Trục trặc khởi chạy phân hệ: Không thể nạp cấu trúc định tuyến hệ thống.")
    st.info(f"💡 Chi tiết kỹ thuật: {router_err}. Vui lòng kiểm tra lại sự tồn tại của file 'core/router.py' trên GitHub.")
# =====================================================================

        st.error("🛑 Không tìm thấy module cấu hình hệ thống 'core.router'. Vui lòng kiểm tra lại cấu trúc thư mục trên GitHub!")

def main():
    route_teacher()

if __name__ == "__main__":
    main()
