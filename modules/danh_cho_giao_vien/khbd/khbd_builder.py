import streamlit as st
from ai_engine.layer_3_reasoning.prompt_manager import PromptManager

# SỬA LỖI ĐƯỜNG DẪN: Hàm bọc tìm kiếm module xuất file Word động
def get_word_engine():
    try:
        # Thử nạp từ thư mục export thực tế của thầy thay vì ai_engine cũ
        from export.word_export import WordExportEngine
        return WordExportEngine
    except Exception:
        return None

def render_khbd_module():
    st.subheader("📚 Xây dựng Kế hoạch bài dạy (KHBD 5512)")
    st.markdown("Soạn thảo giáo án chi tiết theo chuẩn Công văn 5512 của Bộ Giáo dục và Đào tạo.")
    
    # 1. Khung biểu mẫu thu thập thông số giáo án sư phạm
    with st.form("khbd_form"):
        col1, col2 = st.columns(2)
        with col1:
            mon_hoc = st.selectbox("Môn học giảng dạy:", ["Khoa học Tự nhiên", "Vật lý", "Hóa học", "Sinh học"])
            lop = st.selectbox("Khối lớp phổ thông:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], index=1)
            thoi_luong = st.number_input("Thời lượng bài dạy (tiết):", min_value=1, max_value=6, value=2)
        
        with col2:
            ten_bai = st.text_input("Tên bài học / Tiết dạy chủ đề:", value="Tốc độ và đo tốc độ")
            
        # Chọn nội dung tích hợp liên môn phát triển phẩm chất
        noi_dung_tich_hop = st.multiselect(
            "Nội dung cần tích hợp phát triển năng lực:",
            ["Giáo dục bảo vệ môi trường", "Ứng dụng công nghệ thực tiễn", "Kĩ năng thực hành thí nghiệm", "An toàn giao thông đời sống"],
            default=["Ứng dụng công nghệ thực tiễn"]
        )
        
        submit_btn = st.form_submit_button("🚀 Khởi tạo giáo án chuẩn 5512")
