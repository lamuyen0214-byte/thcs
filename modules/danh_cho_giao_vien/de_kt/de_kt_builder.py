# File: modules/danh_cho_giao_vien/de_kt/de_kt_builder.py
import streamlit as st
from ai_engine.layer_1_model.gemini import gemini_instance
from ai_engine.layer_3_reasoning.prompt_manager import PromptManager
from ai_engine.layer_5_output.word_export import WordExportEngine

def render_de_kt_module():
    st.subheader("📝 Xây dựng Đề kiểm tra")
    st.markdown("Hệ thống tự động sinh đề kiểm tra và đáp án, đảm bảo chuẩn định dạng công thức KHTN.")

    with st.form("de_kt_form"):
        col1, col2 = st.columns(2)
        with col1:
            mon_hoc = st.selectbox("Môn học:", ["Khoa học Tự nhiên", "Toán học", "Vật lý", "Hóa học"], index=0)
            lop = st.selectbox("Khối lớp:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], index=3)
            chu_de = st.text_input("Chủ đề kiểm tra:", placeholder="Ví dụ: Điện từ học, Di truyền học...")
            
        with col2:
            so_cau_trac_nghiem = st.number_input("Số câu Trắc nghiệm:", min_value=0, max_value=40, value=10)
            so_cau_tu_luan = st.number_input("Số câu Tự luận:", min_value=0, max_value=10, value=2)
            muc_do = st.select_slider("Mức độ khó:", options=["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"], value="Thông hiểu")

        submit_btn = st.form_submit_button("⚙️ Sinh Đề Kiểm Tra")

    if submit_btn:
        if chu_de.strip() == "":
            st.warning("Vui lòng nhập chủ đề kiểm tra.")
        else:
            with st.spinner("AI đang soạn câu hỏi và đáp án..."):
                # Ghép mức độ vào chủ đề để AI hiểu sâu hơn
                chu_de_nang_cao = f"{chu_de} (Tập trung mức độ: {muc_do})"
                sys_inst, prompt = PromptManager.get_de_kt_prompt(mon_hoc, lop, chu_de_nang_cao, so_cau_trac_nghiem, so_cau_tu_luan)
                
                result = gemini_instance.generate_content(prompt, sys_inst)
                
                if result:
                    st.success("✅ Đã tạo xong đề kiểm tra!")
                    with st.expander("Xem trước Đề và Đáp án", expanded=True):
                        st.markdown(result)
                    
                    st.session_state['current_de_kt'] = result

    # Xử lý xuất file Word
    if 'current_de_kt' in st.session_state:
        st.markdown("---")
        col1, col2 = st.columns([1, 3])
        with col1:
            # Ở các bước sau, dữ liệu này sẽ đi qua Layer 4 (Formatting) trước khi gọi Layer 5
            word_file = WordExportEngine.export_to_word(st.session_state['current_de_kt'], title=f"De_Kiem_Tra_{mon_hoc}")
            st.download_button(
                label="📄 Tải xuống Đề (Word)",
                data=word_file,
                file_name="De_Kiem_Tra_KHTN.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
