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
        
        # --- TAB 2: XÂY DỰNG ĐỀ KIỂM TRA (ĐÃ ĐỒNG BỘ CẤU HÌNH ĐIỂM ĐỘNG CŨ) ---
    with tabs[1]:
        try:
            # Gọi trực tiếp file cấu hình đề thi cũ của thầy
            from views.exam_tab import ExamTab
            
            # Khởi tạo đối tượng giao diện Tkinter/CustomTkinter cũ tương thích luồng Streamlit
            # Nếu thầy đã chuyển hẳn file exam_tab sang giao diện Streamlit, ta gọi hàm render:
            if hasattr(ExamTab, 'render_exam_module'):
                ExamTab.render_exam_module()
            else:
                # Luồng chạy bọc dự phòng nếu file của thầy vẫn giữ cấu trúc Class
                st.subheader("📝 Xây dựng Đề kiểm tra")
                st.info("Hệ thống đang nạp kho dữ liệu ma trận câu hỏi...")
                
                # Đoạn này sẽ gọi trực tiếp file views/exam_tab.py hoạt động
                import views.exam_tab as exam_mod
                if hasattr(exam_mod, 'render_exam_module'):
                    exam_mod.render_exam_module()
        except Exception as e:
            # Hiển thị thông báo hướng dẫn trực quan nếu file views/exam_tab chưa chuyển đổi sang Streamlit
            st.subheader("📝 Xây dựng Đề kiểm tra")
            st.warning("💡 Để hiển thị khung ma trận cũ trên nền tảng Web mới, tệp 'views/exam_tab.py' cần được chuyển đổi cú pháp từ đồ họa máy tính (customtkinter) sang đồ họa mạng (Streamlit).")

        
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
