import streamlit as st

# Giả định import các module điều hướng từ thư mục core
# (Chúng ta sẽ viết code chi tiết cho các file này ở bước sau)
# from core.router import route_teacher, route_teaching_support, route_management
# from ui.sidebar import render_sidebar
# from ui.theme import apply_custom_theme

def main():
    # 1. Cấu hình trang cơ bản
    st.set_page_config(
        page_title="Hệ Sinh Thái Giáo Dục Khoa Học Tự Nhiên & STEM",
        page_icon="⚛️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 2. Áp dụng giao diện (CSS custom)
    # apply_custom_theme()

    # 3. Render Thanh điều hướng (Sidebar)
    # selected_module = render_sidebar()
    
    # Tạm thời tạo thanh sidebar giả lập để test khung
    with st.sidebar:
        st.title("⚙️ Bảng Điều Khiển")
        selected_module = st.radio(
            "Chọn phân hệ làm việc:",
            ["Dành cho giáo viên", "Hỗ trợ giảng dạy", "Quản lý tổ chuyên môn"]
        )
        st.markdown("---")
        st.info("Phiên bản v1.0 - Kiến trúc 5 lớp AI")

    # 4. Điều hướng (Routing) dựa trên lựa chọn ở Sidebar
    if selected_module == "Dành cho giáo viên":
        st.title("👨‍🏫 Phân hệ: Dành Cho Giáo Viên")
        st.write("Tích hợp các công cụ xây dựng KHBD, bài giảng STEM và thiết kế đề kiểm tra.")
        # route_teacher() 
        
    elif selected_module == "Hỗ trợ giảng dạy":
        st.title("🤖 Phân hệ: Hỗ Trợ Giảng Dạy")
        st.write("Tích hợp AI RAG, mô phỏng thí nghiệm và phân tích dữ liệu học tập.")
        # route_teaching_support()
        
    elif selected_module == "Quản lý tổ chuyên môn":
        st.title("📊 Phân hệ: Quản Lý Tổ Chuyên Môn")
        st.write("Không gian số quản lý kế hoạch và phân công chuyên môn.")
        # route_management()

if __name__ == "__main__":
    main()
