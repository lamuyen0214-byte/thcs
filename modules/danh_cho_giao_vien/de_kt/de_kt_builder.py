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
    # 1. CẤU HÌNH CSS ĐỂ KHÓA BỐ CỤC (GIỮ NGUYÊN 100% GIAO DIỆN CỦA THẦY)
    st.markdown("""
        <style>
        .header-blue {color: #0000FF; font-weight: bold; font-size: 16px; text-align: center;}
        .text-red-italic {color: #FF0000; font-style: italic; font-weight: bold; font-size: 14px;}
        .box-trac-nghiem {background-color: #FFF2CC; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .box-tu-luan {background-color: #D5E8D4; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .header-red-title {color: #FF0000; font-weight: bold; font-size: 16px; margin-bottom: 5px;}
        </style>
    """, unsafe_allow_html=True)

    # 2. HÀNG 1: MENU ĐIỀU HƯỚNG CƠ BẢN CỐ ĐỊNH
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<p class="header-blue">MENU MÔN HỌC</p>', unsafe_allow_html=True)
        mon_hoc = st.selectbox("Môn", ["Khoa học Tự nhiên", "Toán học", "Vật lý", "Hóa học"], label_visibility="collapsed", index=0)
    with col2:
        st.markdown('<p class="header-blue">MENU LỚP</p>', unsafe_allow_html=True)
        lop = st.selectbox("Lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"], label_visibility="collapsed", index=3)
    with col3:
        st.markdown('<p class="header-blue">HÌNH THỨC KT</p>', unsafe_allow_html=True)
        hinh_thuc = st.selectbox("Hình thức", ["Giữa kì", "Cuối kì", "Thường xuyên"], label_visibility="collapsed")
    with col4:
        st.markdown('<p class="header-blue">THỜI GIAN</p>', unsafe_allow_html=True)
        thoi_gian = st.selectbox("Thời gian", ["45 phút", "60 phút", "90 phút", "120 phút"], label_visibility="collapsed", index=1)

    st.write("")
    # 3. HÀNG 2: TỶ LỆ MỨC ĐỘ NHẬN THỨC CỐ ĐỊNH
    st.markdown('<p class="header-red-title">Tỷ lệ mức độ nhận thức (%):</p>', unsafe_allow_html=True)
    col_tl1, col_tl2, col_tl3, col_tl4 = st.columns(4)
    with col_tl1:
        nhan_biet = st.number_input("**Nhận biết:**", value=40, step=5, format="%d")
    with col_tl2:
        thong_hieu = st.number_input("**Thông hiểu:**", value=30, step=5, format="%d")
    with col_tl3:
        van_dung = st.number_input("**Vận dụng:**", value=20, step=5, format="%d")
    with col_tl4:
        van_dung_cao = st.number_input("**Vận dụng cao:**", value=10, step=5, format="%d")

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

    # 5. HÀNG 4: CẤU TRÚC MA TRẬN ĐỘNG CHIA ĐÔI HAI CỘT TRÁI/PHẢI
    col_tn, spacer, col_tl = st.columns([12, 1, 12])
    # --- CỘT TRÁI: TRẮC NGHIỆM ĐỘNG GIAO DIỆN CỐ ĐỊNH ---
    with col_tn:
        tn_header = st.empty()
        st.write("")
        
        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu nhiều lựa chọn:")
        with c2: sl1 = st.number_input("SL1", value=12, key="sl1", label_visibility="collapsed")
        with c3: d1 = st.number_input("D1", value=3.0, step=0.25, format="%.2f", key="d1", label_visibility="collapsed")
        with c4: st.write("*điểm*")

        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu đúng/sai:")
        with c2: sl2 = st.number_input("SL2", value=1, key="sl2", label_visibility="collapsed")
        with c3: d2 = st.number_input("D2", value=0.25, step=0.25, format="%.2f", key="d2", label_visibility="collapsed")
        with c4: st.write("*điểm*")

        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu điền khuyết:")
        with c2: sl3 = st.number_input("SL3", value=1, key="sl3", label_visibility="collapsed")
        with c3: d3 = st.number_input("D3", value=0.25, step=0.25, format="%.2f", key="d3", label_visibility="collapsed")
        with c4: st.write("*điểm*")

        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu trả lời ngắn:")
        with c2: sl4 = st.number_input("SL4", value=2, key="sl4", label_visibility="collapsed")
        with c3: d4 = st.number_input("D4", value=0.5, step=0.25, format="%.2f", key="d4", label_visibility="collapsed")
        with c4: st.write("*điểm*")

        # Tự động tính toán tổng điểm trắc nghiệm nhảy số tức thì
        tong_diem_tn = d1 + d2 + d3 + d4
        tong_so_cau_tn = sl1 + sl2 + sl3 + sl4
        tn_header.markdown(f'<div class="box-trac-nghiem">TRẮC NGHIỆM &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {tong_diem_tn:.2f} &nbsp;&nbsp;&nbsp; Điểm</div>', unsafe_allow_html=True)
    # --- CỘT PHẢI: TỰ LUẬN ĐỘNG GIAO DIỆN CỐ ĐỊNH ---
    with col_tl:
        c_tl1, c_tl2 = st.columns([2, 1])
        with c_tl1: st.write("**Nhập số lượng câu Tự luận:**")
        with c_tl2: so_cau_tl = st.number_input("Số câu TL", min_value=1, max_value=10, value=4, key="so_cau_tl", label_visibility="collapsed")
        
        tl_header = st.empty()
        st.write("")
        
        diem_tl_list = []
        # Tạo lưới hàng dọc tự động nhảy số theo số lượng câu tự luận nhập vào
        for i in range(1, int(so_cau_tl) + 1):
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1: 
                st.write(f"**Câu {i}.**")
            with c2: 
                diem = st.number_input("Điểm", value=1.0, step=0.25, format="%.2f", key=f"diem_tl_{i}", label_visibility="collapsed")
                diem_tl_list.append(diem)
            with c3: 
                st.write("*điểm*")

        # Tự động tính toán tổng điểm tự luận nhảy số thời gian thực
        tong_diem_tl = sum(diem_tl_list)
        tl_header.markdown(f'<div class="box-tu-luan">TỰ LUẬN &nbsp;&nbsp;&nbsp; <span style="color:red;">{int(so_cau_tl)}</span> &nbsp;&nbsp;&nbsp; <span style="color:red;">{tong_diem_tl:.2f}</span> &nbsp;&nbsp;&nbsp; Điểm</div>', unsafe_allow_html=True)

    # 6. HÀNG 6: Ô NHẬP LIỆU YÊU CẦU BỔ SUNG KHÁC
    st.write("---")
    col_chk, col_req = st.columns([1, 2])
    with col_chk:
        st.markdown('<p class="text-red-italic">Yêu cầu khác:</p>', unsafe_allow_html=True)
    with col_req:
        bam_sat = st.checkbox("Bám sát nội dung đề cương/ma trận tải lên", value=True)
        yeu_cau_khac = st.text_area("Yêu cầu chi tiết", placeholder="Ví dụ: Chú trọng các câu hỏi liên hệ thực tế...", label_visibility="collapsed")
    
    st.write("")
        # 7. SỰ KIỆN CLICK NÚT BẤM (CÔ LẬP HOÀN TOÀN CHUỖI MÃ CÁ NHÂN AQ... QUA CỔNG HEADER BẢO MẬT)
    if st.button("🚀 Khởi tạo Đề Kiểm Tra", type="primary", use_container_width=True):
        if not ten_bai.strip():
            st.warning("⚠️ Vui lòng nhập 'Tên bài kiểm tra / Đề số' trước khi khởi tạo.")
        else:
            # Thu thập chuỗi API Key dạng aq.ab8rn... cá nhân từ Sidebar của giáo viên
            user_raw_key = st.session_state.get("user_gemini_key", "").strip()
            if not user_raw_key:
                if "GEMINI_API_KEY" in st.secrets: user_raw_key = st.secrets["GEMINI_API_KEY"].strip()
                elif "GOOGLE_API_KEY" in st.secrets: user_raw_key = st.secrets["GOOGLE_API_KEY"].strip()

            if not user_raw_key:
                st.error("⚠️ Lỗi cấu hình: Vui lòng cấu hình nhập API Key cá nhân ở thanh bên (Sidebar) trước!")
                return

            with st.spinner("AI đang phân tích tài liệu đề cương và tiến hành soạn câu hỏi..."):
                chu_de_ai = f"{ten_bai} ({hinh_thuc}, {thoi_gian}). Tỷ lệ: NB {nhan_biet}%, TH {thong_hieu}%, VD {van_dung}%, VDC {van_dung_cao}%."
                if yeu_cau_khac:
                    chu_de_ai += f" Yêu cầu bổ sung: {yeu_cau_khac}"

                # Trích xuất nội dung file tài liệu đính kèm để nạp ngữ cảnh
                file_context = ""
                if de_cuong_file:
                    try:
                        ext = de_cuong_file.name.split(".")[-1].lower()
                        if ext == "pdf":
                            from pypdf import PdfReader
                            reader = PdfReader(de_cuong_file)
                            file_context += "".join([page.extract_text() or "" for page in reader.pages])
                        elif ext == "docx":
                            import docx
                            doc = docx.Document(de_cuong_file)
                            file_context += "\n".join([p.text for p in doc.paragraphs])
                    except Exception as e:
                        st.error(f"Lỗi nạp tệp đính kèm: {e}")

                # ĐÃ VÁ TRIỆT ĐỂ: Link URL thô cố định 100%, tuyệt đối không cộng chuỗi chứa dấu chấm để tránh dính chữ
                url = "https://googleapis.com"
                
                # ÉP CHUẨN KỸ THUẬT GOOGLE AI STUDIO: Truyền mã khóa qua Header x-goog-api-key độc lập
                headers = {
                    "Content-Type": "application/json",
                    "x-goog-api-key": str(user_raw_key).strip()
                }
                
                # Cấu hình phân bổ biểu điểm chi tiết từng câu hỏi bám sát giao diện của thầy
                score_item_1 = d1 / sl1 if sl1 > 0 else 0
                score_item_2 = d2 / sl2 if sl2 > 0 else 0
                score_item_3 = d3 / sl3 if sl3 > 0 else 0
                score_item_4 = d4 / sl4 if sl4 > 0 else 0
                tl_scores_str = ", ".join([f"Câu {idx+1} ({val}đ)" for idx, val in enumerate(diem_tl_list)])

                system_instruction = f"""
                Bạn là chuyên gia khảo thí THCS Bộ GD&ĐT Việt Nam. Hãy biên soạn đề thi bám sát tài liệu và yêu cầu: "{chu_de_ai}".
                [RÀNG BUỘC PHÂN BỔ MỨC ĐỘ NHẬN THỨC]: Tuân thủ nghiêm ngặt tỷ lệ: Nhận biết {nhan_biet}%, Thông hiểu {thong_hieu}%, Vận dụng {van_dung}%, Vận dụng cao {van_dung_cao}%.
                [CẤU TRÚC ĐỀ BẮT BUỘC]:
                - Phần trắc nghiệm ({tong_diem_tn} điểm): {sl1} câu Nhiều lựa chọn (mỗi câu {score_item_1:.2f}đ), {sl2} câu Đúng/Sai (mỗi câu {score_item_2:.2f}đ), {sl3} câu Điền khuyết (mỗi câu {score_item_3:.2f}đ), {sl4} câu Trả lời ngắn (mỗi câu {score_item_4:.2f}đ).
                - Phần tự luận ({tong_diem_tl} điểm): {int(so_cau_tl)} câu với mức điểm lần lượt: {tl_scores_str}.
                [YÊU CẦU ĐẦU RA]: PHẦN 1: ĐỀ KIỂM TRA MINH HỌA và PHẦN 2: ĐÁP ÁN VÀ HƯỚNG DẪN CHẤM CHI TIẾT.
                """
                
                payload = {"contents": [{"parts": [{"text": f"{system_instruction}\n\n[DỮ LIỆU TÀI LIỆU GỐC]:\n{file_context[:4000]}"}]}]}
                
                try:
                    # Gửi gói tin HTTP POST với timeout bảo vệ luồng chạy
                    response = requests.post(url, headers=headers, json=payload, timeout=120)
                    
                    if response.status_code != 200:
                        st.error(f"❌ Lỗi máy chủ Google (Status {response.status_code}): {response.text}")
                        return
                    
                    response_json = response.json()
                    ai_result = response_json['candidates']['content']['parts']['text']
                    st.success("✅ Đã tạo đề thi và ma trận đặc tả kỹ thuật thành công!")
                    
                    st.session_state['current_exam_data'] = {
                        "type": "Trắc nghiệm kết hợp tự luận", "custom_req": ten_bai,
                        "tn_total": tong_so_cau_tn, "c1": sl1, "c2": sl2, "c3": sl3, "c4": sl4,
                        "tn_score": str(tong_diem_tn), "tl_total": str(tong_diem_tl),
                        "tl_scores": [str(v) for v in diem_tl_list], "r_nb": str(nhan_biet), "r_th": str(thong_hieu), "r_vd": str(van_dung), "r_vdc": str(van_dung_cao),
                        "ai_generated_content": ai_result
                    }
                    st.rerun()
                except Exception as net_err:
                    st.error(f"❌ Trục trặc luồng xử lý hoặc phản hồi JSON không đúng cấu trúc: {net_err}")

    # 8. PHÂN HỆ HIỂN THỊ ĐỀ THI XEM TRƯỚC VÀ NÚT TẢI FILE WORD BẢN IN 3PT
    if 'current_exam_data' in st.session_state:
        exam_cache = st.session_state['current_exam_data']
        st.markdown("---")
        with st.expander("🔍 Xem trước Nội dung Đề kiểm tra & Đáp án chi tiết từ AI", expanded=True):
            st.markdown(exam_cache["ai_generated_content"])
            
        WordEngine = get_word_engine()
        if WordEngine:
            try:
                word_file = WordEngine.export_to_word(exam_cache)
                st.download_button(
                    label="📄 Tải xuống file Word (.docx) chứa Ma trận & Đề thi",
                    data=word_file,
                    file_name=f"Bo_De_Kiem_Tra_{ten_bai.replace(' ', '_')[:25]}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as doc_err:
                st.error(f"⚠️ Trình kết xuất file Word đang được cập nhật cấu trúc bảng biểu: {doc_err}")
