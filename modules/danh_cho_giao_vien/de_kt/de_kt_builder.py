import streamlit as st
import os
import sys
import docx
from pypdf import PdfReader
from export.export_word import WordExportEngine
from ai_engine.ai_config import get_api_key
from ai_engine.ai_runner import run_ai_with_fallback

def render_de_kt_module(api_key=""):
    st.markdown("""<style>
    .block-container { padding-top: 1rem !important; }
    .stButton>button { height: 2.5em; }
    </style>""", unsafe_allow_html=True)

    # 1. CẤU HÌNH CƠ BẢN
    col1, col2, col3, col4 = st.columns(4)
    with col1: mon_hoc = st.selectbox("Môn", ["Ngữ văn", "Toán", "Ngoại ngữ", "Giáo dục công dân", "Lịch sử và Địa lý", "Khoa học tự nhiên", "Vật Lý", "Hóa Học", "Sinh Học", "Công nghệ", "Tin học", "GDĐP", "HĐTN-HN"], index=1)
    with col2: lop = st.selectbox("Lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], index=2)
    with col3: hinh_thuc = st.selectbox("Hình thức", ["Trắc nghiệm & Tự luận", "Trắc nghiệm", "Tự Luận"])
    with col4: thoi_gian = st.selectbox("Thời gian", ["90 phút", "120 phút", "60 phút", "45 phút"])

    col_ten, col_file1, col_file2 = st.columns([2, 1, 1])
    with col_ten: ten_bai = st.text_input("Tên bài kiểm tra / Đề số", placeholder="Ví dụ: Kiểm tra giữa kì I")
    with col_file1: de_cuong_file = st.file_uploader("Đề Cương", type=['docx', 'pdf'])
    with col_file2: ma_tran_file = st.file_uploader("Ma trận", type=['docx', 'pdf'])
    
    bam_sat = st.checkbox("Bám sát nội dung đề cương/ma trận tải lên", value=True)
    yeu_cau_khac = st.text_area("Yêu cầu chi tiết", placeholder="Thầy/cô thêm yêu cầu. Ví dụ: Phân bố điểm câu tự luận theo mức độ nhận thức có phân hóa HS...", height=70)

    # 2. KHU VỰC CẤU HÌNH MA TRẬN (ĐÃ KHÔI PHỤC)
    with st.expander("⚙️ Tỷ lệ nhận thức & Số lượng câu", expanded=True):
        st.markdown("**1. Tỷ lệ nhận thức (%)**")
        c1, c2, c3, c4 = st.columns(4)
        nb = c1.number_input("Mức độ Nhận biết", value=40)
        th = c2.number_input("Mức độ Thông hiểu", value=30)
        vd = c3.number_input("Mức độ Vận dụng", value=20)
        vdc = c4.number_input("Mức độ Vận dụng cao", value=10)
        
        st.markdown("**2. Thông số Trắc nghiệm**")
        ct1, ct2, ct3, ct4 = st.columns(4)
        sl1 = ct1.number_input("Số câu nhiều lựa chọn", value=12)
        d1 = ct2.number_input("Điểm/Câu nhiều lựa chọn", value=0.25, step=0.05)
        sl2 = ct3.number_input("Số câu Đúng/Sai", value=4)
        d2 = ct4.number_input("Điểm/Điểm câu Đúng/Sai", value=0.25, step=0.05)
        
        ct5, ct6, ct7, ct8 = st.columns(4)
        sl3 = ct5.number_input("Số câu Điền khuyết", value=4)
        d3 = ct6.number_input("Điểm câu Điền khuyết", value=0.25, step=0.05)
        sl4 = ct7.number_input("Số câu trả lời ngắn", value=2)
        d4 = ct8.number_input("Điểm câu trả lời ngắn", value=0.5, step=0.05)

        st.markdown("**3. Thông số Tự luận**")
        ctl1, ctl2 = st.columns(2)
        so_tl = ctl1.number_input("Tổng số câu Tự luận", value=4)
        diem_tl = ctl2.number_input("Tổng điểm Tự luận", value=4.0, step=0.25)

    # 3. KHỞI TẠO AI
    if st.button("🚀 TỰ ĐỘNG KHỞI TẠO MA TRẬN VÀ ĐỀ THI", type="primary", use_container_width=True):
        if not ten_bai.strip(): st.warning("Vui lòng nhập tên bài!"); st.stop()
        
        # Đọc nội dung file
        file_context = ""
        if de_cuong_file:
            try:
                if de_cuong_file.name.endswith('.pdf'):
                    reader = PdfReader(de_cuong_file)
                    file_context = "\n".join([p.extract_text() for p in reader.pages[:10]])
                elif de_cuong_file.name.endswith('.docx'):
                    doc = docx.Document(de_cuong_file)
                    file_context = "\n".join([p.text for p in doc.paragraphs])
            except Exception as e: st.error(f"Lỗi đọc file: {e}")

        final_key = api_key if api_key else get_api_key()
        # Đóng gói thông số vào prompt
        prompt = f"Soạn đề {mon_hoc} {lop}. Chủ đề: {ten_bai}. Cấu trúc: {yeu_cau_khac}. Tỷ lệ: NB {nb}%, TH {th}%, VD {vd}%, VDC {vdc}%. TN: {sl1} MCQ ({d1}đ), {sl2} Đ/S ({d2}đ), {sl3} ĐK ({d3}đ), {sl4} Ngắn ({d4}đ). TL: {so_tl} câu ({diem_tl}đ). Bám sát tài liệu: {file_context[:3000]}"
        
        with st.spinner("AI đang soạn đề..."):
            result = run_ai_with_fallback(prompt=prompt, api_key=final_key, model_mode="flash")
            if result.get("success"):
                st.session_state['current_exam_data'] = {"title": ten_bai, "content": result.get("text")}
                st.rerun()
            else: st.error("AI không phản hồi.")

    # 4. KẾT QUẢ
    if 'current_exam_data' in st.session_state:
        st.markdown("---")
        with st.expander("Xem & Xuất đề", expanded=True):
            st.markdown(st.session_state['current_exam_data']['content'])
            WordEngine = get_word_engine()
            if WordEngine:
                if st.button("Tải file Đề thi (Word)"):
                    try:
                        word_file = WordEngine.export_to_word(st.session_state['current_exam_data'])
                        st.download_button("Tải về máy", data=word_file, file_name="De_Thi.docx", use_container_width=True)
                    except Exception as e: st.error(f"Lỗi: {e}")

# Helper để lấy WordEngine (giữ nguyên logic cũ của thầy)
def get_word_engine():
    try:
        from export.export_word import WordExportEngine
        return WordExportEngine
    except: return None
