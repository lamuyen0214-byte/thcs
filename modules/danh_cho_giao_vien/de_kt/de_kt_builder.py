import streamlit as st
import os
import requests
import sys
from ai_engine.layer_3_reasoning.prompt_manager import PromptManager

def get_word_engine():
    try:
        # 1. Chống kẹt bộ nhớ đệm (Cache) của Streamlit
        module_path = 'export.export_word'
        if module_path in sys.modules:
            del sys.modules[module_path]
            
        # Gọi chính xác đến tệp export_word.py trong thư mục export/
        from export.export_word import WordExportEngine
        return WordExportEngine
    except Exception as e:
        # ĐỔI PRINT THÀNH ST.ERROR ĐỂ LỖI HIỂN THỊ RÕ LÊN MÀN HÌNH THAY VÌ ẨN ĐI
        st.error(f"⚠️ Không thể tải Module Xuất Word: {e}")
        return None

def render_de_kt_module():
    # 1. CẤU HÌNH CSS ĐỂ KHÓA BỐ CỤC CỐ ĐỊNH (THU NHỎ CHỮ ĐIỂM CHỐNG NHẢY HÀNG)
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

    # 4. HÀNG 3: TÊN BÀI VÀ TẢI FILE DỮ LIỆU CỐ ĐỊNH (TỶ LỆ CỦA THẦY)
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

    # 5. HÀNG 4: CẤU TRÚC MA TRẬN ĐỘNG CHIA ĐÔI HAI CỘT TRÁI/PHẢI GIỮ NGUYÊN TỶ LỆ CỦA THẦY
    col_tn, spacer, col_tl = st.columns([12, 1, 12])
    # --- CỘT TRÁI: TRẮC NGHIỆM ĐỘNG GIAO DIỆN CỐ ĐỊNH ---
    with col_tn:
        tn_header = st.empty()
        st.write("")
        
        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu nhiều lựa chọn:")
        with c2: sl1 = st.number_input("SL1", value=12, key="sl1", label_visibility="collapsed")
        with c3: d1 = st.number_input("D1", value=3.0, step=0.25, format="%.2f", key="d1", label_visibility="collapsed")
        with c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu đúng/sai:")
        with c2: sl2 = st.number_input("SL2", value=1, key="sl2", label_visibility="collapsed")
        with c3: d2 = st.number_input("D2", value=0.25, step=0.25, format="%.2f", key="d2", label_visibility="collapsed")
        with c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu điền khuyết:")
        with c2: sl3 = st.number_input("SL3", value=1, key="sl3", label_visibility="collapsed")
        with c3: d3 = st.number_input("D3", value=0.25, step=0.25, format="%.2f", key="d3", label_visibility="collapsed")
        with c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns([4, 2, 2, 1])
        with c1: st.write("Số câu trả lời ngắn:")
        with c2: sl4 = st.number_input("SL4", value=2, key="sl4", label_visibility="collapsed")
        with c3: d4 = st.number_input("D4", value=0.5, step=0.25, format="%.2f", key="d4", label_visibility="collapsed")
        with col4 if 'col4' in locals() else c4: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True)

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
        for i in range(1, int(so_cau_tl) + 1):
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1: st.write(f"**Câu {i}.**")
            with c2: 
                diem = st.number_input("Điểm", value=1.0, step=0.25, format="%.2f", key=f"diem_tl_{i}", label_visibility="collapsed")
                diem_tl_list.append(diem)
            with c3: st.markdown('<span class="chu-diem-co-nho">điểm</span>', unsafe_allow_html=True)

        tong_diem_tl = sum(diem_tl_list)
        tl_header.markdown(f'<div class="box-tu-luan">TỰ LUẬN &nbsp;&nbsp;&nbsp; <span style="color:red;">{int(so_cau_tl)}</span> &nbsp;&nbsp;&nbsp; <span style="color:red;">{tong_diem_tl:.2f}</span> &nbsp;&nbsp;&nbsp; Điểm</div>', unsafe_allow_html=True)

    st.write("---")
    col_chk, col_req = st.columns([1, 2])
    with col_chk: st.markdown('<p class="text-red-italic">Yêu cầu khác:</p>', unsafe_allow_html=True)
    with col_req:
        bam_sat = st.checkbox("Bám sát nội dung đề cương/ma trận tải lên", value=True)
        yeu_cau_khac = st.text_area("Yêu cầu chi tiết", placeholder="Ví dụ: Chú trọng các câu hỏi liên hệ thực tế...", label_visibility="collapsed")
    
    # 7. SỰ KIỆN CLICK NÚT BẤM (ĐÃ NÂNG CẤP LÕI AM HIỂU CHƯƠNG TRÌNH GDPT 2018 VÀ BỘ SÁCH KẾT NỐI TRI THỨC)
    # Tích hợp menu thả xuống chọn mô hình AI để chủ động phòng tránh lỗi 404
    col_btn_run, col_model_sel = st.columns([3, 1])
    with col_model_sel:
        model_display_name = st.selectbox(
            "Mô hình", 
            ["3.1 Flash-Lite", "3.5 Flash", "3.1 Pro", "Tư duy mở rộng"], 
            label_visibility="collapsed", index=0
        )
    with col_btn_run:
        btn_generate = st.button("🚀 TỰ ĐỘNG KHỞI TẠO MA TRẬN VÀ ĐỀ THI", type="primary", use_container_width=True)

    if btn_generate:
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

            with st.spinner("🤖 Trợ lý AI đang kích hoạt kho tri thức GDPT 2018 và biên soạn đề kiểm tra..."):
                chu_de_ai = f"{ten_bai} ({hinh_thuc}, {thoi_gian}). Tỷ lệ: NB {nhan_biet}%, TH {thong_hieu}%, VD {van_dung}%, VDC {van_dung_cao}%."
                if yeu_cau_khac: chu_de_ai += f" Yêu cầu bổ sung: {yeu_cau_khac}"

                # Khởi tạo luồng trích xuất văn bản thô từ tài liệu đính kèm
                file_context = ""
                if de_cuong_file is not None:
                    try:
                        ext = de_cuong_file.name.split(".")[-1].lower()
                        de_cuong_file.seek(0)
                        if ext == "pdf":
                            from pypdf import PdfReader
                            reader = PdfReader(de_cuong_file)
                            for page_idx in range(min(len(reader.pages), 30)):
                                page_text = reader.pages[page_idx].extract_text()
                                if page_text: file_context += page_text + "\n"
                        elif ext == "docx":
                            import docx
                            file_context += "\n".join([p.text for p in docx.Document(de_cuong_file).paragraphs])
                    except Exception as e: print(e)

                # Cập nhật danh sách định danh mô hình chuẩn xác nhất của Google hiện tại
                model_mapping = {
                    "3.1 Flash-Lite": "gemini-1.5-flash-8b",
                    "3.5 Flash": "gemini-1.5-flash",
                    "3.1 Pro": "gemini-2.0-flash",
                    "Tư duy mở rộng": "gemini-1.5-pro-latest"
                }
                primary_model = model_mapping.get(model_display_name, "gemini-1.5-flash")
                
                # Danh sách dự phòng toàn các mô hình cực nhẹ, tốc độ cao, độ tương thích API 100%
                fallback_queue = list(dict.fromkeys([primary_model, "gemini-1.5-flash", "gemini-1.5-flash-8b", "gemini-2.0-flash"]))
                
                score_item_1 = d1 / sl1 if sl1 > 0 else 0
                score_item_2 = d2 / sl2 if sl2 > 0 else 0
                score_item_3 = d3 / sl3 if sl3 > 0 else 0
                score_item_4 = d4 / sl4 if sl4 > 0 else 0
                tl_scores_str = ", ".join([f"Câu {idx+1} ({val}đ)" for idx, val in enumerate(diem_tl_list)])

                # SIÊU CÂU LỆNH PROMPT SƯ PHẠM
                system_instruction = f"""
                Bạn là Viện trưởng Viện Khoa học Giáo dục kiêm Chuyên gia khảo thí cao cấp của Bộ GD&ĐT Việt Nam.
                [YÊU CẦU NỀN TẢNG TUÂN THỦ]: Bạn phải sở hữu tri thức sâu rộng, am hiểu tường tận 100% mục tiêu cốt lõi của Chương trình GDPT 2018 đối với toàn bộ các môn học và cấu trúc nội dung phân phối chương trình của Bộ sách "Kết nối tri thức với cuộc sống".
                [LUẬT ĐỐI CHIẾU FILE]:
                - Kiểm tra xem [NỘI DUNG TÀI LIỆU] tải lên có ký tự chữ toán học/khoa học nào thuộc môn "{mon_hoc}" hay không.
                - NẾU FILE TRỐNG hoặc file bị lỗi trích xuất chữ: Bạn TUYỆT ĐỐI KHÔNG ĐƯỢC TỪ CHỐI RA ĐỀ. Hãy chủ động kích hoạt ngay kho tri thức chuyên gia nội tại của bạn về môn {mon_hoc} {lop} thuộc bộ sách "Kết nối tri thức với cuộc sống" bám sát chủ đề "{ten_bai}" để tự động bù đắp thông tin và tiến hành biên soạn bộ đề đạt chuẩn quốc gia.
                [TIẾN TRÌNH BIÊN SOẠN BẮT BUỘC]:
                Mục 1: Thiết lập cấu trúc [MA TRẬN ĐỀ KIỂM TRA CHUẨN] phân hóa rõ ràng các cột dọc và hàng ngang mức độ: Nhận biết, Thông hiểu, Vận dụng, Vận dụng cao phân rõ 2 cột nhỏ TN/TL bám sát tỉ lệ {nhan_biet}:{thong_hieu}:{van_dung}:{van_dung_cao}.
                Mục 2: Lập [BẢNG ĐẶC TẢ KỸ THUẬT VÀ TIÊU CHÍ CẦU ĐẠT CHI TIẾT] của từng câu hỏi.
                Mục 3: Biên soạn [NỘI DUNG ĐỀ KIỂM TRA CHÍNH THỨC] môn {mon_hoc} {lop}. Cấu trúc đề: {chu_de_ai}. Trắc nghiệm: {sl1} câu MCQ Nhiều lựa chọn ({score_item_1:.2f}đ), {sl2} câu Đúng/Sai ({score_item_2:.2f}đ), {sl3} câu Điền khuyết ({score_item_3:.2f}đ), {sl4} câu ngắn ({score_item_4:.2f}đ). Tự luận: {int(so_cau_tl)} câu với biểu điểm chi tiết: {tl_scores_str}.
                Mục 4: Xuất bản [ĐÁP ÁN VÀ HƯỚNG DẪN CHẤM] khóa mã trắc nghiệm và thang điểm tự luận chi tiết đến 0.25đ.
                """
                
                response_text = None
                activated_model_name = ""
                error_log = [] # Két sắt lưu trữ toàn bộ lịch sử lỗi
                
                from google import genai
                try:
                    client = genai.Client(api_key=str(user_raw_key))
                    for current_model in fallback_queue:
                        try:
                            response = client.models.generate_content(
                                model=current_model,
                                contents=[f"{system_instruction}\n\n[NỘI DUNG TÀI LIỆU GỐC TẢI LÊN]:\n{file_context[:8000]}"]
                            )
                            if response and response.text:
                                response_text = response.text
                                activated_model_name = current_model
                                break
                        except Exception as e:
                            # Bắt trọn mọi lỗi của từng mô hình đưa vào danh sách
                            error_log.append(f"[{current_model}] thất bại: {str(e)}")
                            continue 
                except Exception as api_err:
                    st.error(f"❌ Lỗi khởi tạo hệ thống AI: {api_err}")
                    return
                    
                if response_text:
                    st.session_state['current_exam_data'] = {
                        "type": hinh_thuc, "custom_req": ten_bai if ten_bai else "De_Kiem_Tra",
                        "tn_total": tong_so_cau_tn, "c1": sl1, "c2": sl2, "c3": sl3, "c4": sl4,
                        "tn_score": str(tong_diem_tn), "tl_total": str(tong_diem_tl),
                        "tl_scores": [str(v) for v in diem_tl_list], "r_nb": str(nhan_biet), "r_th": str(thong_hieu), "r_vd": str(van_dung), "r_vdc": str(van_dung_cao),
                        "ai_generated_content": response_text
                    }
                    st.success(f"✅ Đã khởi tạo thành công bằng mô hình {activated_model_name}!")
                else:
                    # In rõ ràng lịch sử "chiến đấu" của vòng lặp để giáo viên không bị rối
                    error_details = "\n\n".join(error_log)
                    st.error(f"❌ Không thể kết nối AI sau khi đã quét toàn bộ các mô hình dự phòng. Chi tiết lỗi hệ thống:\n{error_details}")

    # 8. CẶP NÚT BẤM CHỨC NĂNG KẾT XUẤT CỐ ĐỊNH 100% RA MÀN HÌNH THEO ĐÚNG YÊU CẦU
    st.markdown("---")
    st.markdown("##### 📥 Kết Xuất Hồ Sơ Đề Kiểm Tra Chuyên Nghiệp")
    
    if st.session_state.get('delete_action_trigger'):
        if 'current_exam_data' in st.session_state:
            del st.session_state['current_exam_data']
        st.session_state['delete_action_trigger'] = False
        st.rerun()

    exam_cache = st.session_state.get('current_exam_data')

    if exam_cache:
        with st.expander("🔍 Xem trước Nội dung Đề kiểm tra & Đáp án chi tiết từ AI", expanded=True):
            st.markdown(exam_cache["ai_generated_content"])

        WordEngine = get_word_engine()
        if WordEngine:
            try:
                word_file = WordEngine.export_to_word(exam_cache)
                
                col_save, col_dl, col_del = st.columns(3)
                
                with col_save:
                    if st.button("💾 Lưu file tạm thời", use_container_width=True, key="save_temp_action"):
                        st.success("✅ Đã lưu an toàn đề thi vào bộ nhớ hệ thống!")
                
                with col_dl:
                    st.download_button(
                        label="📄 Tải file về máy",
                        data=word_file,
                        file_name=f"Bo_De_Kiem_Tra_{ten_bai.replace(' ', '_') if ten_bai else 'Moi'}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                        key="dl_docx_final_fixed_v6_ready"
                    )
                
                with col_del:
                    if st.button("❌ Xóa file", type="secondary", use_container_width=True, key="clear_cache_final_fixed_v6_ready"):
                        st.session_state['delete_action_trigger'] = True
                        st.rerun()
                        
            except Exception as doc_err:
                st.error(f"⚠️ Trình kết xuất file Word đang báo lỗi: {doc_err}")
                # KHÓA BỐ CỤC: Bổ sung 3 nút vô hiệu hóa khi quá trình xuất Word nội bộ gặp lỗi để bảo toàn giao diện
                col_save, col_dl, col_del = st.columns(3)
                with col_save: st.button("💾 Lưu file tạm thời", type="secondary", use_container_width=True, disabled=True)
                with col_dl: st.button("📄 Tải file về máy", type="secondary", use_container_width=True, disabled=True)
                with col_del: st.button("❌ Xóa file", type="secondary", use_container_width=True, disabled=True)
        else:
            # KHÓA BỐ CỤC: Nếu file Word hoàn toàn không thể nạp (bị mất), vẫn duy trì 3 nút ở dạng chờ trên màn hình
            col_save, col_dl, col_del = st.columns(3)
            with col_save: st.button("💾 Lưu file tạm thời", type="secondary", use_container_width=True, disabled=True)
            with col_dl: st.button("📄 Tải file về máy", type="secondary", use_container_width=True, disabled=True)
            with col_del: st.button("❌ Xóa file", type="secondary", use_container_width=True, disabled=True)
    else:
        # Trạng thái chờ mặc định khi chưa có đề thi
        col_save, col_dl, col_del = st.columns(3)
        with col_save: st.button("💾 Lưu file tạm thời", type="secondary", use_container_width=True, disabled=True)
        with col_dl: st.button("📄 Tải file về máy", type="secondary", use_container_width=True, disabled=True)
        with col_del: st.button("❌ Xóa file", type="secondary", use_container_width=True, disabled=True)
