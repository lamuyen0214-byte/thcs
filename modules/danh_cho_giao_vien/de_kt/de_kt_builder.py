import streamlit as st
import os
import sys

# =====================================================================
# 1. ĐỊNH VỊ ĐƯỜNG DẪN GỐC TỰ ĐỘNG TÌM AI_ENGINE (ƯU TIÊN TUYỆT ĐỐI)
# =====================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = current_dir
# Quét ngược lên các thư mục cha cho đến khi thấy lõi 'ai_engine'
while not os.path.exists(os.path.join(root_dir, 'ai_engine')) and root_dir != os.path.dirname(root_dir):
    root_dir = os.path.dirname(root_dir)

if root_dir not in sys.path:
    sys.path.insert(0, root_dir) # Dùng insert(0) thay vì append

# Giữ nguyên khai báo đường dẫn cũ của thầy cho thư mục export
export_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
if export_path not in sys.path:
    sys.path.append(export_path)

# =====================================================================
# 2. NẠP ĐỘNG CƠ TỪ KIẾN TRÚC MỚI
# =====================================================================
from ai_engine.ai_config import get_api_key
from ai_engine.ai_runner import run_ai_with_fallback

def get_word_engine():
    try:
        from export.export_word import WordExportEngine
        return WordExportEngine
    except Exception as e:
        print(f"Lỗi nạp module Word: {e}")
        return None

def render_de_kt_module(api_key=""): # Bổ sung tham số api_key
    # 1. CẤU HÌNH CSS ĐỂ KHÓA BỐ CỤC CỐ ĐỊNH CHỐNG NHẢY DÒNG CHỮ
    st.markdown("""
        <style>
        /* Ép toàn bộ khối container chính của Streamlit bung rộng kịch trần lề trái và lề phải */
        div[data-testid="stAppViewBlockContainer"], 
        .main .block-container, 
        .stAppViewBlockContainer {
            max-width: 98% !important;
            width: 98% !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }
        .header-blue {color: #0000FF; font-weight: bold; font-size: 16px; text-align: center;}
        .text-red-italic {color: #FF0000; font-style: italic; font-weight: bold; font-size: 14px;}
        .box-trac-nghiem {background-color: #FFF2CC; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .box-tu-luan {background-color: #D5E8D4; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .header-red-title {color: #FF0000; font-weight: bold; font-size: 16px; margin-bottom: 5px;}
        
        /* Thu nhỏ chữ điểm bám sát ô số, ép không cho phép xuống hàng */
        .chu-diem-co-nho {
            font-size: 12px !important;
            font-style: italic;
            white-space: nowrap !important;
            display: inline-block;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. HÀNG 1: MENU ĐIỀU HƯỚNG CỐ ĐỊNH 4 CỘT
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

    # 3. HÀNG 2: TỶ LỆ MỨC ĐỘ NHẬN THỨC CỐ ĐỊNH CỦA THẦY
    st.markdown('<p class="header-red-title">Tỷ lệ mức độ nhận thức (%):</p>', unsafe_allow_html=True)
    col_tl1, col_tl2, col_tl3, col_tl4 = st.columns(4)
    with col_tl1: nhan_biet = st.number_input("**Nhận biết:**", value=40, step=5, format="%d", key="num_nb_de_kt")
    with col_tl2: thong_hieu = st.number_input("**Thông hiểu:**", value=30, step=5, format="%d", key="num_th_de_kt")
    with col_tl3: van_dung = st.number_input("**Vận dụng:**", value=20, step=5, format="%d", key="num_vd_de_kt")
    with col_tl4: van_dung_cao = st.number_input("**Vận dụng cao:**", value=10, step=5, format="%d", key="num_vdc_de_kt")

    if (nhan_biet + thong_hieu + van_dung + van_dung_cao) != 100:
        st.error("⚠️ Tổng tỷ lệ phần trăm mức độ nhận thức phải bằng 100%!")

    # 4. HÀNG 3: KHU VỰC TẢI FILE TÀI LIỆU VÀ GẮN KEY TĨNH CHO Ô NHẬP LIỆU CHỮ
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
    # Chia đôi không gian màn hình thênh thang wide cho Trắc nghiệm và Tự luận
    col_tn, spacer, col_tl = st.columns([12, 1, 12])

    # --- CỘT TRÁI: THÔNG SỐ BIỂU ĐIỂM TRẮC NGHIỆM ĐỘNG ---
    with col_tn:
        tn_header = st.empty()
        st.write("")
        
        # SỬA DỨT ĐIỂM: Ép mảng tỷ lệ [5, 2, 2, 1] để cột 1 thênh thang, chữ tiêu đề phẳng lỳ không nhảy dòng
        c1, c2, c3, c4 = st.columns([5, 2, 2, 1])
        with c1: st.write("Số câu nhiều lựa chọn:")
        with c2: sl1 = st.number_input("SL1", value=12, key="sl1_de_kt_k", label_visibility="collapsed")
        with c3: d1 = st.number_input("D1", value=3.0, step=0.25, format="%.2f", key="d1_de_kt_k", label_visibility="collapsed")
        with c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns([5, 2, 2, 1])
        with c1: st.write("Số câu đúng/sai:")
        with c2: sl2 = st.number_input("SL2", value=1, key="sl2_de_kt_k", label_visibility="collapsed")
        with c3: d2 = st.number_input("D2", value=0.25, step=0.25, format="%.2f", key="d2_de_kt_k", label_visibility="collapsed")
        with c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns([5, 2, 2, 1])
        with c1: st.write("Số câu điền khuyết:")
        with c2: sl3 = st.number_input("SL3", value=1, key="sl3_de_kt_k", label_visibility="collapsed")
        with c3: d3 = st.number_input("D3", value=0.25, step=0.25, format="%.2f", key="d3_de_kt_k", label_visibility="collapsed")
        with c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns([5, 2, 2, 1])
        with c1: st.write("Số câu trả lời ngắn:")
        with c2: sl4 = st.number_input("SL4", value=2, key="sl4_de_kt_k", label_visibility="collapsed")
        with c3: d4 = st.number_input("D4", value=0.5, step=0.25, format="%.2f", key="d4_de_kt_k", label_visibility="collapsed")
        with c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True)

        tong_diem_tn = d1 + d2 + d3 + d4
        tong_so_cau_tn = sl1 + sl2 + sl3 + sl4
        tn_header.markdown(f'<div class="box-trac-nghiem">TRẮC NGHIỆM &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {tong_diem_tn:.2f} &nbsp;&nbsp;&nbsp; Điểm</div>', unsafe_allow_html=True)

    # --- CỘT PHẢI: VÒNG LẶP SỐ CÂU TỰ LUẬN ĐỘNG ---
    with col_tl:
        c_tl1, c_tl2 = st.columns([7, 3])
        with c_tl1: st.write("**Nhập số lượng câu Tự luận:**")
        with c_tl2: so_cau_tl = st.number_input("Số câu TL", min_value=1, max_value=10, value=4, key="so_cau_tl_de_kt_k", label_visibility="collapsed")
        tl_header = st.empty()
        st.write("")
        
        diem_tl_list = []
        for i in range(1, int(so_cau_tl) + 1):
            # Ép mảng tỷ lệ [3, 4, 3] cho phần cột tự luận để thẳng hàng đẹp mắt
            c1, c2, c3 = st.columns([3, 4, 3])
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

    col_btn_run, col_model_sel = st.columns(2)
    with col_model_sel:
        model_display_name = st.selectbox("Mô hình", ["3.1 Flash-Lite", "3.5 Flash", "3.1 Pro", "Tư duy mở rộng"], label_visibility="collapsed", index=0, key="sb_model_ai_de_kt_run")
    with col_btn_run:
        activated = st.button("🚀 TỰ ĐỘNG KHỞI TẠO MA TRẬN VÀ ĐỀ THI", type="primary", use_container_width=True, key="btn_submit_run_de_kt")

    if activated:
        if not ten_bai.strip():
            st.warning("⚠️ Vui lòng nhập 'Tên bài kiểm tra / Đề số' trước khi khởi tạo.")
        else:
            # -------------------------------------------------------------
            # BỘ ĐIỀU KHIỂN TRUNG TÂM MỚI (AI ENGINE)
            # -------------------------------------------------------------
            if not api_key: # Kiểm tra api_key được truyền vào
                st.error("⚠️ Lỗi hệ thống: Chưa nhận diện được API Key cá nhân hợp lệ tại Sidebar.")
                st.stop() # Chặn ngay luồng thực thi nếu không có key

            with st.spinner("AI đang soạn đề thi bám sát chương trình sách Kết nối tri thức..."):
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
                
                # Hệ thống prompt tinh gọn và sắc bén
                system_instruction = f"Bạn là Chuyên gia khảo thí cao cấp Bộ GD&ĐT Việt Nam. Bộ sách độc tôn áp dụng từ năm 2026: 'Kết nối tri thức với cuộc sống'. Soạn đề thi môn {mon_hoc} {lop}. Tỷ lệ nhận thức: NB {nhan_biet}%, TH {thong_hieu}%, VD {van_dung}%, VDC {van_dung_cao}%. Trắc nghiệm: {sl1} câu MCQ Nhiều lựa chọn ({d1/sl1 if sl1>0 else 0:.2f}đ), {sl2} câu Đúng/Sai, {sl3} câu Điền khuyết, {sl4} câu ngắn. Phần Tự luận: {int(so_cau_tl)} câu. Cấu trúc bài kiểm tra bám sát chủ đề: {ten_bai}. {yeu_cau_khac}"
                prompt_de_kt = f"{system_instruction}\n\n[TÀI LIỆU GỐC ĐỂ BÁM SÁT]:\n{file_context[:6000]}"
                
                # Xác định mô hình tự động qua tên Selectbox
                mode = "pro" if "Pro" in model_display_name or "mở rộng" in model_display_name.lower() else "flash"
                
                # GỌI ENGINE CỐT LÕI MÀ KHÔNG CẦN VIẾT LẠI LOGIC XỬ LÝ LỖI
                result = run_ai_with_fallback(
                    prompt=prompt_de_kt, 
                    api_key=api_key, 
                    model_mode=mode
                )

                if result.get("success"):
                    st.session_state['current_exam_data'] = {
                        "type": hinh_thuc, "custom_req": ten_bai if ten_bai else "De_Kiem_Tra", "ten_bai_save": str(ten_bai),
                        "tn_total": tong_so_cau_tn, "c1": sl1, "c2": sl2, "c3": sl3, "c4": sl4,
                        "tn_score": str(tong_diem_tn), "tl_total": str(tong_diem_tl),
                        "tl_scores": [str(v) for v in diem_tl_list], "r_nb": str(nhan_biet), "r_th": str(thong_hieu), "r_vd": str(van_dung), "r_vdc": str(van_dung_cao),
                        "ai_generated_content": result.get("text")
                    }
                    st.success(f"✅ Hệ thống bóc tách ma trận và soạn đề thi hoàn tất trong {result.get('time'):.2f} giây! (Model: {result.get('model')})")
                    st.rerun()
                else:
                    st.error("❌ QUÁ TRÌNH KHỞI TẠO BỊ CHẶN: Máy chủ Google AI Studio từ chối phản hồi.")
                    with st.expander("🔍 Chi tiết lỗi kỹ thuật ngầm từ hệ thống", expanded=True):
                        st.code(result.get("error"))

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
            except Exception as e: st.error(f"💡 Trình kết xuất file Word đang đồng bộ: {e}")

    # ÉP CỨNG BỘ 3 NÚT BẰNG BIẾN ĐỘC LẬP - HIỂN THỊ NGANG NHAU TĂM TẮP THEO HÌNH 3 CỦA THẦY
    col_save, col_download, col_delete = st.columns(3)
    with col_save:
        if st.button("💾 Lưu file tạm thời", use_container_width=True, disabled=(exam_cache is None), key="btn_save_de_kt_final_k"):
            st.sidebar.success("💾 Đã lưu cấu hình hồ sơ đề thi vào RAM phiên làm việc an toàn!")
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
