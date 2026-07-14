import streamlit as st
import os
import docx
from pypdf import PdfReader
from export.export_word import WordExportEngine
from ai_engine.ai_config import get_api_key
from ai_engine.ai_runner import run_ai_with_fallback

def render_quizizz_module(api_key=""):
    # Tinh chỉnh CSS Giao diện: Kế thừa 100% chuẩn hệ thống (Xanh/Đỏ/Khoảng cách)
    st.markdown("""
    <style>
    div[data-testid="stAppViewBlockContainer"], .main .block-container {
        padding-top: 3.5rem !important;
        padding-bottom: 3rem !important;
    }
    .stSelectbox label p, .stTextInput label p, .stNumberInput label p, .stFileUploader label p, .stTextArea label p {
        color: #0000FF !important; 
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    .stMarkdown p strong {
        color: #FF0000 !important; 
        font-size: 15px !important;
    }
    .stButton>button { 
        font-weight: bold; 
        border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 1. CẤU HÌNH CƠ BẢN
    col1, col2, col3 = st.columns(3)
    with col1: mon_hoc = st.selectbox("Chọn Môn", ["Ngữ văn", "Toán", "Ngoại ngữ", "Giáo dục công dân", "Lịch sử và Địa lý", "Khoa học tự nhiên", "Vật Lý", "Hóa Học", "Sinh Học", "Công nghệ", "Tin học", "GDĐP", "HĐTN-HN"], index=5, key="qz_mon")
    with col2: lop = st.selectbox("Chọn Lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], index=2, key="qz_lop")
    with col3: thoi_gian_cau = st.selectbox("Thời lượng / Câu (Quizizz)", ["30 giây", "45 giây", "60 giây", "2 phút", "3 phút"], index=1, key="qz_tg")

    col_ten, col_file = st.columns([2, 1])
    with col_ten: ten_bai = st.text_input("Chủ đề Quizizz / Tên bài học", placeholder="Ví dụ: Bài 4: Tốc độ chuyển động")
    with col_file: tai_lieu_file = st.file_uploader("Tải tài liệu tham chiếu (PDF/Docx)", type=['docx', 'pdf'])
    
    yeu_cau_khac = st.text_area("Yêu cầu chi tiết", placeholder="Thầy cô yêu cầu thêm. Ví dụ: Các câu hỏi điền khuyết phải gắn với công thức, câu ghép đôi gắn với hiện tượng thực tế...", height=70)

    # 2. KHU VỰC CẤU HÌNH CÂU HỎI & ĐỘ KHÓ
    with st.expander("Cấu hình Tỷ lệ nhận thức & Cơ cấu Dạng câu hỏi", expanded=True):
        st.markdown("**1. Tỷ lệ nhận thức (%)**")
        c1, c2, c3, c4 = st.columns(4)
        nb = c1.number_input("Mức độ Nhận biết (%)", value=40, key="qz_nb")
        th = c2.number_input("Mức độ Thông hiểu (%)", value=30, key="qz_th")
        vd = c3.number_input("Mức độ Vận dụng (%)", value=20, key="qz_vd")
        vdc = c4.number_input("Vận dụng cao (%)", value=10, key="qz_vdc")

        st.markdown("**2. Cơ cấu Dạng câu hỏi Quizizz**")
        ct1, ct2, ct3, ct4 = st.columns(4)
        sl_mcq = ct1.number_input("1 Đáp án đúng (MCQ)", value=10, min_value=0, key="qz_mcq")
        sl_multi = ct2.number_input("Nhiều đáp án (Checkbox)", value=2, min_value=0, key="qz_multi")
        sl_dien = ct3.number_input("Điền khuyết (Fill-in)", value=2, min_value=0, key="qz_dien")
        sl_ghep = ct4.number_input("Ghép đôi (Matching)", value=2, min_value=0, key="qz_ghep")

    # 3. KHỞI TẠO AI
    if st.button("TỰ ĐỘNG SINH NGÂN HÀNG QUIZIZZ", type="primary", use_container_width=True):
        if not ten_bai.strip(): 
            st.warning("Vui lòng nhập Chủ đề / Tên bài học!")
            st.stop()
        
        file_context = ""
        if tai_lieu_file:
            try:
                if tai_lieu_file.name.endswith('.pdf'):
                    reader = PdfReader(tai_lieu_file)
                    file_context = "\n".join([p.extract_text() for p in reader.pages[:10]])
                elif tai_lieu_file.name.endswith('.docx'):
                    doc = docx.Document(tai_lieu_file)
                    file_context = "\n".join([p.text for p in doc.paragraphs])
            except Exception as e: st.error(f"Lỗi đọc file: {e}")

        final_key = api_key if api_key else get_api_key()
        
        # SIÊU CÂU LỆNH PROMPT CHUYÊN BIỆT CHO QUIZIZZ
        prompt = f"""
Bạn là Chuyên gia thiết kế nội dung Elearning xuất sắc. Hãy soạn một bộ câu hỏi tương tác lên nền tảng Quizizz môn {mon_hoc} {lop}. 
Chủ đề: {ten_bai}.
Yêu cầu phân bổ mức độ: Nhận biết {nb}%, Thông hiểu {th}%, Vận dụng {vd}%, VDC {vdc}%.
Thời gian dự kiến làm mỗi câu: {thoi_gian_cau}.
Dựa sát vào tài liệu sau: {file_context[:3500]}
Yêu cầu chi tiết của giáo viên: {yeu_cau_khac}

BẮT BUỘC tạo chính xác các dạng câu hỏi sau:
1. Dạng 1: {sl_mcq} câu hỏi CHỌN 1 ĐÁP ÁN ĐÚNG. Mỗi câu có 4 phương án (A, B, C, D).
2. Dạng 2: {sl_multi} câu hỏi NHIỀU ĐÁP ÁN ĐÚNG (Checkbox). Mỗi câu 4-5 phương án, liệt kê rõ các đáp án đúng.
3. Dạng 3: {sl_dien} câu hỏi ĐIỀN KHUYẾT. Cung cấp câu trần thuật thiếu từ và CHUỖI TỪ KHOÁ CẦN ĐIỀN CHÍNH XÁC.
4. Dạng 4: {sl_ghep} câu hỏi GHÉP ĐÔI. Cho 2 nhóm dữ liệu (Ví dụ: Nhóm 1 (A,B,C,D) và Nhóm 2 (1,2,3,4)) và đáp án ghép cặp.

Về Định dạng Markdown: 
- Trình bày rõ từng câu hỏi.
- Dưới mỗi câu, BẮT BUỘC phải có "ĐÁP ÁN" và "GIẢI THÍCH NGẮN GỌN" (rất quan trọng để Quizizz hiện phản hồi cho học sinh sau khi chọn).
"""
        with st.spinner("AI đang thiết kế cấu trúc và sinh ngân hàng câu hỏi đa dạng..."):
            result = run_ai_with_fallback(prompt=prompt, api_key=final_key, model_mode="flash")
            if result.get("success"):
                st.session_state['current_quizizz_data'] = {"title": ten_bai, "content": result.get("text")}
                st.rerun()
            else: st.error("AI không phản hồi.")

    # 4. KẾT QUẢ VÀ XUẤT FILE
    if 'current_quizizz_data' in st.session_state:
        st.markdown("---")
        with st.expander("Xem trước & Tải về", expanded=True):
            st.markdown(st.session_state['current_quizizz_data']['content'])
            
            # Kết nối trái tim xuất file
            try:
                if st.button("📥 Tải bản in Đề cương & Đáp án (Word)", use_container_width=True):
                    word_file = WordExportEngine.export_to_word(st.session_state['current_quizizz_data'])
                    st.download_button("Xác nhận Tải về máy", data=word_file, file_name=f"Quizizz_{ten_bai.replace(' ', '_')}.docx", use_container_width=True)
            except Exception as e: 
                st.error(f"Lỗi trình xuất Word: {e}")
