# File: modules/danh_cho_giao_vien/khbd/khbd_builder.py
import streamlit as st
from ai_engine.layer_1_model.gemini import gemini_instance
from ai_engine.layer_3_reasoning.prompt_manager import PromptManager
from ai_engine.layer_5_output.word_export import WordExportEngine

def render_khbd_module():
    st.subheader("📚 Xây dựng Kế hoạch bài dạy (KHBD)")
    st.markdown("Hệ thống tự động sinh KHBD chuẩn Công văn 5512, hỗ trợ tích hợp các chủ đề chuyên sâu.")

    with st.form("khbd_form"):
        col1, col2 = st.columns(2)
        with col1:
            mon_hoc = st.selectbox("Môn học:", ["Khoa học Tự nhiên", "Vật lý", "Hóa học", "Sinh học"])
            lop = st.selectbox("Khối lớp:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], index=3) # Mặc định để Lớp 9
            thoi_luong = st.number_input("Thời lượng (Số tiết):", min_value=1, max_value=5, value=1)
        
        with col2:
            ten_bai = st.text_input("Tên bài học/Chủ đề:", placeholder="Ví dụ: Đo điện năng tiêu thụ, Phản ứng oxi hóa khử...")
            noi_dung_tich_hop = st.multiselect(
                "Nội dung giáo dục tích hợp:",
                ["Trí tuệ nhân tạo (AI)", "Hệ thống tự động hóa / IoT", "Tiết kiệm năng lượng", "Giáo dục môi trường"],
                default=["Trí tuệ nhân tạo (AI)"]
            )
            
        submit_btn = st.form_submit_button("📝 Soạn KHBD")

    if submit_btn:
        if ten_bai.strip() == "":
            st.warning("Vui lòng nhập tên bài học.")
        else:
            with st.spinner("Đang xây dựng tiến trình dạy học..."):
                sys_inst, prompt = PromptManager.get_khbd_prompt(ten_bai, mon_hoc, lop, thoi_luong, noi_dung_tich_hop)
                result = gemini_instance.generate_content(prompt, sys_inst)
                
                if result:
                    st.success("✅ Đã hoàn thành Kế hoạch bài dạy!")
                    with st.expander("Xem trước Giáo án", expanded=True):
                        st.markdown(result)
                    
                    st.session_state['current_khbd_content'] = result

    # Xử lý xuất file Word
    if 'current_khbd_content' in st.session_state:
        st.markdown("---")
        st.subheader("📥 Xuất Hồ sơ")
        word_file = WordExportEngine.export_to_word(st.session_state['current_khbd_content'], title=f"KHBD")
        
        st.download_button(
            label="📄 Tải xuống Giáo án (Word)",
            data=word_file,
            file_name="KHBD_KhoaHocTuNhien.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
