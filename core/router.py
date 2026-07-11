import streamlit as st
from modules.danh_cho_giao_vien.stem.stem_builder import render_stem_module
def route_teacher():
    st.header("👨‍🏫 Phân hệ: Dành Cho Giáo Viên")
    tabs = st.tabs([
        "XD KHBD", "XD Đề KT", "Thiết kế bài dạy STEM", 
        "Rubric", "Chủ nhiệm", "Quản lý điểm", "Tạo prompt"
    ])
    
    with tabs[0]:
        st.subheader("Xây dựng Kế hoạch bài dạy (KHBD)")
        st.write("Module sinh tự động KHBD môn Khoa học Tự nhiên lớp 9 sẽ được kết nối tại đây.")
        
    with tabs[1]:
        st.subheader("Xây dựng Đề kiểm tra")
        st.write("Giao diện sinh đề, trộn đề và xuất file Word chuẩn định dạng Toán, Lý, Hóa.")
        
    with tabs[2]:
        # GỌI MODULE STEM TẠI ĐÂY
        render_stem_module()
    with tabs[3]:
        st.write("Module tạo Rubric đánh giá học sinh.")
    with tabs[4]:
        st.write("Module hỗ trợ công tác chủ nhiệm lớp.")
    with tabs[5]:
        st.write("Module quản lý điểm số.")
    with tabs[6]:
        st.write("Giao diện tùy chỉnh và tạo Prompt cho AI.")


def route_teaching_support():
    st.header("🤖 Phân hệ: Hỗ Trợ Giảng Dạy")
    tabs = st.tabs([
        "Hỏi-Đáp (RAG)", "Trò chơi", "Chấm bài", "Học liệu", "Mô phỏng", 
        "Phân tích", "Ngân hàng đề", "Sinh Video", "Tương tác", "Cá nhân hóa"
    ])
    
    with tabs[0]:
        st.subheader("Hỏi - Đáp theo tài liệu (RAG)")
        st.write("Hệ thống AI truy xuất và trả lời dựa trên kho tài liệu nội bộ.")
    
    with tabs[1]:
        st.write("Module khởi tạo trò chơi học tập.")
    # Các module khác sẽ được kết nối dần vào các tab này...


def route_management():
    st.header("📊 Phân hệ: Quản Lý Tổ Chuyên Môn")
    tabs = st.tabs([
        "Phân công CM", "Sinh hoạt", "Thời khóa biểu", 
        "Kế hoạch Tổ", "Kế hoạch Cá nhân"
    ])
    
    with tabs[0]:
        st.subheader("Quản lý và phân công chuyên môn")
        st.write("Bảng theo dõi tiến độ và phân công nhiệm vụ trong tổ.")
        
    with tabs[1]:
        st.write("Nội dung và biên bản sinh hoạt tổ chuyên môn.")
    # Các module khác sẽ được kết nối dần vào các tab này...
