# =====================================================================
# FILE: core/router.py (CẤU TRÚC ĐỊNH TUYẾN DỘNG AN TOÀN TRÁNH LỖI CACHE)
# =====================================================================
import streamlit as st
import sys
import os

# Bảo đảm thư mục gốc luôn nằm trong luồng tìm kiếm của hệ thống
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

def route_teacher():
    st.header("👨‍🏫 Phân hệ: Dành Cho Giáo Viên")
    
    # Khởi tạo chuẩn 7 tab chức năng sư phạm
    tabs = st.tabs([
        "XD KHBD", "XD Đề KT", "Thiết kế bài dạy STEM", 
        "Rubric", "Chủ nhiệm", "Quản lý điểm", "Tạo prompt"
    ])
    
    # --- TAB 1: XÂY DỰNG KẾ HOẠCH BÀI DẠY (KHBD) ---
    with tabs[0]:
        try:
            from modules.danh_cho_giao_vien.khbd.khbd_builder import render_khbd_module
            render_khbd_module()
        except Exception as e:
            st.error(f"💡 Hệ thống đang đồng bộ Tab KHBD: {e}")
        
        # --- TAB 2: XÂY DỰNG ĐỀ KIỂM TRA (ĐÃ ĐỒNG BỘ MODULE ĐỒ HỌA MÀU SẮC CỦA THẦY) ---
    with tabs[1]:
        try:
            # Gọi trực tiếp hàm render_de_kt_module từ file de_kt_builder.py
            from modules.danh_cho_giao_vien.de_kt.de_kt_builder import render_de_kt_module
            render_de_kt_module()
        except KeyError:
            import modules.danh_cho_giao_vien.de_kt.de_kt_builder as de_kt_mod
            de_kt_mod.render_de_kt_module()
        except Exception as e:
            st.error(f"💡 Hệ thống đang đồng bộ Tab Đề kiểm tra: {e}")
        
    # --- TAB 3: THIẾT KẾ BÀI DẠY STEM ---
    with tabs[2]:
        try:
            from modules.danh_cho_giao_vien.stem.stem_builder import render_stem_module
            render_stem_module()
        except Exception as e:
            st.error(f"💡 Hệ thống đang đồng bộ Tab STEM: {e}")
        
    # --- CÁC TAB KHÁC DỰ PHÒNG GIỮ NGUYÊN KHUNG ---
    with tabs[3]:
        st.subheader("📊 Xây dựng Rubric đánh giá")
    with tabs[4]:
        st.subheader("📋 Công tác Chủ nhiệm")
    with tabs[5]:
        st.subheader("📈 Quản lý điểm số")
    with tabs[6]:
        st.subheader("💡 Công cụ Tạo prompt")
