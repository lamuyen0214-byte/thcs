import streamlit as st
from ai_engine.layer_3_reasoning.prompt_manager import PromptManager

def get_word_engine():
    try:
        from export.word_export import WordExportEngine
        return WordExportEngine
    except Exception:
        return None

def render_stem_module():
    st.subheader("🛠️ Công Cụ Thiết Kế Bài Dạy STEM")
    st.markdown("Xây dựng kịch bản dự án STEM chi tiết, tích hợp kiến thức liên môn và ứng dụng thực tiễn.")
    
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
            placeholder="Ví dụ: Thiết kế hoạt động phù hợp cho học sinh..."
        )
        submit_btn = st.form_submit_button("🚀 Khởi tạo kịch bản STEM")
    if submit_btn:
        if chu_de.strip() == "":
            st.warning("Vui lòng nhập chủ đề dự án STEM.")
        else:
            # ĐỒNG BỘ: Gọi biến client chứa API Key cá nhân AQ... từ file cấu hình độc lập
            from ai_config import get_ai_client
            gemini_client = get_ai_client()
            
            if not gemini_client:
                st.error("⚠️ Lỗi xác thực: Vui lòng cấu hình nhập API Key cá nhân ở thanh bên (Sidebar) trước!")
            else:
                with st.spinner("🤖 Trợ lý AI đang xây dựng kịch bản bài dạy STEM..."):
                    try:
                        sys_inst, prompt = PromptManager.get_stem_prompt(chu_de, mon_hoc, lop, yeu_cau_dac_biet)
                        
                        # Sử dụng SDK mới kết nối trực tiếp bằng gemini_client
                        response = gemini_client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[sys_inst, prompt]
                        )
                        result = response.text
                        
                        if result:
                            st.success("✅ Đã tạo xong kịch bản bài dạy!")
                            with st.expander("Xem trước Nội dung bài dạy STEM", expanded=True):
                                st.markdown(result)
                            st.session_state['current_stem_content'] = result
                    except Exception as api_err:
                        st.error(f"❌ Lỗi máy chủ Google từ chối truy cập: {api_err}")

    if 'current_stem_content' in st.session_state:
        st.markdown("---")
        st.subheader("📥 Xuất Dữ Liệu Văn Bản")
        WordEngine = get_word_engine()
        if WordEngine:
            try:
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
