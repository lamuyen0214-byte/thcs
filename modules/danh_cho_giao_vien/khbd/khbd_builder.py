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
        # DÁN CHÈN THÊM ĐOẠN NÀY VÀO TRONG CẶP THẺ <style> CỦA CẢ 2 FILE BUILDER KHBD VÀ DE_KT:
    st.markdown("""
        <style>
        /* Ép toàn bộ khối container chính của Streamlit bung rộng kịch trần lề trái và lề phải */
        .main .block-container {
            max-width: 98% !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }
        
        /* Giải phóng không gian cho thanh Tab để các phân hệ dàn hàng ngang thênh thang */
        .stTabs [data-baseweb="tab-list"] {
            width: 100% !important;
            max-width: 100% !important;
        }

        .header-blue {color: #0000FF; font-weight: bold; font-size: 16px; text-align: center;}
        .text-red-italic {color: #FF0000; font-style: italic; font-weight: bold; font-size: 14px;}
        .box-trac-nghiem {background-color: #FFF2CC; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .box-tu-luan {background-color: #D5E8D4; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .header-red-title {color: #FF0000; font-weight: bold; font-size: 16px; margin-bottom: 5px;}
        .chu-diem-co-nho {font-size: 11px !important; font-style: italic; white-space: nowrap !important; display: inline-block; margin-top: 10px;}
        </style>
    """, unsafe_allow_html=True)


    # ĐÃ ĐỒNG BỘ: Gắn key tĩnh 'txt_ten_bai_khbd_5512' khóa cứng chữ gõ của giáo viên chống trống khi rerun
    st.markdown('<p class="header-red-title">Tên bài học / Chủ đề bài dạy:</p>', unsafe_allow_html=True)
    ten_bai = st.text_input("Tên bài", placeholder="Ví dụ: Bài 4: Tốc độ chuyển động", label_visibility="collapsed", key="txt_ten_bai_khbd_5512")

    col_lop, col_mau, col_tiet, col_file = st.columns([1.5, 2, 1.5, 2])
    with col_lop:
        st.markdown('<p class="header-blue">Lớp:</p>', unsafe_allow_html=True)
        lop = st.selectbox("Lớp KHBD", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], label_visibility="collapsed", index=0)
    with col_mau:
        st.markdown('<p class="header-blue">Mẫu thiết kế:</p>', unsafe_allow_html=True)
        mau_thiet_ke = st.selectbox("Mẫu", ["Chuẩn 5512", "Rút gọn", "STEM"], label_visibility="collapsed", index=0)
    with col_tiet:
        st.markdown('<p class="header-blue">Thời lượng (Tiết):</p>', unsafe_allow_html=True)
        thoi_luong = st.number_input("Thời lượng", min_value=1, max_value=10, value=2, label_visibility="collapsed")
    with col_file:
        st.markdown('<p class="header-blue">Tài liệu (docx, pdf, txt):</p>', unsafe_allow_html=True)
        tai_lieu_file = st.file_uploader("Tài liệu đính kèm", type=['docx', 'pdf', 'txt'], label_visibility="collapsed")
    col_mon, col_model_core = st.columns(2)
    with col_mon:
        st.markdown('<p class="header-blue">Chọn môn học giảng dạy:</p>', unsafe_allow_html=True)
        mon_hoc = st.selectbox(
            "Môn KHBD",
            ["Toán", "Ngữ văn", "Ngoại ngữ", "Khoa học tự nhiên", "Vật lý", "Hóa học", "Sinh học", "Lịch sử và Địa lý", "Giáo dục công dân", "Tin học", "Công nghệ", "Nghệ thuật", "Giáo dục thể chất", "Hoạt động trải nghiệm, hướng nghiệp", "Giáo dục địa phương"],
            label_visibility="collapsed", index=3
        )
    with col_model_core:
        st.markdown('<p class="header-blue">Chọn lõi xử lý Trợ lý AI:</p>', unsafe_allow_html=True)
        model_display_name = st.selectbox(
            "Mô hình KHBD", ["3.1 Flash-Lite", "3.5 Flash", "3.1 Pro", "Tư duy mở rộng"], label_visibility="collapsed", index=0
        )

    st.write("")
    bam_sat = st.checkbox("🚩 Bám sát 100% tài liệu tải lên", value=True)
    st.write("")

    if st.button("🚀 KHỞI TẠO TIẾN TRÌNH KẾ HOẠCH BÀI DẠY", type="primary", use_container_width=True):
        if not ten_bai.strip():
            st.warning("⚠️ Vui lòng điền 'Tên bài học / Chủ đề bài dạy' trước khi kích hoạt.")
        else:
            user_raw_key = st.session_state.get("user_gemini_key", "").strip()
            if not user_raw_key:
                if "GEMINI_API_KEY" in st.secrets: user_raw_key = st.secrets["GEMINI_API_KEY"].strip()
                elif "GOOGLE_API_KEY" in st.secrets: user_raw_key = st.secrets["GOOGLE_API_KEY"].strip()

            if not user_raw_key:
                st.error("⚠️ Lỗi xác thực: Vui lòng cấu hình nhập API Key cá nhân ở thanh bên (Sidebar) trước!")
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
                            for p_idx in range(min(len(reader.pages), 30)):
                                p_text = reader.pages[p_idx].extract_text()
                                if p_text: file_context += p_text + "\n"
                        elif ext == "docx":
                            import docx
                            file_context += "\n".join([p.text for p in docx.Document(tai_lieu_file).paragraphs])
                    except Exception as e: print(e)

                if not file_context.strip(): file_context = f"Phạm vi đơn vị kiến thức trọng tâm của bài: {ten_bai}."

                model_mapping = {"3.1 Flash-Lite": "models/gemini-2.5-flash", "3.5 Flash": "models/gemini-2.5-flash", "3.1 Pro": "models/gemini-2.5-pro", "Tư duy mở rộng": "models/gemini-2.5-pro"}
                primary_model = model_mapping.get(model_display_name, "models/gemini-2.5-flash")
                fallback_queue = list(dict.fromkeys([primary_model, "models/gemini-2.5-flash", "models/gemini-2.5-pro"]))

                response_text = None
                from google import genai
                try:
                    client = genai.Client(api_key=str(user_raw_key))
                    system_instruction = f"Bạn là chuyên gia thẩm định chương trình giáo dục phổ thông Bộ GD&ĐT. Kể từ năm 2026, Việt Nam sử dụng CHỈ DUY NHẤT bộ sách 'Kết nối tri thức với cuộc sống'. Soạn tệp Kế hoạch bài dạy môn {mon_hoc} {lop} kiểu mẫu '{mau_thiet_ke}' thời lượng {thoi_luong} tiết bám sát tệp tài liệu đính kèm. Đầu ra bắt buộc có mục I. Mục tiêu, II. Thiết bị học liệu, III. Tiến trình 4 hoạt động 5512."
                    
                    for current_model in fallback_queue:
                        try:
                            response = client.models.generate_content(model=current_model, contents=[f"{system_instruction}\n\n[TÀI LIỆU GỐC]:\n{file_context[:8000]}"])
                            if response and response.text:
                                response_text = response.text
                                break
                        except Exception: continue
                except Exception as api_err:
                    st.error(f"❌ Trục trặc kết nối AI: {api_err}")
                    return

                if response_text:
                    # ĐÃ ĐỒNG BỘ: Khóa tĩnh chuỗi tên bài 'ten_bai_save' vào bộ đệm, bảo vệ an toàn khỏi rerun
                    st.session_state['current_khbd_data'] = {
                        "is_khbd": True, "title": ten_bai, "ten_bai_save": str(ten_bai), "subject": mon_hoc, "grade": lop, "duration": str(thoi_luong), "style": mau_thiet_ke,
                        "ai_content_raw": response_text
                    }
                    st.success("✅ Đã khởi tạo giáo án điện tử thành công!")
                    st.rerun()
    # =====================================================================
    # 6. KHU VỰC KẾT XUẤT HỒ SƠ GIÁO ÁN VÀ ĐỒNG BỘ MỞ KHÓA LUỒNG TẢI FILE WORD CHUẨN XỊN
    # =====================================================================
    st.markdown("---")
    st.markdown("##### 📥 Kết Xuất Hồ Sơ Giáo Án Sư Phạm Chuyên Nghiệp")
    
    if st.session_state.get('khbd_delete_trigger'):
        if 'current_khbd_data' in st.session_state: 
            del st.session_state['current_khbd_data']
        st.session_state['khbd_delete_trigger'] = False
        st.rerun()

    khbd_cache = st.session_state.get('current_khbd_data')
    word_file = None  # Khởi tạo luồng bytes thô ban đầu

    if khbd_cache:
        with st.expander("🔍 Xem trước Tiến trình Giáo án chi tiết (Chuẩn 5512)", expanded=True):
            st.markdown(khbd_cache["ai_content_raw"])

        WordEngine = get_word_engine()
        if WordEngine:
            try:
                # ĐÃ ĐỒNG BỘ: Ép cấu hình đồng nhất hai từ khóa nội dung để tệp export bốc dữ liệu sạch lỗi ngầm
                if "ai_generated_content" not in khbd_cache:
                    khbd_cache["ai_generated_content"] = khbd_cache["ai_content_raw"]
                
                # Thực thi luồng trích xuất Byte lưu trực tiếp vào bộ nhớ tạm thời của trang Web
                word_file = WordEngine.export_to_word(khbd_cache)
            except Exception as e:
                st.error(f"💡 Trình dịch biểu mẫu Word đang đồng bộ cấu trúc văn bản: {e}")

    # ĐÃ KHÓA CỐ ĐỊNH HÌNH 3: Luôn luôn dựng khung 3 nút hàng ngang song song kịch lề máy tính laptop
    col_save, col_download, col_delete = st.columns(3)
    
    with col_save:
        if st.button("💾 Lưu file tạm thời", use_container_width=True, disabled=(khbd_cache is None), key="btn_save_khbd_v7"):
            st.sidebar.success("💾 Đã lưu cấu hình giáo án vào RAM phiên làm việc an toàn!")
            
    with col_download:
        # ĐÃ MỞ KHÓA THÀNH CÔNG: Khi có luồng văn bản Word, nút bấm tải file lập tức sáng đèn xanh lá 100% khả dụng
        if word_file is not None and khbd_cache is not None:
            saved_khbd_title = khbd_cache.get("ten_bai_save", "Moi").replace(" ", "_")
            st.download_button(
                label="📄 Tải file về máy", 
                data=word_file,
                file_name=f"Giao_An_Ket_Noi_Tri_Thuc_{saved_khbd_title}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True, 
                key="btn_dl_word_khbd_v7_active"
            )
        else:
            # Khung nút mặc định màu xám khi trạng thái chờ, bảo vệ giao diện không bị co lệch hàng dòng
            st.button("📄 Tải file về máy", disabled=True, use_container_width=True, key="btn_dl_word_khbd_v7_disabled")
            
    with col_delete:
        if st.button("❌ Xóa file", use_container_width=True, disabled=(khbd_cache is None), key="btn_del_khbd_v7"):
            st.session_state['khbd_delete_trigger'] = True
            st.rerun()

