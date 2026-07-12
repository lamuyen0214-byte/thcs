import streamlit as st
from modules.danh_cho_giao_vien.khbd.khbd_builder import render_khbd_module
from modules.danh_cho_giao_vien.de_kt.de_kt_builder import render_de_kt_module
# Khai báo sẵn module STEM để thầy ghép vào sau
from modules.danh_cho_giao_vien.stem.stem_builder import render_stem_module
from modules.danh_cho_giao_vien.rubric.rubric_builder import render_rubric_module
def render_module():
    st.markdown("## 👨‍🏫 Phân hệ: Hỗ trợ Giáo viên")
    
    # Khôi phục nguyên bản 7 tab chuẩn của thầy
    tabs = st.tabs([
        "XD KHBD", "XD Đề KT", "Thiết kế bài dạy STEM", 
        "Rubric", "Chủ nhiệm", "Quản lý điểm", "Tạo prompt"
    ])
    
    with tabs[0]:
        render_khbd_module()
        
    with tabs[1]:
        render_de_kt_module()

    with tabs[2]:
        st.subheader("🧪 Thiết kế bài dạy STEM")
        st.info("⏳ Thầy đang chuẩn bị file stem_builder.py để tích hợp vào đây...")
        render_stem_module()
        
    with tabs[3]:
        st.subheader("📊 Xây dựng Rubric đánh giá")
        st.info("⏳ Giao diện đang được cập nhật...")
        render_rubric_module()
    with tabs[4]:
        st.subheader("📋 Công tác Chủ nhiệm")
        st.info("⏳ Giao diện đang được cập nhật...")
        
    with tabs[5]:
        st.subheader("📈 Quản lý điểm số")
        st.info("⏳ Giao diện đang được cập nhật...")
        
    with tabs[6]:
        st.subheader("💡 Công cụ Tạo prompt")
        st.info("⏳ Giao diện đang được cập nhật...")
