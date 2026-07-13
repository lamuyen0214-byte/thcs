import streamlit as st
import sys
import os
# ... (Phần import giữ nguyên) ...

def render_module(api_key=""): # Thêm api_key vào tham số
    st.markdown("## 👨‍🏫 Phân hệ: Hỗ trợ Giáo viên")
    tabs = st.tabs(["XD KHBD", "XD Đề KT", "Thiết kế bài dạy STEM", "Rubric", "Chủ nhiệm", "Quản lý điểm", "Tạo prompt"])
    
    with tabs[0]: render_khbd_module(api_key=api_key); st.info(WELCOME_MESSAGE)
    with tabs[1]: render_de_kt_module(api_key=api_key); st.info(WELCOME_MESSAGE)
    with tabs[2]: st.subheader("🧪 Thiết kế bài dạy STEM"); render_stem_module(api_key=api_key); st.info(WELCOME_MESSAGE)
    with tabs[3]: st.subheader("📊 Xây dựng Rubric đánh giá"); render_rubric_module(api_key=api_key); st.info(WELCOME_MESSAGE)
    with tabs[4]: st.subheader("📋 Công tác Chủ nhiệm"); render_homeroom_module(api_key=api_key); st.info(WELCOME_MESSAGE)
    with tabs[5]: st.subheader("📈 Quản lý điểm số"); render_quan_ly_diem_module(api_key=api_key); st.info(WELCOME_MESSAGE)
    with tabs[6]: st.subheader("💡 Công cụ Tạo prompt"); render_prompt_module(api_key=api_key); st.info(WELCOME_MESSAGE)
# --- 1. ĐỊNH VỊ ĐƯỜNG DẪN GỐC ---
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# --- 2. IMPORT CÁC MODULE CHỨC NĂNG ---
from modules.danh_cho_giao_vien.khbd.khbd_builder import render_khbd_module
from modules.danh_cho_giao_vien.de_kt.de_kt_builder import render_de_kt_module
from modules.danh_cho_giao_vien.stem.stem_builder import render_stem_module
from modules.danh_cho_giao_vien.rubric.rubric_builder import render_rubric_module
from modules.danh_cho_giao_vien.organization.homeroom_builder import render_homeroom_module
from modules.danh_cho_giao_vien.quan_ly_diem.quan_ly_diem_builder import render_quan_ly_diem_module
from modules.danh_cho_giao_vien.tao_prompt.prompt_builder import render_prompt_module

# --- 3. HẰNG SỐ GIAO DIỆN ---
WELCOME_MESSAGE = "⏳ Chào mừng quý thầy cô đến với nền tảng số AI tích hợp chuyên sâu, trường THCS Nguyễn Chí Thanh, P.Tân Lập, tỉnh Đắk Lắk."

# --- 4. GIAO DIỆN CHÍNH PHÂN HỆ (ĐÃ NHẬN API_KEY) ---
def render_module(api_key=""):
    st.markdown("## 👨‍🏫 Phân hệ: Hỗ trợ Giáo viên")
    
    tabs = st.tabs([
        "XD KHBD", "XD Đề KT", "Thiết kế bài dạy STEM", 
        "Rubric", "Chủ nhiệm", "Quản lý điểm", "Tạo prompt"
    ])
    
    # Truyền api_key xuống từng module con để chúng khởi tạo Client tại chỗ
    with tabs[0]:
        render_khbd_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    with tabs[1]:
        render_de_kt_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)

    with tabs[2]:
        st.subheader("🧪 Thiết kế bài dạy STEM")
        render_stem_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    with tabs[3]:
        st.subheader("📊 Xây dựng Rubric đánh giá")
        render_rubric_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    with tabs[4]:
        st.subheader("📋 Công tác Chủ nhiệm")
        render_homeroom_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    with tabs[5]:
        st.subheader("📈 Quản lý điểm số")
        render_quan_ly_diem_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
        
    with tabs[6]:
        st.subheader("💡 Công cụ Tạo prompt")
        render_prompt_module(api_key=api_key)
        st.info(WELCOME_MESSAGE)
