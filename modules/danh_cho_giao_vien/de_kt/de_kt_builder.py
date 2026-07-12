import streamlit as st
import os
import requests

def get_word_engine():
    try:
        from export.word_export import WordExportEngine
        return WordExportEngine
    except Exception:
        return None

def render_de_kt_module():
    # 1. CẤU HÌNH CSS ĐỂ KHÓA BỐ CỤC CỐ ĐỊNH (THU NHỎ CHỮ ĐIỂM CHỐNG NHẢY DÒNG)
    st.markdown("""
        <style>
        .header-blue {color: #0000FF; font-weight: bold; font-size: 16px; text-align: center;}
        .text-red-italic {color: #FF0000; font-style: italic; font-weight: bold; font-size: 14px;}
        .box-trac-nghiem {background-color: #FFF2CC; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .box-tu-luan {background-color: #D5E8D4; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .header-red-title {color: #FF0000; font-weight: bold; font-size: 16px; margin-bottom: 5px;}
        
        /* Thu nhỏ chữ điểm bám sát ô số, ép không cho phép xuống hàng */
        .chu-diem-co-nho {
            font-size: 11px !important;
            font-style: italic;
            white-space: nowrap !important;
            display: inline-block;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. HÀNG 1: MENU ĐIỀU HƯỚNG CƠ BẢN CỐ ĐỊNH THEO TÊN NHÃN MỚI
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<p class="header-blue">Chọn môn học</p>', unsafe_allow_html=True)
        mon_hoc = st.selectbox(
            "Môn", 
            ["Ngữ văn", "Toán", "Ngoại ngữ", "Giáo dục công dân", "Lịch sử và Địa lý", "Khoa học tự nhiên", "Vật Lý", "Hóa Học", "Sinh Học", "Công nghệ", "Tin học", "GDĐP", "HĐTN-HN"], 
            label_visibility="collapsed", index=5
        )
    with col2:
        st.markdown('<p class="header-blue">Chọn lớp</p>', unsafe_allow_html=True)
        lop = st.selectbox(
            "Lớp", 
            ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], 
            label_visibility="collapsed", index=1
        )
    with col3:
        st.markdown('<p class="header-blue">Hình thức kiểm tra</p>', unsafe_allow_html=True)
        hinh_thuc = st.selectbox(
            "Hình thức", 
            ["Trắc nghiệm & Tự luận", "Trắc nghiệm", "Tự Luận"], 
            label_visibility="collapsed"
        )
    with col4:
        st.markdown('<p class="header-blue">Thời lượng kiểm tra</p>', unsafe_allow_html=True)
        thoi_gian = st.selectbox(
            "Thời gian", 
            ["45 phút", "60 phút", "90 phút", "120 phút"], 
            label_visibility="collapsed", index=1
        )

    st.write("")
    # 3. HÀNG 2: TỶ LỆ MỨC ĐỘ NHẬN THỨC CỐ ĐỊNH CỦA THẦY
    st.markdown('<p class="header-red-title">Tỷ lệ mức độ nhận thức (%):</p>', unsafe_allow_html=True)
    col_tl1, col_tl2, col_tl3, col_tl4 = st.columns(4)
    with col_tl1: nhan_biet = st.number_input("**Nhận biết:**", value=40, step=5, format="%d")
    with col_tl2: thong_hieu = st.number_input("**Thông hiểu:**", value=30, step=5, format="%d")
    with col_tl3: van_dung = st.number_input("**Vận dụng:**", value=20, step=5, format="%d")
    with col_tl4: van_dung_cao = st.number_input("**Vận dụng cao:**", value=10, step=5, format="%d")

    st.write("")

    if (nhan_biet + thong_hieu + van_dung + van_dung_cao) != 100:
        st.error("⚠️ Tổng tỷ lệ phần trăm mức độ nhận thức phải bằng 100%!")

    # 4. HÀNG 3: TÊN BÀI VÀ TẢI FILE DỮ LIỆU CỐ ĐỊNH
    col_ten, col_file1, col_file2 = st.columns([2, 1, 1])
    with col_ten:
        st.markdown('<p class="header-red-title">Tên bài kiểm tra / Đề số:</p>', unsafe_allow_html=True)
        ten_bai = st.text_input("Tên bài", placeholder="Ví dụ: Kiểm tra đánh giá giữa kì I", label_visibility="collapsed")
    with col_file1:
        st.markdown('<p class="text-red-italic">Tải Đề Cương (.docx, .pdf):</p>', unsafe_allow_html=True)
        de_cuong_file = st.file_uploader("Đề cương", type=['docx', 'pdf'], label_visibility="collapsed")
    with col_file2:
        st.markdown('<p class="text-red-italic">Tải Đề mẫu ma trận (.docx, .pdf):</p>', unsafe_allow_html=True)
        ma_tran_file = st.file_uploader("Ma trận", type=['docx', 'pdf'], label_visibility="collapsed")

    st.write("")
    # 5. HÀNG 4: CẤU TRÚC MA TRẬN ĐỘNG CHIA ĐÔI HAI CỘT TRÁI/PHẢI GIỮ NGUYÊN TỶ LỆ COLUMNS GỐC
    col_tn, spacer, col_tl = st.columns([12, 1, 12])
    
    with col_tn:
        tn_header = st.empty()
        st.write("")
        
        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu nhiều lựa chọn:")
        with c2: sl1 = st.number_input("SL1", value=12, key="sl1", label_visibility="collapsed")
        with c3: d1 = st.number_input("D1", value=3.0, step=0.25, format="%.2f", key="d1", label_visibility="collapsed")
        with c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True) # ĐÃ SỬA CỠ CHỮ

        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu đúng/sai:")
        with c2: sl2 = st.number_input("SL2", value=1, key="sl2", label_visibility="collapsed")
        with c3: d2 = st.number_input("D2", value=0.25, step=0.25, format="%.2f", key="d2", label_visibility="collapsed")
        with c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True) # ĐÃ SỬA CỠ CHỮ

        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu điền khuyết:")
        with c2: sl3 = st.number_input("SL3", value=1, key="sl3", label_visibility="collapsed")
        with c3: d3 = st.number_input("D3", value=0.25, step=0.25, format="%.2f", key="d3", label_visibility="collapsed")
        with c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True) # ĐÃ SỬA CỠ CHỮ

        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu trả lời ngắn:")
        with c2: sl4 = st.number_input("SL4", value=2, key="sl4", label_visibility="collapsed")
        with c3: d4 = st.number_input("D4", value=0.5, step=0.25, format="%.2f", key="d4", label_visibility="collapsed")
        with c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True) # ĐÃ SỬA CỠ CHỮ

        tong_diem_tn = d1 + d2 + d3 + d4
        tong_so_cau_tn = sl1 + sl2 + sl3 + sl4
        tn_header.markdown(f'<div class="box-trac-nghiem">TRẮC NGHIỆM &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {tong_diem_tn:.2f} &nbsp;&nbsp;&nbsp; Điểm</div>', unsafe_allow_html=True)
    with col_tl:
        c_tl1, c_tl2 = st.columns([2, 1])
        with c_tl1: st.write("**Nhập số lượng câu Tự luận:**")
        with c_tl2: so_cau_tl = st.number_input("Số câu TL", min_value=1, max_value=10, value=4, key="so_cau_tl", label_visibility="collapsed")
        
        tl_header = st.empty()
        st.write("")
        
        diem_tl_list = []
        for i in range(1, int(so_cau_tl) + 1):
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1: st.write(f"**Câu {i}.**")
            with c2: 
                diem = st.number_input("Điểm", value=1.0, step=0.25, format="%.2f", key=f"diem_tl_{i}", label_visibility="collapsed")
                diem_tl_list.append(diem)
            with c3: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True) # ĐÃ SỬA CỠ CHỮ

        tong_diem_tl = sum(diem_tl_list)
        tl_header.markdown(f'<div class="box-tu-luan">TỰ LUẬN &nbsp;&nbsp;&nbsp; <span style="color:red;">{int(so_cau_tl)}</span> &nbsp;&nbsp;&nbsp; <span style="color:red;">{tong_diem_tl:.2f}</span> &nbsp;&nbsp;&nbsp; Điểm</div>', unsafe_allow_html=True)

    # 6. HÀNG 6: Ô NHẬP LIỆU YÊU CẦU BỔ SUNG KHÁC GIỮ NGUYÊN CẤU TRÚC GỐC CỦA THẦY
    st.write("---")
    col_chk, col_req = st.columns([1, 2])
    with col_chk:
        st.markdown('<p class="text-red-italic">Yêu cầu khác:</p>', unsafe_allow_html=True)
    with col_req:
        bam_sat = st.checkbox("Bám sát nội dung đề cương/ma trận tải lên", value=True)
        yeu_cau_khac = st.text_area("Yêu cầu chi tiết", placeholder="Ví dụ: Chú trọng các câu hỏi liên hệ thực tế...", label_visibility="collapsed")
    
    st.write("")
    # 7. SỰ KIỆN CLICK NÚT BẤM (ĐÃ SỬA: VÁ TRIỆT ĐỂ LUỒNG ĐỌC STREAMLIT FILE ĐÍNH KÈM VÀ PHÂN PHỐI ĐIỂM)
    if st.button("🚀 Khởi tạo Đề Kiểm Tra", type="primary", use_container_width=True):
        if not ten_bai.strip():
            st.warning("⚠️ Vui lòng nhập 'Tên bài kiểm tra / Đề số' trước khi khởi tạo.")
        else:
            user_raw_key = st.session_state.get("user_gemini_key", "").strip()
            if not user_raw_key:
                if "GEMINI_API_KEY" in st.secrets: user_raw_key = st.secrets["GEMINI_API_KEY"].strip()
                elif "GOOGLE_API_KEY" in st.secrets: user_raw_key = st.secrets["GOOGLE_API_KEY"].strip()

            if not user_raw_key:
                st.error("⚠️ Lỗi cấu hình: Vui lòng nhập Gemini API Key ở thanh bên (Sidebar) trước!")
                return

            with st.spinner("AI đang phân tích tài liệu đề cương và tiến hành soạn câu hỏi..."):
                chu_de_ai = f"{ten_bai} ({hinh_thuc}, {thoi_gian}). Tỷ lệ: NB {nhan_biet}%, TH {thong_hieu}%, VD {van_dung}%, VDC {van_dung_cao}%."
                if yeu_cau_khac: chu_de_ai += f" Yêu cầu bổ sung: {yeu_cau_khac}"

                # SỬA LỖI CHÍ MẠNG: Khởi tạo luồng đọc an toàn cưỡng ép con trỏ tệp tin quay về vị trí số 0
                file_context = ""
                if de_cuong_file is not None:
                    try:
                        ext = de_cuong_file.name.split(".")[-1].lower()
                        # Đưa con trỏ file stream về đầu để tránh việc đọc chuỗi rỗng sau khi rerun
                        de_cuong_file.seek(0)
                        
                        if ext == "pdf":
                            from pypdf import PdfReader
                            reader = PdfReader(de_cuong_file)
                            # Đọc tăng dung lượng lấy nhiều trang kiến thức hơn
                            for page_idx in range(min(len(reader.pages), 30)):
                                page_text = reader.pages[page_idx].extract_text()
                                if page_text: file_context += page_text + "\n"
                        elif ext == "docx":
                            import docx
                            doc = docx.Document(de_cuong_file)
                            file_context += "\n".join([p.text for p in doc.paragraphs])
                    except Exception as e: 
                        st.error(f"Trục trặc trích xuất văn bản tệp tin: {e}")

                # Nếu thầy không tải file đề cương, hệ thống dùng chủ đề gõ ở ô text_input làm ngữ cảnh
                if not file_context.strip():
                    file_context = f"Chủ đề trọng tâm cần ra đề: {ten_bai}. Phạm vi kiến thức môn {mon_hoc} {lop}."

                try:
                    from google import genai
                    client = genai.Client(api_key=str(user_raw_key))
                    
                    score_item_1 = d1 / sl1 if sl1 > 0 else 0
                    score_item_2 = d2 / sl2 if sl2 > 0 else 0
                    score_item_3 = d3 / sl3 if sl3 > 0 else 0
                    score_item_4 = d4 / sl4 if sl4 > 0 else 0
                    tl_scores_str = ", ".join([f"Câu {idx+1} ({val}đ)" for idx, val in enumerate(diem_tl_list)])

                    # Khóa cấu hình prompt bộc lộ mệnh lệnh tối cao bắt buộc đọc khối văn bản
                    system_instruction = f"""
                    Bạn là chuyên gia kiểm định khảo thí THCS Bộ GD&ĐT Việt Nam.
                    [NHIỆM VỤ 1 - KIỂM TRA MÂU THUẪN]: Hãy đối chiếu môn học được chọn trên giao diện là "{mon_hoc}" với nội dung thực tế trong đoạn văn bản [NỘI DUNG ĐỀ CƯƠNG TẢI LÊN] ở dưới. Nếu văn bản tải lên thuộc môn học khác (Ví dụ: chọn môn Khoa học tự nhiên nhưng đề cương lại là bài tập Toán, Văn...), bạn BẮT BUỘC phải dừng lại ngay và xuất duy nhất dòng cảnh báo: "⚠️ CẢNH BÁO: PHÁT HIỆN MÂU THUẪN KIẾN THỨC. FILE TẢI LÊN KHÔNG PHẢI MÔN KHỞI TẠO." và tuyệt đối không soạn câu hỏi.
                    [NHIỆM VỤ 2 - BIÊN SOẠN BÁM SÁT]: Nếu môn học trùng khớp, hãy soạn đề thi môn {mon_hoc} {lop} bám sát hoàn toàn vào phạm vi kiến thức cốt lõi phân bố trong [NỘI DUNG ĐỀ CƯƠNG TẢI LÊN], không lấy kiến thức ngoài tệp.
                    Cấu trúc đề: {chu_de_ai}. Trắc nghiệm: {sl1} câu MCQ ({score_item_1:.2f}đ), {sl2} câu Đúng/Sai ({score_item_2:.2f}đ), {sl3} câu Điền khuyết ({score_item_3:.2f}đ), {sl4} câu ngắn ({score_item_4:.2f}đ). Tự luận: {int(so_cau_tl)} câu với biểu điểm: {tl_scores_str}.
                    Yêu cầu chia rõ ràng thành PHẦN 1: ĐỀ KIỂM TRA MINH HỌA và PHẦN 2: ĐÁP ÁN VÀ HƯỚNG DẪN CHẤM CHI TIẾT.
                    """
                    
                    # Nới rộng dung lượng đọc file lên 8000 ký tự để bao quát toàn bộ nội dung SGK Toán
                    response = client.models.generate_content(
                        model="models/gemini-2.5-flash",
                        contents=[f"{system_instruction}\n\n[NỘI DUNG ĐỀ CƯƠNG TẢI LÊN]:\n{file_context[:8000]}"]
                    )
                    
                    ai_result = response.text
                    if ai_result:
                        st.session_state['current_exam_data'] = {
                            "type": hinh_thuc, "custom_req": ten_bai if ten_bai else "De_Kiem_Tra",
                            "tn_total": tong_so_cau_tn, "c1": sl1, "c2": sl2, "c3": sl3, "c4": sl4,
                            "tn_score": str(tong_diem_tn), "tl_total": str(tong_diem_tl),
                            "tl_scores": [str(v) for v in diem_tl_list], "r_nb": str(nhan_biet), "r_th": str(thong_hieu), "r_vd": str(van_dung), "r_vdc": str(van_dung_cao),
                            "ai_generated_content": ai_result
                        }
                        st.success("✅ Đã tạo đề thi và ma trận thành công!")
                        st.rerun()
                except Exception as api_err:
                    st.error(f"❌ Trục trặc kết nối mô hình AI: {api_err}")

    # 8. KHU VỰC KẾT XUẤT HỒ SƠ - KHÓA HIỂN THỊ CỐ ĐỊNH CẶP NÚT BẤM VÀ XỬ LÝ LỆNH XÓA SẠCH BỘ NHỚ
    st.markdown("---")
    st.markdown("##### 📥 Kết Xuất Hồ Sơ Đề Kiểm Tra Chuyên Nghiệp")
    
    if st.session_state.get('delete_action_trigger'):
        if 'current_exam_data' in st.session_state:
            del st.session_state['current_exam_data']
        st.session_state['delete_action_trigger'] = False
        st.rerun()

    exam_cache = st.session_state.get('current_exam_data')

    if exam_cache:
        # Khi đã tạo đề thành công -> Mở khóa cặp nút hoạt động (màu xanh lá)
        with st.expander("🔍 Xem trước Nội dung Đề kiểm tra & Đáp án chi tiết từ AI", expanded=True):
            st.markdown(exam_cache["ai_generated_content"])

        WordEngine = get_word_engine()
        if WordEngine:
            try:
                word_file = WordEngine.export_to_word(exam_cache)
                col_dl, col_del = st.columns(2)
                with col_dl:
                    st.download_button(
                        label="📄 Tải xuống file Word (.docx) chứa Ma trận & Đề thi hoàn chỉnh",
                        data=word_file,
                        file_name=f"Bo_De_Kiem_Tra_{ten_bai.replace(' ', '_') if ten_bai else 'Moi'}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                        key="download_docx_key_fixed_v3"
                    )
                with col_del:
                    if st.button("❌ Xóa đề thi hiện tại khỏi bộ đệm", type="secondary", use_container_width=True, key="clear_cache_key_fixed_v3"):
                        st.session_state['delete_action_trigger'] = True
                        st.rerun()
            except Exception as doc_err:
                st.error(f"⚠️ Trình kết xuất file Word đang đồng bộ: {doc_err}")
    else:
        # Ở trạng thái chờ -> Hiển thị cặp nút màu xám cố định để giao diện không bị trống trải
        col_dl, col_del = st.columns(2)
        with col_dl:
            st.button("📄 Tải xuống file Word (.docx) chứa Ma trận & Đề thi hoàn chỉnh", type="secondary", use_container_width=True, disabled=True, help="Nút bấm sẽ kích hoạt sau khi AI khởi tạo đề thành công.")
        with col_del:
            st.button("❌ Xóa đề thi hiện tại khỏi bộ đệm", type="secondary", use_container_width=True, disabled=True)

