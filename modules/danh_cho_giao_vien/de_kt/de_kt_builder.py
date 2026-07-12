# =====================================================================
# FILE: modules/danh_cho_giao_vien/de_kt/de_kt_builder.py - PHẦN 1
# =====================================================================
import streamlit as st
import os
import requests

def get_word_engine():
    try:
        from export.export_word import WordExportEngine
        return WordExportEngine
    except Exception as e:
        print(f"Lỗi nạp module Word: {e}")
        return None

def render_de_kt_module():
    # 1. CẤU HÌNH CSS ĐỂ KHÓA BỐ CỤC CỐ ĐỊNH CHỐNG NHẢY DÒNG CHỮ
    st.markdown("""
        <style>
        .header-blue {color: #0000FF; font-weight: bold; font-size: 16px; text-align: center;}
        .text-red-italic {color: #FF0000; font-style: italic; font-weight: bold; font-size: 14px;}
        .box-trac-nghiem {background-color: #FFF2CC; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .box-tu-luan {background-color: #D5E8D4; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .header-red-title {color: #FF0000; font-weight: bold; font-size: 16px; margin-bottom: 5px;}
        .chu-diem-co-nho {font-size: 11px !important; font-style: italic; white-space: nowrap !important; display: inline-block; margin-top: 10px;}
        </style>
    """, unsafe_allow_html=True)

    # 2. HÀNG 1: MENU ĐIỀU HƯỚNG CỐ ĐỊNH ĐÃ KHỬ TRÙNG LẶP ID WIDGET BẰNG KEY TĨNH
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<p class="header-blue">Chọn môn học</p>', unsafe_allow_html=True)
        mon_hoc = st.selectbox("Môn", ["Ngữ văn", "Toán", "Ngoại ngữ", "Giáo dục công dân", "Lịch sử và Địa lý", "Khoa học tự nhiên", "Vật Lý", "Hóa Học", "Sinh Học", "Công nghệ", "Tin học", "GDĐP", "HĐTN-HN"], label_visibility="collapsed", index=1, key="sb_mon_hoc_de_kt_unique")
    with col2:
        st.markdown('<p class="header-blue">Chọn lớp</p>', unsafe_allow_html=True)
        lop = st.selectbox("Lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], label_visibility="collapsed", index=2, key="sb_lop_de_kt_unique")
    with col3:
        st.markdown('<p class="header-blue">Hình thức kiểm tra</p>', unsafe_allow_html=True)
        hinh_thuc = st.selectbox("Hình thức", ["Trắc nghiệm & Tự luận", "Trắc nghiệm", "Tự Luận"], label_visibility="collapsed", key="sb_hinh_thuc_de_kt_unique")
    with col4:
        st.markdown('<p class="header-blue">Thời lượng kiểm tra</p>', unsafe_allow_html=True)
        thoi_gian = st.selectbox("Thời gian", ["45 phút", "60 phút", "90 phút", "120 phút"], label_visibility="collapsed", index=0, key="sb_thoi_gian_de_kt_unique")

    st.write("")
    st.markdown('<p class="header-red-title">Tỷ lệ mức độ nhận thức (%):</p>', unsafe_allow_html=True)
    col_tl1, col_tl2, col_tl3, col_tl4 = st.columns(4)
    with col_tl1: nhan_biet = st.number_input("**Nhận biết:**", value=40, step=5, format="%d", key="num_nb_de_kt")
    with col_tl2: thong_hieu = st.number_input("**Thông hiểu:**", value=30, step=5, format="%d", key="num_th_de_kt")
    with col_tl3: van_dung = st.number_input("**Vận dụng:**", value=20, step=5, format="%d", key="num_vd_de_kt")
    with col_tl4: van_dung_cao = st.number_input("**Vận dụng cao:**", value=10, step=5, format="%d", key="num_vdc_de_kt")

    if (nhan_biet + thong_hieu + van_dung + van_dung_cao) != 100:
        st.error("⚠️ Tổng tỷ lệ phần trăm mức độ nhận thức phải bằng 100%!")
# =====================================================================
# FILE: modules/danh_cho_giao_vien/de_kt/de_kt_builder.py - PHẦN 2
# =====================================================================
    col_ten, col_file1, col_file2 = st.columns(3)
    with col_ten:
        st.markdown('<p class="header-red-title">Tên bài kiểm tra / Đề số:</p>', unsafe_allow_html=True)
        ten_bai = st.text_input("Tên bài", placeholder="Ví dụ: Kiểm tra đánh giá giữa kì I", label_visibility="collapsed", key="txt_ten_bai_de_kt")
    with col_file1:
        st.markdown('<p class="text-red-italic">Tải Đề Cương (.docx, .pdf):</p>', unsafe_allow_html=True)
        de_cuong_file = st.file_uploader("Đề cương", type=['docx', 'pdf'], label_visibility="collapsed", key="file_de_cuong_de_kt")
    with col_file2:
        st.markdown('<p class="text-red-italic">Tải Đề mẫu ma trận (.docx, .pdf):</p>', unsafe_allow_html=True)
        ma_tran_file = st.file_uploader("Ma trận", type=['docx', 'pdf'], label_visibility="collapsed", key="file_ma_tran_de_kt")

    st.write("")
    col_tn, spacer, col_tl = st.columns(3)
    
    with col_tn:
        tn_header = st.empty()
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.write("Số câu nhiều lựa chọn:")
        with c2: sl1 = st.number_input("SL1", value=12, key="sl1_de_kt_k", label_visibility="collapsed")
        with c3: d1 = st.number_input("D1", value=3.0, step=0.25, format="%.2f", key="d1_de_kt_k", label_visibility="collapsed")
        with c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.write("Số câu đúng/sai:")
        with c2: sl2 = st.number_input("SL2", value=1, key="sl2_de_kt_k", label_visibility="collapsed")
        with c3: d2 = st.number_input("D2", value=0.25, step=0.25, format="%.2f", key="d2_de_kt_k", label_visibility="collapsed")
        with c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.write("Số câu điền khuyết:")
        with c2: sl3 = st.number_input("SL3", value=1, key="sl3_de_kt_k", label_visibility="collapsed")
        with c3: d3 = st.number_input("D3", value=0.25, step=0.25, format="%.2f", key="d3_de_kt_k", label_visibility="collapsed")
        with c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.write("Số câu trả lời ngắn:")
        with c2: sl4 = st.number_input("SL4", value=2, key="sl4_de_kt_k", label_visibility="collapsed")
        with c3: d4 = st.number_input("D4", value=0.5, step=0.25, format="%.2f", key="d4_de_kt_k", label_visibility="collapsed")
        with c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True)

        tong_diem_tn = d1 + d2 + d3 + d4
        tong_so_cau_tn = sl1 + sl2 + sl3 + sl4
        tn_header.markdown(f'<div class="box-trac-nghiem">TRẮC NGHIỆM &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {tong_diem_tn:.2f} &nbsp;&nbsp;&nbsp; Điểm</div>', unsafe_allow_html=True)

    with col_tl:
        c_tl1, c_tl2 = st.columns(2)
        with c_tl1: st.write("**Nhập số lượng câu Tự luận:**")
        with c_tl2: so_cau_tl = st.number_input("Số câu TL", min_value=1, max_value=10, value=4, key="so_cau_tl_de_kt_k", label_visibility="collapsed")
        tl_header = st.empty()
        
        diem_tl_list = []
        for i in range(1, int(so_cau_tl) + 1):
            c1, c2, c3 = st.columns(3)
            with c1: st.write(f"**Câu {i}.**")
            with c2: 
                diem = st.number_input("Điểm", value=1.0, step=0.25, format="%.2f", key=f"diem_tl_{i}_de_kt_k", label_visibility="collapsed")
                diem_tl_list.append(diem)
            with c3: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True)

        tong_diem_tl = sum(diem_tl_list)
        tl_header.markdown(f'<div class="box-tu-luan">TỰ LUẬN &nbsp;&nbsp;&nbsp; <span style="color:red;">{int(so_cau_tl)}</span> &nbsp;&nbsp;&nbsp; <span style="color:red;">{tong_diem_tl:.2f}</span> &nbsp;&nbsp;&nbsp; Điểm</div>', unsafe_allow_html=True)

    st.write("---")
    col_chk, col_req = st.columns(2)
    with col_chk: st.markdown('<p class="text-red-italic">Yêu cầu khác:</p>', unsafe_allow_html=True)
    with col_req:
        bam_sat = st.checkbox("Bám sát nội dung đề cương/ma trận tải lên", value=True, key="chk_bam_sat_de_kt")
        yeu_cau_khac = st.text_area("Yêu cầu chi tiết", placeholder="Ví dụ: Chú trọng các câu hỏi liên hệ thực tế...", label_visibility="collapsed", key="ta_req_de_kt")
# =====================================================================
# FILE: modules/danh_cho_giao_vien/de_kt/de_kt_builder.py - PHẦN 3
# =====================================================================
    col_btn_run, col_model_sel = st.columns(2)
    with col_model_sel:
        model_display_name = st.selectbox("Mô hình", ["3.1 Flash-Lite", "3.5 Flash", "3.1 Pro", "Tư duy mở rộng"], label_visibility="collapsed", index=0, key="sb_model_ai_de_kt_run")
    with col_btn_run:
        activated = st.button("🚀 TỰ ĐỘNG KHỞI TẠO MA TRẬN VÀ ĐỀ THI", type="primary", use_container_width=True, key="btn_submit_run_de_kt")

    if activated:
        if not ten_bai.strip():
            st.warning("⚠️ Vui lòng nhập 'Tên bài kiểm tra / Đề số' trước khi khởi tạo.")
        else:
            # ĐÃ ĐỒNG BỘ CHÍ MẠNG: Triệt tiêu lệnh genai.Client cũ, bốc đúng Client tập trung từ file app.py cha
            client = st.session_state.get("gemini_client")
            if not client:
                st.error("⚠️ Lỗi hệ thống: Chưa tìm thấy API Key hợp lệ tại Sidebar. Vui lòng kiểm tra lại!")
                return

            with st.spinner("AI đang kết nối Client cha và tiến hành soạn câu hỏi cùng ma trận..."):
                file_context = ""
                if de_cuong_file is not None:
                    try:
                        ext = de_cuong_file.name.split(".")[-1].lower()
                        de_cuong_file.seek(0)
                        if ext == "pdf":
                            from pypdf import PdfReader
                            reader = PdfReader(de_cuong_file)
                            for page_idx in range(min(len(reader.pages), 20)):
                                p_text = reader.pages[page_idx].extract_text()
                                if p_text: file_context += p_text + "\n"
                        elif ext == "docx":
                            import docx
                            file_context += "\n".join([p.text for p in docx.Document(de_cuong_file).paragraphs])
                    except Exception: pass

                if not file_context.strip(): file_context = f"Phạm vi chủ đề bài kiểm tra: {ten_bai}."

                try:
                    from config.models import get_fallback_queue
                    fallback_models = get_fallback_queue(model_display_name)
                except Exception:
                    from main.config.models import get_fallback_queue
                    fallback_models = get_fallback_queue(model_display_name)

                response_text = None
                system_instruction = f"Bạn là Chuyên gia khảo thí của Bộ GD&ĐT Việt Nam. Bộ sách độc tôn năm 2026: 'Kết nối tri thức với cuộc sống'. Hãy soạn ma trận dạng bảng, đặc tả và đề thi môn {mon_hoc} {lop} bám sát chủ đề: {ten_bai}. Tỷ lệ nhận thức: Nhận biết {nhan_biet}%, Thông hiểu {thong_hieu}%, Vận dụng {van_dung}%, Vận dụng cao {van_dung_cao}%."
                
                # Quét thông suốt chuỗi dự phòng thông minh bằng luồng Client cha tĩnh
                for current_model in fallback_models:
                    try:
                        response = client.models.generate_content(model=current_model, contents=[f"{system_instruction}\n\n[DỮ LIỆU TÀI LIỆU]:\n{file_context[:8000]}"])
                        if response and response.text:
                            response_text = response.text
                            break
                        except Exception: continue

                if response_text:
                    st.session_state['current_exam_data'] = {
                        "type": hinh_thuc, "custom_req": ten_bai if ten_bai else "De_Kiem_Tra", "ten_bai_save": str(ten_bai),
                        "tn_total": tong_so_cau_tn, "c1": sl1, "c2": sl2, "c3": sl3, "c4": sl4,
                        "tn_score": str(tong_diem_tn), "tl_total": str(tong_diem_tl),
                        "tl_scores": [str(v) for v in diem_tl_list], "r_nb": str(nhan_biet), "r_th": str(thong_hieu), "r_vd": str(van_dung), "r_vdc": str(van_dung_cao),
                        "ai_generated_content": response_text
                    }
                    st.success("✅ Đã tạo hồ sơ đề kiểm tra thành công!")
                    st.rerun()

    st.markdown("---")
    st.markdown("##### 📥 Kết Xuất Hồ Sơ Đề Kiểm Tra Chuyên Nghiệp")
    if st.session_state.get('delete_action_trigger'):
        if 'current_exam_data' in st.session_state: del st.session_state['current_exam_data']
        st.session_state['delete_action_trigger'] = False
        st.rerun()

    exam_cache = st.session_state.get('current_exam_data')
    word_file = None

    if exam_cache:
        with st.expander("🔍 Xem trước Nội dung Đề kiểm tra & Đáp án chi tiết từ AI", expanded=True):
            st.markdown(exam_cache["ai_generated_content"])
        WordEngine = get_word_engine()
        if WordEngine:
            try: word_file = WordEngine.export_to_word(exam_cache)
            except Exception as e: st.error(f"💡 Trình dịch Word đang đồng bộ: {e}")

    col_save, col_download, col_delete = st.columns(3)
    with col_save:
        if st.button("💾 Lưu file tạm thời", use_container_width=True, disabled=(exam_cache is None), key="btn_save_de_kt_final_k"):
            st.sidebar.success("💾 Đã lưu cấu hình đề thi vào RAM phiên an toàn!")
    with col_download:
        if word_file is not None and exam_cache is not None:
            saved_title = exam_cache.get("ten_bai_save", "Moi").replace(" ", "_")
            st.download_button(label="📄 Tải file về máy", data=word_file, file_name=f"Bo_De_Kiem_Tra_{saved_title}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True, key="btn_dl_word_de_kt_final_k")
        else:
            st.button("📄 Tải file về máy", disabled=True, use_container_width=True, key="btn_dl_word_de_kt_dis_final_k")
    with col_delete:
        if st.button("❌ Xóa file", use_container_width=True, disabled=(exam_cache is None), key="btn_del_de_kt_final_k"):
            st.session_state['delete_action_trigger'] = True
            st.rerun()
