import streamlit as st
import sys
import os

# --- 1. ĐỊNH VỊ ĐƯỜNG DẪN GỐC (ƯU TIÊN TUYỆT ĐỐI BẰNG INSERT) ---
# Đảm bảo Python ưu tiên tìm kiếm thư mục dự án trước các thư viện hệ thống
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# --- 2. IMPORT CÁC MODULE CHỨC NĂNG ---
#from modules.danh_cho_giao_vien.khbd.khbd_builder import render_khbd_module
#from modules.danh_cho_giao_vien.de_kt.de_kt_builder import render_de_kt_module
#from modules.danh_cho_giao_vien.stem.stem_builder import render_stem_module
#from modules.danh_cho_giao_vien.rubric.rubric_builder import render_rubric_module
#from modules.danh_cho_giao_vien.organization.homeroom_builder import render_homeroom_module
#from modules.danh_cho_giao_vien.quan_ly_diem.quan_ly_diem_builder import render_quan_ly_diem_module
#from modules.danh_cho_giao_vien.tao_prompt.prompt_builder import render_prompt_module

# --- 3. HẰNG SỐ GIAO DIỆN (DRY - DON'T REPEAT YOURSELF) ---
WELCOME_MESSAGE = "⏳ Chào mừng quý thầy cô đến với nền tảng số AI tích hợp chuyên sâu, trường THCS Nguyễn Chí Thanh, P.Tân Lập, tỉnh Đắk Lắk."

# --- 4. GIAO DIỆN CHÍNH PHÂN HỆ GIÁO VIÊN ---
def render_module():
    st.markdown("## 👨‍🏫 Phân hệ: Hỗ trợ Giáo viên")
    
    # Khôi phục nguyên bản 7 tab chuẩn
    tabs = st.tabs([
        "XD KHBD", "XD Đề KT", "Thiết kế bài dạy STEM", 
        "Rubric", "Chủ nhiệm", "Quản lý điểm", "Tạo prompt"
    ])
    
    with tabs[0]:
        render_khbd_module()
        st.info(WELCOME_MESSAGE)
        
    with tabs[1]:
        render_de_kt_module()
        st.info(WELCOME_MESSAGE)

    with tabs[2]:
        st.subheader("🧪 Thiết kế bài dạy STEM")
        st.info(WELCOME_MESSAGE)
        render_stem_module()
        
    with tabs[3]:
        st.subheader("📊 Xây dựng Rubric đánh giá")
        st.info(WELCOME_MESSAGE)
        render_rubric_module()
        
    with tabs[4]:
        st.subheader("📋 Công tác Chủ nhiệm")
        st.info(WELCOME_MESSAGE)
        render_homeroom_module()
        
    with tabs[5]:
        st.subheader("📈 Quản lý điểm số")
        st.info(WELCOME_MESSAGE)
        render_quan_ly_diem_module()
        
    with tabs[6]:
        st.subheader("💡 Công cụ Tạo prompt")
        st.info(WELCOME_MESSAGE)
        render_prompt_module()
