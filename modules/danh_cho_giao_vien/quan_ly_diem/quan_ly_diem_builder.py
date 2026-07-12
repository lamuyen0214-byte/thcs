# =====================================================================
# FILE: modules/danh_cho_giao_vien/quan_ly_diem/quan_ly_diem_builder.py
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
        return None

def render_quan_ly_diem_module():
    st.markdown("""
        <style>
        .header-blue {color: #0000FF; font-weight: bold; font-size: 15px; text-align: left; margin-bottom: 2px;}
        .box-grading {background-color: #E6E6FA; padding: 15px; border-radius: 8px; border-left: 5px solid #9370DB; margin-bottom: 15px;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="box-grading">📈 <b>Trợ lý Khảo thí & Học vụ:</b> Tự động phân tích phổ điểm, đánh giá năng lực lớp học và đề xuất kế hoạch bồi dưỡng/phụ đạo học sinh.</div>', unsafe_allow_html=True)

    # 1. CẤU HÌNH THÔNG SỐ
    col1, col2 = st.columns(2)
    with col1:
        mon_hoc = st.selectbox("Môn học:", ["Khoa học tự nhiên", "Toán", "Vật lý", "Hóa học", "Sinh học", "Ngữ văn", "Tiếng Anh"], index=0)
    with col2:
        lop = st.selectbox("Khối lớp:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], index=3)

    st.markdown('<p class="header-blue">Dán dữ liệu điểm số của lớp (Copy từ Excel/Word):</p>', unsafe_allow_html=True)
    du_lieu_diem = st.text_area(
        "Dữ liệu điểm", 
        placeholder="""Ví dụ copy/paste thẳng từ cột Excel:
Nguyễn Văn A: 8.5
Trần Thị B: 4.5
Lê Văn C: 9.0
Phạm Thị D: 3.0 (HS khuyết tật học hòa nhập)
...""", 
        height=150, label_visibility="collapsed"
    )

    st.markdown('<p class="header-blue">Yêu cầu phân tích cụ thể (Tùy chọn):</p>', unsafe_allow_html=True)
    yeu_cau_them = st.text_input("Yêu cầu thêm", placeholder="Ví dụ: Đề xuất phương pháp học trực quan giúp nhóm dưới trung bình hiểu bài tốt hơn...", label_visibility="collapsed")

    # 2. XỬ LÝ AI
    if st.button("🚀 PHÂN TÍCH VÀ LẬP BÁO CÁO THỐNG KÊ", type="primary", use_container_width=True):
        if not du_lieu_diem.strip():
            st.warning("⚠️ Thầy/Cô vui lòng dán dữ liệu điểm vào khung trống trước khi phân tích.")
            return

        user_raw_key = st.session_state.get("user_gemini_key", "").strip()
        if not user_raw_key:
            if "GEMINI_API_KEY" in st.secrets: user_raw_key = st.secrets["GEMINI_API_KEY"].strip()
        if not user_raw_key:
            st.error("⚠️ Lỗi cấu hình: Vui lòng nhập Gemini API Key ở thanh bên (Sidebar) trước!")
            return

        with st.spinner("🤖 AI đang tính toán phổ điểm và lập báo cáo chuyên sâu..."):
            from google import genai
            try:
                client = genai.Client(api_key=str(user_raw_key))
                
                prompt_he_thong = f"""
Bạn là một Chuyên gia Dữ liệu Giáo dục và là Giáo viên giỏi. Hãy phân tích bảng điểm môn {mon_hoc} của {lop} dưới đây:

DỮ LIỆU ĐIỂM:
{du_lieu_diem}

Yêu cầu cụ thể từ giáo viên: {yeu_cau_them if yeu_cau_them else "Phân tích chung và đề xuất giải pháp."}

Hãy xuất ra một Báo cáo Phân tích chất lượng học tập với cấu trúc Markdown như sau:
1. **Thống kê tổng quan:** Tổng số HS, điểm trung bình lớp, tỷ lệ % các mức điểm (Giỏi, Khá, TB, Yếu/Kém). Trình bày bằng BẢNG MARKDOWN.
2. **Phân tích phổ điểm & Nhận định:** Đánh giá chung về mức độ nắm bắt kiến thức của học sinh.
3. **Nhận diện nhóm học sinh:** Lọc ra danh sách nhóm HS xuất sắc cần bồi dưỡng thêm và nhóm HS dưới trung bình cần quan tâm đặc biệt.
4. **Đề xuất Kế hoạch hành động:** Đưa ra 3 giải pháp sư phạm cụ thể để cải thiện điểm số cho nhóm yếu (chú trọng tính khả thi và các phương pháp hỗ trợ giáo dục hòa nhập nếu có).
                """
                
                response = client.models.generate_content(
                    model="models/gemini-2.5-flash",
                    contents=prompt_he_thong
                )
                
                if response and response.text:
                    st.session_state['current_grading_data'] = {
                        "is_khbd": True, # Mượn cờ True để xuất Word giữ nguyên định dạng bảng
                        "title": f"Báo Cáo Phân Tích Điểm - {mon_hoc} {lop}",
                        "subject": mon_hoc,
                        "grade": lop,
                        "ten_bai_save": "Bao_Cao_Phan_Tich_Diem",
                        "ai_generated_content": response.text
                    }
                    st.success("✅ Đã hoàn tất phân tích và lập báo cáo!")
            except Exception as api_err:
                st.error(f"❌ Lỗi máy chủ AI: {api_err}")

    # 3. KẾT XUẤT WORD
    st.markdown("---")
    grading_cache = st.session_state.get('current_grading_data')
    if grading_cache:
        with st.expander("🔍 Xem trước Báo cáo Phân tích", expanded=True):
            st.markdown(grading_cache["ai_generated_content"])
            
        WordEngine = get_word_engine()
        word_file = None
        if WordEngine:
            try:
                word_file = WordEngine.export_to_word(grading_cache)
            except Exception as e:
                st.error(f"⚠️ Lỗi xuất Word: {e}")

        col_dl, col_del = st.columns(2)
        with col_dl:
            if word_file:
                st.download_button(
                    label="📄 Tải Báo cáo (Word)", 
                    data=word_file, 
                    file_name="Bao_Cao_Phan_Tich_Diem.docx", 
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            else:
                st.button("📄 Tải Báo cáo (Đang xử lý)", disabled=True, use_container_width=True)
                
        with col_del:
            if st.button("❌ Xóa bản nháp", use_container_width=True):
                del st.session_state['current_grading_data']
                st.rerun()
