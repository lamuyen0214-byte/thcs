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
    # 2. Xử lý nghiệp vụ gọi mô hình ngôn ngữ lớn khi bấm nút
    if submit_btn:
        if ten_bai.strip() == "":
            st.warning("Vui lòng nhập tên bài học cần soạn giáo án.")
        else:
            # ĐỒNG BỘ BẢO MẬT: Gọi client chứa Key động định dạng AQ... mới từ file cấu hình độc lập
            from ai_config import get_ai_client
            gemini_client = get_ai_client()
            
            if not gemini_client:
                st.error("⚠️ Lỗi xác thực: Vui lòng cấu hình nhập API Key cá nhân ở thanh bên (Sidebar) trước!")
            else:
                with st.spinner("🤖 Trợ lý AI đang nghiên cứu tài liệu và soạn thảo tiến trình 5512..."):
                    try:
                        # Gọi PromptManager để trích xuất hệ thống câu lệnh giáo án cốt cán
                        sys_inst, prompt = PromptManager.get_khbd_prompt(
                            ten_bai, mon_hoc, lop, thoi_luong, noi_dung_tich_hop
                        )
                        
                        # SDK mới yêu cầu truyền tham số qua đối tượng Client đồng bộ
                        response = gemini_client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[sys_inst, prompt]
                        )
                        result = response.text
                        
                        if result:
                            st.success("✅ Đã soạn thảo xong Kế hoạch bài dạy chi tiết!")
                            with st.expander("Xem trước Tiến trình Giáo án chi tiết (Chuẩn 5512)", expanded=True):
                                st.markdown(result)
                            
                            # Lưu trữ văn bản giáo án vào bộ nhớ phiên Streamlit
                            st.session_state['current_khbd_content'] = result
                    except Exception as api_err:
                        st.error(f"❌ Máy chủ Google từ chối quyền truy cập hoặc lỗi Quota: {api_err}")

    # 3. Phân hệ tải file Word in ấn hành chính
    if 'current_khbd_content' in st.session_state:
        st.markdown("---")
        st.subheader("📥 Kết Xuất Hồ Sơ Giáo Án")
        
        WordEngine = get_word_engine()
        if WordEngine:
            try:
                word_file = WordEngine.export_to_word(st.session_state['current_khbd_content'])
                st.download_button(
                    label="📄 Tải xuống giáo án Word (.docx)",
                    data=word_file,
                    file_name=f"Giao_An_5512_{ten_bai.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as doc_err:
                st.error(f"⚠️ Trình xuất file Word đang được cập nhật: {doc_err}")
        else:
            st.info("💡 Hệ thống đang khởi tạo biểu mẫu văn bản hành chính dự phòng.")
