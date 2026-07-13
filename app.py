# =====================================================================
# FILE CHUẨN HÓA CỦA THẦY LÊ HỒNG DƯỠNG: app.py (VÁ SẠCH LỖI KHỞI CHẠY)
# =====================================================================
import streamlit as st
import os
import sys
from modules.teaching.ai_quiz_generator import render_quiz_generator
# --- BƯỚC 0: THUẬT TOÁN ĐỊNH VỊ TỐI CAO - BẮT BUỘC PHẢI ĐẶT TRÊN CÙNG TRƯỚC LUỒNG IMPORT ---
# Ép Python nạp thư mục hiện tại và folder con 'main' vào luồng tìm kiếm hệ thống
current_working_dir = os.getcwd()
if current_working_dir not in sys.path:
    sys.path.append(current_working_dir)

sub_main_path = os.path.join(current_working_dir, "main")
if os.path.exists(sub_main_path) and sub_main_path not in sys.path:
    sys.path.append(sub_main_path)

# --- BƯỚC 1: KHÓA CẤU HÌNH TRANG ĐẦU TIÊN - Bung rộng tràn viền sát lề laptop ---
try:
    st.set_page_config(layout="wide", page_title="Hệ Sinh Thái Số - L.H.Dưỡng Education", page_icon="👨‍🏫")
except Exception:
    pass

# --- BƯỚC 2: GỌI CÁC FILE VIEWS ĐA CẤP ĐÃ VÁ LỖI KHÔNG TÌM THẤY MODULE ---
try:
    # Thử nạp luồng trực tiếp ở thư mục gốc
    from views import teacher_support, teaching_support, department_mgmt
except (ModuleNotFoundError, ImportError, KeyError):
    try:
        # Nếu kẹt folder con 'main', luồng dự phòng cưỡng ép nạp xuyên thấu folder con
        from main.views import teacher_support, teaching_support, department_mgmt
    except Exception as path_err:
        st.error("🛑 Trục trặc tệp tin: Hệ thống không tìm thấy thư mục 'views' trên kho GitHub của thầy.")
        st.info(f"💡 Chi tiết kỹ thuật: {path_err}")

# Nạp thư viện kết nối AI chính hãng của Google
try:
    from google import genai
except ImportError:
    pass

# --- BƯỚC 3: SIDEBAR - GIỮ NGUYÊN VẸN 100% THIẾT KẾ CỦA THẦY LÊ HỒNG DƯỠNG ---
with st.sidebar:
    st.markdown("""
        <h2 style='text-align: center; color: red; font-size: 24px; margin-bottom: 5px;'>
        HỆ SINH THÁI SỐ<br>HỖ TRỢ GIÁO VIÊN
        </h2>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<h4 style='text-align: center; color: blue;'>CHỌN PHÂN HỆ</h4>", unsafe_allow_html=True)
    phan_he = st.selectbox(
        "Hỗ trợ giáo viên", 
        ["Hỗ trợ Giáo viên", "Hỗ trợ Giảng dạy", "Quản lý Tổ chuyên môn"],
        label_visibility="collapsed", key="sb_phan_he_main_root"
    )
    
    st.markdown("---")
    
    st.markdown("🔑 **Cấu hình API Key Cá Nhân**")
    api_key = st.text_input("Nhập Gemini API Key:", type="password", value=st.session_state.get("user_gemini_key", ""), key="ti_api_key_root")
    
    if api_key:
        st.session_state["user_gemini_key"] = api_key.strip()
        st.markdown("<p style='font-size: 12px; color: green;'>🎯 Đang chạy bằng tài khoản Gemini cá nhân.</p>", unsafe_allow_html=True)

    # Khởi tạo và đồng bộ Client tập trung vào RAM hệ thống phục vụ 2 phân hệ KHBD và Đề KT
    final_api_key = st.session_state.get("user_gemini_key", "").strip()
    if not final_api_key:
        if "GEMINI_API_KEY" in st.secrets: final_api_key = st.secrets["GEMINI_API_KEY"]
        elif "GOOGLE_API_KEY" in st.secrets: final_api_key = st.secrets["GOOGLE_API_KEY"]

    if final_api_key:
        try:
            st.session_state["gemini_client"] = genai.Client(api_key=str(final_api_key))
        except Exception:
            pass
    
    st.markdown("---")
    
    st.markdown("""
        <div style='text-align: center; color: blue; font-weight: bold; font-size: 13px;'>
        Tác giả: Lê Hồng Dưỡng<br>
        Đơn vị: Trường THCS Nguyễn Chí Thanh
        </div>
    """, unsafe_allow_html=True)

# --- BƯỚC 4: ĐIỀU PHỐI (ROUTER) ĐỂ HIỂN THỊ GIAO DIỆN PHÂN HỆ ---
def run_router():
    try:
        if phan_he == "Hỗ trợ Giáo viên":
            teacher_support.render_module()
        elif phan_he == "Hỗ trợ Giảng dạy":
            teaching_support.render_module()
        elif phan_he == "Quản lý Tổ chuyên môn":
            department_mgmt.render_module()
        if chon_phan_he == "Trình tạo đề kiểm tra":
            render_quiz_generator()
    except Exception as run_err:
        st.error(f"💡 Hệ thống đang đồng bộ mã nguồn của phân hệ: {run_err}")

if __name__ == "__main__":
    run_router()
