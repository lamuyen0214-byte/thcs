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
        
    # --- TAB 2: XÂY DỰNG ĐỀ KIỂM TRA (ĐÃ ĐỒNG BỘ ĐƯỜNG DẪN THỰC TẾ) ---
    with tabs[1]:
        try:
            # Chỉ định Python nạp trực tiếp hàm render_exam_module từ thư mục views
            from views.exam_tab import render_exam_module
            render_exam_module()
        except KeyError:
            # Khử lỗi bộ nhớ đệm cache ngầm của Streamlit Cloud bằng import alias trực tiếp
            import views.exam_tab as exam_mod
            exam_mod.render_exam_module()
        except Exception as e:
            st.error(f"💡 Hệ thống đang khởi tạo dữ liệu Tab Đề kiểm tra: {e}")
        
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
