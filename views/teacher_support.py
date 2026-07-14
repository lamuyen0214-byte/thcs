import streamlit as st
import sys
import os

# =====================================================================
# 1. ĐỊNH VỊ ĐƯỜNG DẪN GỐC HỆ THỐNG (ĐƯA LÊN ĐẦU FILE)
# =====================================================================
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# =====================================================================
# 2. IMPORT CÁC MODULE CHỨC NĂNG CON
# =====================================================================
from modules.danh_cho_giao_vien.khbd.khbd_builder import render_khbd_module
from modules.danh_cho_giao_vien.de_kt.de_kt_builder import render_de_kt_module
from modules.danh_cho_giao_vien.stem.stem_builder import render_stem_module
from modules.danh_cho_giao_vien.rubric.rubric_builder import render_rubric_module
from modules.danh_cho_giao_vien.organization.homeroom_builder import render_homeroom_module
from modules.danh_cho_giao_vien.quan_ly_diem.quan_ly_diem_builder import render_quan_ly_diem_module
from modules.danh_cho_giao_vien.tao_prompt.prompt_builder import render_prompt_module
from modules.danh_cho_giao_vien.quizizz.quizizz_builder import render_quizizz_module
# =====================================================================
# 3. HẰNG SỐ NỀN TẢNG GIAO DIỆN
# =====================================================================
WELCOME_MESSAGE = "⏳ Chào mừng quý thầy cô đến với nền tảng số AI tích hợp chuyên sâu, trường THCS Nguyễn Chí Thanh, P.Tân Lập, tỉnh Đắk Lắk."

# =====================================================================
# 4. GIAO DIỆN CHÍNH PHÂN HỆ (ĐÃ KHỬ TRÙNG LẶP VÀ SỬA EMOJI BỊ LỖI CHUỖI)
# =====================================================================
def render_module(api_key=""):
    """
    Hàm điều phối trung tâm của phân hệ Hỗ trợ Giáo viên.
    Tiếp nhận api_key từ app.py và phân phối xuống tất cả các tính năng cốt lõi.
    """
    st.markdown("## 👨‍🏫 Phân hệ: Hỗ trợ Giáo viên")
    
    # Khởi tạo thanh Tabs chức năng cho giáo viên
    tabs = st.tabs([
        "XD KHBD", 
        "XD Đề KT", 
        "Thiết kế bài dạy STEM", 
        "Rubric", 
        "Chủ nhiệm", 
        "Quản lý điểm", 
        "Tạo prompt"
    ])
    
    # --- Tab 1: Xây dựng Kế hoạch bài dạy (Giáo án) ---
    with tabs[0]:
        render_khbd_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    # --- Tab 2: Xây dựng Đề kiểm tra ---
    with tabs[1]:
        render_de_kt_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    # --- Tab 3: Thiết kế bài dạy STEM ---
    with tabs[2]:
        st.subheader("🧪 Thiết kế bài dạy STEM")
        render_stem_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    # --- Tab 4: Xây dựng Rubric đánh giá ---
    with tabs[3]:
        st.subheader("📊 Xây dựng Rubric đánh giá")
        render_rubric_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    # --- Tab 5: Công tác Chủ nhiệm lớp ---
    with tabs[4]:
        st.subheader("📋 Công tác Chủ nhiệm")
        render_homeroom_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    # --- Tab 6: Quản lý điểm số học sinh ---
    with tabs[5]:
        st.subheader("📈 Quản lý điểm số")
        render_quan_ly_diem_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    # --- Tab 7: Công cụ Tạo prompt tối ưu cho AI ---
    with tabs[6]:
        st.subheader("💡 Công cụ Tạo prompt")
        render_prompt_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
import streamlit as st
import sys
import os

# =====================================================================
# 1. ĐỊNH VỊ ĐƯỜNG DẪN GỐC HỆ THỐNG (ĐƯA LÊN ĐẦU FILE)
# =====================================================================
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# =====================================================================
# 2. IMPORT CÁC MODULE CHỨC NĂNG CON
# =====================================================================
from modules.danh_cho_giao_vien.khbd.khbd_builder import render_khbd_module
from modules.danh_cho_giao_vien.de_kt.de_kt_builder import render_de_kt_module
from modules.danh_cho_giao_vien.stem.stem_builder import render_stem_module
from modules.danh_cho_giao_vien.rubric.rubric_builder import render_rubric_module
from modules.danh_cho_giao_vien.organization.homeroom_builder import render_homeroom_module
from modules.danh_cho_giao_vien.quan_ly_diem.quan_ly_diem_builder import render_quan_ly_diem_module
from modules.danh_cho_giao_vien.tao_prompt.prompt_builder import render_prompt_module

# =====================================================================
# 3. HẰNG SỐ NỀN TẢNG GIAO DIỆN
# =====================================================================
WELCOME_MESSAGE = "⏳ Chào mừng quý thầy cô đến với nền tảng số AI tích hợp chuyên sâu, trường THCS Nguyễn Chí Thanh, P.Tân Lập, tỉnh Đắk Lắk."

# =====================================================================
# 4. GIAO DIỆN CHÍNH PHÂN HỆ
# =====================================================================
def render_module(api_key=""):
    """
    Hàm điều phối trung tâm của phân hệ Hỗ trợ Giáo viên.
    Tiếp nhận api_key từ app.py và phân phối xuống tất cả các tính năng cốt lõi.
    """
    st.markdown("## 👨‍🏫 Phân hệ: Hỗ trợ Giáo viên")
    
    # Khởi tạo thanh Tabs chức năng cho giáo viên (Đã bổ sung 2 thẻ mới)
    tabs = st.tabs([
        "XD KHBD", 
        "XD Đề KT", 
        "Thiết kế bài dạy STEM", 
        "Rubric", 
        "Chủ nhiệm", 
        "Quản lý điểm", 
        "Tạo prompt",
        "Quizizz",              # <-- Thẻ mới 1
        "Mô phỏng thực hành"    # <-- Thẻ mới 2
    ])
    
    # --- Tab 1: Xây dựng Kế hoạch bài dạy (Giáo án) ---
    with tabs[0]:
        render_khbd_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    # --- Tab 2: Xây dựng Đề kiểm tra ---
    with tabs[1]:
        render_de_kt_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    # --- Tab 3: Thiết kế bài dạy STEM ---
    with tabs[2]:
        st.subheader("🧪 Thiết kế bài dạy STEM")
        render_stem_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    # --- Tab 4: Xây dựng Rubric đánh giá ---
    with tabs[3]:
        st.subheader("📊 Xây dựng Rubric đánh giá")
        render_rubric_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    # --- Tab 5: Công tác Chủ nhiệm lớp ---
    with tabs[4]:
        st.subheader("📋 Công tác Chủ nhiệm")
        render_homeroom_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    # --- Tab 6: Quản lý điểm số học sinh ---
    with tabs[5]:
        st.subheader("📈 Quản lý điểm số")
        render_quan_ly_diem_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    # --- Tab 7: Công cụ Tạo prompt tối ưu cho AI ---
    with tabs[6]:
        st.subheader("💡 Công cụ Tạo prompt")
        render_prompt_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)

    # --- Tab 8: Quizizz nội bộ ---
        
    with tabs[7]:
        st.subheader("🎯 Quizizz nội bộ (AI sinh & chấm trắc nghiệm)")
        st.info(WELCOME_MESSAGE)
        render_quizizz_module(api_key=api_key)

    # --- Tab 9: Mô phỏng thực hành KHTN ---
    with tabs[8]:
        st.subheader("🔬 Mô phỏng thực hành KHTN")
        st.warning("🚧 Phân hệ đang trong quá trình phát triển và tích hợp. Xin vui lòng quay lại sau!")
        # Nơi gọi hàm tương lai: render_mophong_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
