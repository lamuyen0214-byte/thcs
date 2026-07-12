# =====================================================================
# FILE HOÀN CHỈNH: modules/danh_cho_giao_vien/khbd/khbd_builder.py - ĐOẠN 1
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

def render_khbd_module():
    st.markdown("""
        <style>
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
        .header-blue {color: #0000FF; font-weight: bold; font-size: 15px; text-align: left; margin-bottom: 2px;}
        .text-red-italic {color: #FF0000; font-style: italic; font-weight: bold; font-size: 14px;}
        .header-red-title {color: #FF0000; font-weight: bold; font-size: 15px; margin-bottom: 5px;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="header-red-title">Tên bài học / Chủ đề bài dạy:</p>', unsafe_allow_html=True)
    ten_bai = st.text_input("Tên bài", placeholder="Ví dụ: Bài 4: Tốc độ chuyển động", label_visibility="collapsed", key="txt_ten_bai_khbd_5512")

    col_lop, col_mau, col_tiet, col_file = st.columns([1.5, 2, 1.5, 2])
    with col_lop:
        st.markdown('<p class="header-blue">Lớp:</p>', unsafe_allow_html=True)
        lop = st.selectbox("Lớp KHBD", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], label_visibility="collapsed", index=2, key="sb_lop_khbd_unique")
    with col_mau:
        st.markdown('<p class="header-blue">Mẫu thiết kế:</p>', unsafe_allow_html=True)
        mau_thiet_ke = st.selectbox("Mẫu", ["Chuẩn 5512", "Rút gọn", "STEM"], label_visibility="collapsed", index=0, key="sb_mau_khbd_unique")
    with col_tiet:
        st.markdown('<p class="header-blue">Thời lượng (Tiết):</p>', unsafe_allow_html=True)
        thoi_luong = st.number_input("Thời lượng", min_value=1, max_value=10, value=2, label_visibility="collapsed", key="num_tiet_khbd_unique")
    with col_file:
        st.markdown('<p class="header-blue">Tài liệu (docx, pdf, txt):</p>', unsafe_allow_html=True)
        tai_lieu_file = st.file_uploader("Tài liệu đính kèm", type=['docx', 'pdf', 'txt'], label_visibility="collapsed", key="file_tai_lieu_khbd_unique")
# =====================================================================
# FILE HOÀN CHỈNH: modules/danh_cho_giao_vien/khbd/khbd_builder.py - ĐOẠN 2
# =====================================================================
    col_mon, col_model_core = st.columns(2)
    with col_mon:
        st.markdown('<p class="header-blue">Chọn môn học giảng dạy:</p>', unsafe_allow_html=True)
        mon_hoc = st.selectbox("Môn KHBD", ["Toán", "Ngữ văn", "Ngoại ngữ", "Khoa học tự nhiên", "Vật lý", "Hóa học", "Sinh học", "Lịch sử và Địa lý", "Giáo dục công dân", "Tin học", "Công nghệ", "Nghệ thuật", "Giáo dục thể chất", "Hoạt động trải nghiệm, hướng nghiệp", "Giáo dục địa phương"], label_visibility="collapsed", index=0, key="sb_mon_khbd_unique")
    with col_model_core:
        st.markdown('<p class="header-blue">Chọn lõi xử lý Trợ lý AI:</p>', unsafe_allow_html=True)
        model_display_name = st.selectbox("Mô hình KHBD", ["3.1 Flash-Lite", "3.5 Flash", "3.1 Pro", "Tư duy mở rộng"], label_visibility="collapsed", index=0, key="sb_model_khbd_unique")

    st.write("")
    bam_sat = st.checkbox("🚩 Bám sát 100% tài liệu tải lên", value=True, key="chk_bam_sat_khbd_unique")
    st.write("")

    if st.button("🚀 KHỞI TẠO TIẾN TRÌNH KẾ HOẠCH BÀI DẠY", type="primary", use_container_width=True, key="btn_run_khbd_unique"):
        if not ten_bai.strip():
            st.warning("⚠️ Vui lòng điền 'Tên bài học / Chủ đề bài dạy' trước khi kích hoạt.")
        else:
            client = st.session_state.get("gemini_client")
            if not client:
                st.error("⚠️ Lỗi xác thực: Vui lòng kiểm tra hoặc nhập lại API Key ở thanh bên (Sidebar)!")
                return

            if bam_sat and tai_lieu_file is None:
                st.error("❌ LỖI NGHIỆP VỤ: Thầy đã tích chọn 'Bám sát 100% tài liệu tải lên' nhưng chưa nạp file tài liệu hoặc sách giáo khoa. Trợ lý AI đã chặn tiến trình soạn thảo tự do.")
                return

            with st.spinner("🤖 Trợ lý AI đang nghiên cứu tài liệu và thiết lập giáo án 5512..."):
                file_context = ""
                if tai_lieu_file is not None:
                    try:
                        ext = tai_lieu_file.name.split(".")[-1].lower()
                        tai_lieu_file.seek(0)
                        if ext == "pdf":
                            from pypdf import PdfReader
                            reader = PdfReader(tai_lieu_file)
                            for p_idx in range(min(len(reader.pages), 20)):
                                p_text = reader.pages[page_idx].extract_text()
                                if p_text: file_context += p_text + "\n"
                        elif ext == "docx":
                            import docx
                            file_context += "\n".join([p.text for p in docx.Document(tai_lieu_file).paragraphs])
                    except Exception: pass

                if not file_context.strip(): file_context = f"Chủ đề bài học: {ten_bai}."

                prompt_file_content = ""
                prompt_path = "prompts/khbd_prompt.txt"
                if os.path.exists(prompt_path):
                    try:
                        with open(prompt_path, "r", encoding="utf-8") as f: prompt_file_content = f.read()
                    except Exception: pass
                if not prompt_file_content.strip(): prompt_file_content = "Yêu cầu bắt buộc: Tích hợp 'Năng lực số' và ứng dụng 'Trí tuệ nhân tạo (AI)'."

                try:
                    from config.models import get_fallback_queue
                    fallback_queue = get_fallback_queue(model_display_name, phan_he_mode="khbd")
                except Exception:
                    from main.config.models import get_fallback_queue
                    fallback_queue = get_fallback_queue(model_display_name, phan_he_mode="khbd")

                response_text = None
                error_logs = []
                system_instruction = f"Bạn là Chuyên gia của Bộ GD&ĐT Việt Nam. Bộ sách duy nhất năm 2026: 'Kết nối tri thức với cuộc sống'. {prompt_file_content}. Biên soạn KHBD môn {mon_hoc} {lop} mẫu '{mau_thiet_ke}' thời lượng {thoi_luong} tiết bám sát [TÀI LIỆU GỐC]."
                
                for current_model in fallback_queue:
                    try:
                        response = client.models.generate_content(model=current_model, contents=[f"{system_instruction}\n\n[TÀI LIỆU]:\n{file_context[:8000]}"])
                        if response and response.text:
                            response_text = response.text
                            break
                    except Exception as single_err:
                        error_logs.append(f"{current_model}: {str(single_err)}")
                        continue

                if response_text:
                    st.session_state['current_khbd_data'] = {
                        "is_khbd": True, "title": ten_bai, "ten_bai_save": str(ten_bai), "subject": mon_hoc, "grade": lop, "duration": str(thoi_luong), "style": mau_thiet_ke,
                        "ai_generated_content": response_text
                    }
                    st.success("✅ Đã khởi tạo giáo án điện tử thành công!")
                    st.rerun()
                else:
                    st.error("❌ QUÁ TRÌNH KHỞI TẠO BỊ CHẶN: Máy chủ từ chối phản hồi.")
                    with st.expander("🔍 Chi tiết log lỗi kỹ thuật ngầm từ hệ thống Google Server", expanded=True):
                        for log in error_logs: st.code(log)
# =====================================================================
# FILE HOÀN CHỈNH: modules/danh_cho_giao_vien/khbd/khbd_builder.py - ĐOẠN 3
# =====================================================================
    st.markdown("---")
    st.markdown("##### 📥 Kết Xuất Hồ Sơ Giáo Án Sư Phạm Chuyên Nghiệp")
    if st.session_state.get('khbd_delete_trigger'):
        if 'current_khbd_data' in st.session_state: del st.session_state['current_khbd_data']
        st.session_state['khbd_delete_trigger'] = False
        st.rerun()

    khbd_cache = st.session_state.get('current_khbd_data')
    word_file = None

    if khbd_cache:
        with st.expander("🔍 Xem trước Tiến trình Giáo án chi tiết (Chuẩn 5512)", expanded=True):
            st.markdown(khbd_cache["ai_generated_content"])
        WordEngine = get_word_engine()
        if WordEngine:
            try: word_file = WordEngine.export_to_word(khbd_cache)
            except Exception as e: st.error(f"💡 Trình dịch Word đang đồng bộ cấu trúc: {e}")

    # BỘ 3 NÚT CHỨC NĂNG DÀN HÀNG NGANG TĂM TẮP CHUẨN ĐỒ HỌA HÌNH 3
    col_save, col_download, col_delete = st.columns(3)
    with col_save:
        if st.button("💾 Lưu file tạm thời", use_container_width=True, disabled=(khbd_cache is None), key="btn_save_khbd_v7"):
            st.sidebar.success("💾 Đã lưu cấu hình giáo án vào RAM phiên làm việc an toàn!")
    with col_download:
        if word_file is not None and khbd_cache is not None:
            saved_khbd_title = khbd_cache.get("ten_bai_save", "Moi").replace(" ", "_")
            st.download_button(label="📄 Tải file về máy", data=word_file, file_name=f"Giao_An_Ket_Noi_Tri_Thức_{saved_khbd_title}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True, key="btn_dl_word_khbd_v7_active")
        else:
            st.button("📄 Tải file về máy", disabled=True, use_container_width=True, key="btn_dl_word_khbd_v7_disabled")
    with col_delete:
        if st.button("❌ Xóa file", use_container_width=True, disabled=(khbd_cache is None), key="btn_del_khbd_v7"):
            st.session_state['khbd_delete_trigger'] = True
            st.rerun()
