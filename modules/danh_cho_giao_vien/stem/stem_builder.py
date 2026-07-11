# File: modules/danh_cho_giao_vien/stem/stem_builder.py
import streamlit as st
from ai_engine.layer_1_model.gemini import gemini_instance
from ai_engine.layer_3_reasoning.prompt_manager import PromptManager

def render_stem_module():
    st.subheader("🛠️ Công Cụ Thiết Kế Bài Dạy STEM")
    st.markdown("Xây dựng kịch bản dự án STEM chi tiết, tích hợp kiến thức liên môn và ứng dụng thực tiễn.")
    
    # 1. Khu vực nhập liệu
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
            placeholder="Ví dụ: Cần thiết kế thêm các hoạt động hoặc câu hỏi điều chỉnh phù hợp cho học sinh khuyết tật tham gia..."
        )
        
        submit_btn = st.form_submit_button("🚀 Khởi tạo kịch bản STEM")

    # 2. Xử lý logic khi bấm nút
    if submit_btn:
        if chu_de.strip() == "":
            st.warning("Vui lòng nhập chủ đề dự án STEM.")
        else:
            with st.spinner("AI đang phân tích và xây dựng kịch bản..."):
                # Gọi Lớp 3 để lấy prompt chuẩn
                sys_inst, prompt = PromptManager.get_stem_prompt(
                    chu_de, mon_hoc, lop, yeu_cau_dac_biet
                )
                
                # Gọi Lớp 1 (Gemini) để sinh nội dung
                result = gemini_instance.generate_content(prompt, sys_inst)
                
                if result:
                    st.success("✅ Đã tạo xong kịch bản bài dạy!")
                    
                    # Hiển thị kết quả trong một khung chứa
                    with st.expander("Xem trước Nội dung bài dạy STEM", expanded=True):
                        st.markdown(result)
                        
                    # Lưu trữ kết quả tạm thời vào session để chờ xuất file Word (chúng ta sẽ làm tính năng xuất file Word sau)
                    st.session_state['current_stem_content'] = result
# File: modules/danh_cho_giao_vien/stem/stem_builder.py
import streamlit as st
from ai_engine.layer_1_model.gemini import gemini_instance
from ai_engine.layer_3_reasoning.prompt_manager import PromptManager
from ai_engine.layer_5_output.word_export import WordExportEngine # Bổ sung dòng import này

def render_stem_module():
    st.subheader("🛠️ Công Cụ Thiết Kế Bài Dạy STEM")
    st.markdown("Xây dựng kịch bản dự án STEM chi tiết, tích hợp kiến thức liên môn và ứng dụng thực tiễn.")
    
    # ... (Giữ nguyên phần form nhập liệu phía trên) ...
    with st.form("stem_form"):
        col1, col2 = st.columns(2)
        with col1:
            mon_hoc = st.selectbox("Môn học chủ đạo:", ["Khoa học Tự nhiên", "Toán học", "Tin học", "Công nghệ"])
            lop = st.selectbox("Khối lớp:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], index=3)
        with col2:
            chu_de = st.text_input("Chủ đề / Tên dự án STEM:", value="Hệ thống tiết kiệm năng lượng thông minh sử dụng vi điều khiển ESP8266")
        yeu_cau_dac_biet = st.text_area("Yêu cầu bổ sung (Tùy chọn):")
        submit_btn = st.form_submit_button("🚀 Khởi tạo kịch bản STEM")

    if submit_btn:
        if chu_de.strip() == "":
            st.warning("Vui lòng nhập chủ đề dự án STEM.")
        else:
            with st.spinner("AI đang phân tích và xây dựng kịch bản..."):
                sys_inst, prompt = PromptManager.get_stem_prompt(chu_de, mon_hoc, lop, yeu_cau_dac_biet)
                result = gemini_instance.generate_content(prompt, sys_inst)
                
                if result:
                    st.success("✅ Đã tạo xong kịch bản bài dạy!")
                    with st.expander("Xem trước Nội dung bài dạy STEM", expanded=True):
                        st.markdown(result)
                    
                    # Lưu vào session_state để không bị mất khi giao diện tải lại
                    st.session_state['current_stem_content'] = result

    # --- PHẦN BỔ SUNG: XỬ LÝ XUẤT FILE WORD ---
    if 'current_stem_content' in st.session_state:
        st.markdown("---")
        st.subheader("📥 Xuất Dữ Liệu")
        
        # Gọi Lớp 5 để tạo file Word
        word_file = WordExportEngine.export_to_word(st.session_state['current_stem_content'])
        
        # Nút tải xuống của Streamlit
        st.download_button(
            label="📄 Tải xuống file Word",
            data=word_file,
            file_name="Kich_Ban_STEM_KHTN.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
