import streamlit as st
import os
import sys

# =====================================================================
# 1. ĐỊNH VỊ ĐƯỜNG DẪN GỐC CHỐNG LỖI IMPORT TRÊN MÁY TÍNH KHÁC (TỐI ƯU CAO CẤP)
# =====================================================================
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Ép hệ thống nhận diện cả thư mục lõi để các file con gọi trực tiếp không bị lạc đường
ai_engine_path = os.path.join(root_dir, 'ai_engine')
if os.path.exists(ai_engine_path) and ai_engine_path not in sys.path:
    sys.path.insert(0, ai_engine_path)

# =====================================================================
# 2. CẤU HÌNH TRANG (GIỮ NGUYÊN 100%)
# =====================================================================
st.set_page_config(layout="wide", page_title="Hệ Sinh Thái Số - L.H.Dưỡng Education", page_icon="👨‍🏫")

# =====================================================================
# 3. IMPORT CÁC MODULE VÀ TRÁI TIM HỆ THỐNG
# =====================================================================
from ai_engine.ai_config import render_api_config_sidebar

# TÁCH RIÊNG TỪNG MODULE ĐỂ CÁCH LY LỖI VÀ CHẨN ĐOÁN CHÍNH XÁC
try:
    from views import teacher_support
except Exception as e:
    st.error(f"Lỗi nạp Phân hệ Giáo viên: {e}")
    teacher_support = None

try:
    from views import teaching_support
except Exception as e:
    st.error(f"Lỗi nạp Phân hệ Giảng dạy: {e}")
    teaching_support = None

try:
    from views import department_mgmt
except Exception as e:
    st.error(f"Lỗi nạp Phân hệ Tổ chuyên môn: {e}")
    department_mgmt = None

try:
    from modules.teaching.ai_quiz_generator import render_quiz_generator
except Exception as e:
    st.error(f"Lỗi nạp Trình tạo đề kiểm tra: {e}")
    render_quiz_generator = None

# =====================================================================
# 4. THANH SIDEBAR ĐIỀU HƯỚNG VÀ CẤU HÌNH (GIỮ NGUYÊN 100%)
# =====================================================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: red;'>HỆ SINH THÁI SỐ<br>HỖ TRỢ GIÁO VIÊN</h2>", unsafe_allow_html=True)
    
    # Danh sách phân hệ 
    phan_he = st.radio(
        "CHỌN PHÂN HỆ", 
        ["Hỗ trợ Giáo viên", "Hỗ trợ Giảng dạy", "Quản lý Tổ chuyên môn"], 
        key="sb_phan_he_main"
    )
    
    # Render Sidebar cấu hình API - Để sát ngay dưới radio
    render_api_config_sidebar()
    
    # Chân trang hằng số tác giả của thầy
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center;'>
            <p style='font-style: italic; font-size: 13px; color: #555;'>
                Tác giả: Lê Hồng Dưỡng<br>
                THCS Nguyễn Chí Thanh
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# =====================================================================
# 5. ĐIỀU PHỐI LIÊN THÔNG ĐĂNG NHẬP (ROUTER)
# =====================================================================
def run_router():
    # Lấy dữ liệu API Key bảo mật từ RAM phiên làm việc
    current_key = st.session_state.get("gemini_api_key", "")
    
    mapping = {
        "Hỗ trợ Giáo viên": teacher_support.render_module if teacher_support else None,
        "Hỗ trợ Giảng dạy": teaching_support.render_module if teaching_support else None,
        "Quản lý Tổ chuyên môn": department_mgmt.render_module if department_mgmt else None,
        "Trình tạo đề kiểm tra": render_quiz_generator if render_quiz_generator else None
    }
    
    action = mapping.get(phan_he)
    if action:
        try:
            # Chuyển tiếp mã đăng nhập an toàn xuống các tầng kiến trúc con
            action(api_key=current_key)
        except TypeError:
            # Phương án dự phòng an toàn tuyệt đối nếu có phân hệ chưa kịp cập nhật tham số nhận
            action()
    else:
        st.warning("Phân hệ này đang bị lỗi nạp hoặc đang được phát triển. Vui lòng xem log màu đỏ ở trên.")

if __name__ == "__main__":
    run_router()
