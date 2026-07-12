# =====================================================================
# FILE: modules/danh_cho_giao_vien/rubric/rubric_builder.py
# =====================================================================
import streamlit as st
import os
import sys

# Đảm bảo hệ thống tìm thấy thư mục export
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

def get_word_engine():
    try:
        from export.export_word import WordExportEngine
        return WordExportEngine
    except Exception as e:
        st.error(f"Lỗi nạp module kết xuất Word: {e}")
        return None

def render_rubric_module():
    st.markdown("""
        <style>
        .header-blue {color: #0000FF; font-weight: bold; font-size: 15px; text-align: left; margin-bottom: 2px;}
        .header-red-title {color: #FF0000; font-weight: bold; font-size: 16px; margin-bottom: 5px;}
        .box-rubric {background-color: #D5E8D4; padding: 15px; border-radius: 8px; border-left: 5px solid #82B366; margin-bottom: 15px;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="box-rubric">📊 <b>Chuyên gia Khảo thí:</b> Khởi tạo bảng Rubric đánh giá đa chiều cho các dự án học tập, bài thuyết trình hoặc sản phẩm thực hành.</div>', unsafe_allow_html=True)

    # KHUNG NHẬP LIỆU
    st.markdown('<p class="header-red-title">Tên nhiệm vụ / Sản phẩm cần đánh giá:</p>', unsafe_allow_html=True)
    ten_nhiem_vu = st.text_input("Nhiệm vụ", placeholder="Ví dụ: Đánh giá dự án thiết kế hệ thống tiết kiệm điện thông minh...", label_visibility="collapsed")

    col1, col2, col3 = st.columns([1.5, 1.5, 2])
    with col1:
        st.markdown('<p class="header-blue">Môn học:</p>', unsafe_allow_html=True)
        mon_hoc = st.selectbox("Môn học Rubric", ["Khoa học tự nhiên", "Vật lý", "Hóa học", "Sinh học", "Toán", "Công nghệ"], label_visibility="collapsed", index=0)
    with col2:
        st.markdown('<p class="header-blue">Đối tượng:</p>', unsafe_allow_html=True)
        lop = st.selectbox("Lớp Rubric", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], label_visibility="collapsed", index=3)
    with col3:
        st.markdown('<p class="header-blue">Thang điểm:</p>', unsafe_allow_html=True)
        thang_diem = st.selectbox("Thang điểm", ["Thang điểm 10", "Thang điểm 100", "Theo mức độ (Tốt, Khá, Đạt, CĐ)"], label_visibility="collapsed", index=0)

    st.markdown('<p class="header-blue">Các tiêu chí trọng tâm (Tùy chọn):</p>', unsafe_allow_html=True)
    tieu_chi = st.text_area("Tiêu chí", placeholder="Ví dụ: Tính sáng tạo, Hoạt động nhóm, Khả năng ứng dụng thực tế, Trình bày báo cáo...", height=70, label_visibility="collapsed")

    st.write("")

    # XỬ LÝ AI VỚI KEY THÔ BỀN BỈ
    if st.button("🚀 TỰ ĐỘNG LẬP BẢNG RUBRIC", type="primary", use_container_width=True):
        if not ten_nhiem_vu.strip():
            st.warning("⚠️ Vui lòng nhập 'Tên nhiệm vụ' trước khi khởi tạo.")
            return

        user_raw_key = st.session_state.get("user_gemini_key", "").strip()
        if not user_raw_key:
            if "GEMINI_API_KEY" in st.secrets: user_raw_key = st.secrets["GEMINI_API_KEY"].strip()
        if not user_raw_key:
            st.error("⚠️ Lỗi cấu hình: Vui lòng nhập Gemini API Key ở thanh bên (Sidebar) trước!")
            return

        with st.spinner("🤖 AI đang phân tích tiêu chí và lập ma trận đánh giá..."):
            from google import genai
            try:
                client = genai.Client(api_key=str(user_raw_key))
                
                system_instruction = f"""
Bạn là Chuyên gia Đo lường và Đánh giá Giáo dục. Nhiệm vụ của bạn là thiết kế một bảng Rubric đánh giá chi tiết cho môn {mon_hoc} {lop}.
Nhiệm vụ/Sản phẩm học sinh cần thực hiện: {ten_nhiem_vu}.
Thang điểm áp dụng: {thang_diem}.
Các tiêu chí trọng tâm cần có: {tieu_chi if tieu_chi else 'Kiến thức chuyên môn, Kỹ năng thực hành, Trình bày & Thái độ'}.

Yêu cầu định dạng đầu ra:
1. Mô tả ngắn gọn mục đích của bảng Rubric này.
2. Trình bày Rubric dưới dạng **BẢNG MARKDOWN**. Các cột bao gồm: Tiêu chí, Trọng số (%), và 4 mức độ đạt được (Tốt, Khá, Đạt, Cần cố gắng) với mô tả hành vi cụ thể cho từng mức độ.
3. Cung cấp một biểu mẫu nhỏ để giáo viên ghi chú nhanh.
                """
                
                response = client.models.generate_content(
                    model="models/gemini-2.5-flash",
                    contents=system_instruction
                )
                
                if response and response.text:
                    st.session_state['current_rubric_data'] = {
                        "is_khbd": False, # Để xuất dưới dạng bảng ma trận Word
                        "custom_req": ten_nhiem_vu,
                        "ai_generated_content": response.text
                    }
                    st.success("✅ Đã khởi tạo bảng Rubric thành công!")
            except Exception as api_err:
                st.error(f"❌ Lỗi máy chủ AI: {api_err}")

    # KẾT XUẤT WORD
    st.markdown("---")
    rubric_cache = st.session_state.get('current_rubric_data')
    if rubric_cache:
        with st.expander("🔍 Xem trước Bảng Rubric Đánh Giá", expanded=True):
            st.markdown(rubric_cache["ai_generated_content"])
            
        WordEngine = get_word_engine()
        word_file = None
        if WordEngine:
            try:
                word_file = WordEngine.export_to_word(rubric_cache)
            except Exception as e:
                pass

        col_dl, col_del = st.columns(2)
        with col_dl:
            if word_file:
                st.download_button("📄 Tải Rubric (Word)", data=word_file, file_name="Rubric_Danh_Gia.docx", use_container_width=True)
        with col_del:
            if st.button("❌ Xóa bản nháp", use_container_width=True):
                del st.session_state['current_rubric_data']
                st.rerun()
