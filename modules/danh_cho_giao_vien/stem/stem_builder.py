import streamlit as st
from ai_engine.layer_1_model.gemini import gemini_instance
from ai_engine.layer_3_reasoning.prompt_manager import PromptManager

# Thêm hàm bọc an toàn để xử lý import động tránh sập ứng dụng do lỗi cache
def get_word_engine():
    try:
        from ai_engine.layer_5_output.word_export import WordExportEngine
        return WordExportEngine
    except Exception:
        return None

def render_stem_module():
    st.subheader("🛠️ Công Cụ Thiết Kế Bài Dạy STEM")
    st.markdown("Xây dựng kịch bản dự án STEM chi tiết, tích hợp kiến thức liên môn và ứng dụng thực tiễn.")
    
    # 1. Khu vực form cấu hình thông số dự án liên môn
    with st.form("stem_form"):
        col1, col2 = st.columns(2)
        with col1:
            mon_hoc = st.selectbox("Môn học chủ đạo:", ["Khoa học Tự nhiên", "Toán học", "Tin học", "Công nghệ"])
            lop = st.selectbox("Khối lớp:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], index=3)
        
        with col2:
            chu_de = st.text_input(
                "Chủ đề / Tên dự án STEM:", 
                value="Hệ thống tiết kiệm năng lượng thông minh sử dụng vi điều khiển ESP8266"
            )
            
        yeu_cau_dac_biet = st.text_area(
            "Yêu cầu bổ sung (Tùy chọn):", 
            placeholder="Ví dụ: Cần thiết kế thêm các hoạt động phù hợp..."
        )
        
        submit_btn = st.form_submit_button("🚀 Khởi tạo kịch bản STEM")
        # 2. Xử lý logic nghiệp vụ khi giáo viên bấm nút kích hoạt
    if submit_btn:
        if chu_de.strip() == "":
            st.warning("Vui lòng nhập chủ đề dự án STEM.")
        else:
            # ĐÃ SỬA: Gọi biến client chứa Key động cá nhân (Định dạng AQ...) từ file cấu hình độc lập
            from ai_config import get_ai_client
            gemini_client = get_ai_client()
            
            if not gemini_client:
                st.error("⚠️ Lỗi xác thực: Vui lòng nhập hoặc kiểm tra lại API Key ở thanh bên (Sidebar)!")
            else:
                with st.spinner("🤖 Chuyên gia AI đang phân tích tài liệu và xây dựng kịch bản bài dạy STEM..."):
                    try:
                        # SDK google-genai mới yêu cầu truyền tham số qua Client và Model cụ thể
                        response = gemini_client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[sys_inst, prompt] # Nạp cả câu lệnh hệ thống và nội dung yêu cầu
                        )
                        result = response.text
                        
                        if result:
                            st.success("✅ Đã tạo xong kịch bản bài dạy!")
                            with st.expander("Xem trước Nội dung bài dạy STEM", expanded=True):
                                st.markdown(result)
                            
                            # Khóa chặt kết quả vào bộ đệm phiên làm việc của Streamlit
                            st.session_state['current_stem_content'] = result
                    except Exception as api_err:
                        # Bắt lỗi 401 hoặc hiển thị thông báo tường minh nếu khóa hết hạn mức
                        st.error(f"❌ Máy chủ Google từ chối truy cập hoặc sai định dạng Key: {api_err}")

    # 3. Phân hệ kết xuất tệp Word in ấn (Định dạng lề trang chuẩn hành chính)
    if 'current_stem_content' in st.session_state:
        st.markdown("---")
        st.subheader("📥 Xuất Dữ Liệu Văn Bản")
        
        WordEngine = get_word_engine()
        if WordEngine:
            try:
                # Tạo file docx từ nội dung chữ thô sạch ký tự rác Markdown
                word_file = WordEngine.export_to_word(st.session_state['current_stem_content'])
                
                st.download_button(
                    label="📄 Tải xuống file Word thiết kế STEM",
                    data=word_file,
                    file_name=f"Kich_Ban_STEM_{lop.replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as doc_err:
                st.error(f"⚠️ Trình xuất Word đang được cập nhật: {doc_err}")
        else:
            st.info("💡 Hệ thống đang khởi tạo module xuất bản văn bản Word dự phòng.")
