import streamlit as st
# Nhập các module đã được di chuyển vào đúng vị trí mới
from modules.danh_cho_giao_vien.khbd.khbd_builder import render_khbd_module
from modules.danh_cho_giao_vien.de_kt.de_kt_builder import render_de_kt_module

def render_module():
    st.header("👨‍🏫 Phân hệ: Hỗ trợ Giáo viên")
    
    # Chia tab để giao diện không bị quá tải
    tab1, tab2, tab3 = st.tabs(["Xây dựng KHBD", "Xây dựng Đề KT", "Tiện ích khác"])
    
    with tab1:
        render_khbd_module()
    
    with tab2:
        render_de_kt_module()
        
    with tab3:
        st.write("Các tính năng khác (STEM, Rubric...) sẽ được tích hợp tiếp theo.")
