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
        except KeyError:
            # Biện pháp cưỡng ép nạp trực tiếp nếu Streamlit Cloud bị kẹt KeyError module
            import modules.danh_cho_giao_vien.khbd.khbd_builder as khbd_mod
            khbd_mod.render_khbd_module()
        except Exception as e:
            st.error(f"💡 Hệ thống đang đồng bộ Tab KHBD: {e}")
        
    # --- TAB 2: XÂY DỰNG ĐỀ KIỂM TRA ---
    with tabs[1]:
        st.subheader("Xây dựng Đề kiểm tra")
        st.write("Giao diện sinh đề, trộn đề và xuất file Word chuẩn định dạng Toán, Lý, Hóa.")
        
    # --- TAB 3: THIẾT KẾ BÀI DẠY STEM ---
    with tabs[2]:
        try:
            from modules.danh_cho_giao_vien.stem.stem_builder import render_stem_module
            render_stem_module()
        except KeyError:
            # Biện pháp cưỡng ép nạp trực tiếp nếu Streamlit Cloud bị kẹt KeyError module
            import modules.danh_cho_giao_vien.stem.stem_builder as stem_mod
            stem_mod.render_stem_module()
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
