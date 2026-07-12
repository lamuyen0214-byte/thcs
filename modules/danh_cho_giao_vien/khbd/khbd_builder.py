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
    # 1. CẤU HÌNH CSS NỘI BỘ (KHÓA CHẶT BỐ CỤC THEO ĐÚNG HÌNH 2 VÀ HÌNH 3 CỦA THẦY)
    st.markdown("""
        <style>
        .header-blue {color: #0000FF; font-weight: bold; font-size: 15px; text-align: left; margin-bottom: 2px;}
        .text-red-italic {color: #FF0000; font-style: italic; font-weight: bold; font-size: 14px;}
        .header-red-title {color: #FF0000; font-weight: bold; font-size: 15px; margin-bottom: 5px;}
        </style>
    """, unsafe_allow_html=True)

    # 2. HÀNG NGANG 1 (HÌNH 2): TÊN BÀI HỌC / CHỦ ĐỀ BÀI DẠY
    st.markdown('<p class="header-red-title">Tên bài học / Chủ đề bài dạy:</p>', unsafe_allow_html=True)
    ten_bai = st.text_input("Tên bài", placeholder="Ví dụ: Bài 4: Tốc độ chuyển động", label_visibility="collapsed")

    # 3. HÀNG NGANG 2 (HÌNH 2): LỚP - MẪU THIẾT KẾ - THỜI LƯỢNG - TẢI LIỆU (CHIA 4 CỘT TĂM TẮP)
    col_lop, col_mau, col_tiet, col_file = st.columns([1.5, 2, 1.5, 2])
    
    with col_lop:
        st.markdown('<p class="header-blue">Lớp:</p>', unsafe_allow_html=True)
        lop = st.selectbox(
            "Lớp KHBD", 
            ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], 
            label_visibility="collapsed", index=0
        )
    with col_mau:
        st.markdown('<p class="header-blue">Mẫu thiết kế:</p>', unsafe_allow_html=True)
        mau_thiet_ke = st.selectbox(
            "Mẫu", 
            ["Chuẩn 5512", "Rút gọn", "STEM"], 
            label_visibility="collapsed", index=0
        )
    with col_tiet:
        st.markdown('<p class="header-blue">Thời lượng (Tiết):</p>', unsafe_allow_html=True)
        thoi_luong = st.number_input("Thời lượng", min_value=1, max_value=10, value=2, label_visibility="collapsed")
    with col_file:
        st.markdown('<p class="header-blue">Tài liệu (docx, pdf, txt):</p>', unsafe_allow_html=True)
        tai_lieu_file = st.file_uploader("Tài liệu đính kèm", type=['docx', 'pdf', 'txt'], label_visibility="collapsed")
    # 4. CHÈN BỔ SUNG: KHU VỰC CHỌN 16 MÔN HỌC GDPT 2018 VÀ SELECTBOX CHỌN MÔ HÌNH DỰ PHÒNG
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
            "Mô hình KHBD", 
            ["3.1 Flash-Lite", "3.5 Flash", "3.1 Pro", "Tư duy mở rộng"], 
            label_visibility="collapsed", index=0
        )

    st.write("")
    bam_sat = st.checkbox("🚩 Bám sát 100% tài liệu tải lên", value=True)
    st.write("")

    # 5. SỰ KIỆN CLICK NÚT BẤM (TÍCH HỢP AUTO-FALLBACK XÓA SỔ LỖI 503 VÀ KHÓA CHẶT BỘ SÁCH KẾT NỐI TRI THỨC)
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

            with st.spinner("🤖 Trợ lý AI đang áp dụng tri thức bộ sách Kết nối tri thức và thiết kế giáo án..."):
                # Đọc văn bản thô cưỡng ép con trỏ file stream về đầu trang tránh rỗng chữ
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
                        elif ext == "txt":
                            file_context += tai_lieu_file.read().decode("utf-8")
                    except Exception as e: print(e)

                if not file_context.strip():
                    file_context = f"Phạm vi đơn vị kiến thức trọng tâm của bài: {ten_bai}."

                model_mapping = {
                    "3.1 Flash-Lite": "models/gemini-2.5-flash", "3.5 Flash": "models/gemini-2.5-flash",
                    "3.1 Pro": "models/gemini-1.5-pro", "Tư duy mở rộng": "models/gemini-2.5-pro"
                }
                primary_model = model_mapping.get(model_display_name, "models/gemini-2.5-flash")
                fallback_queue = list(dict.fromkeys([primary_model, "models/gemini-2.5-flash", "models/gemini-1.5-pro", "models/gemini-2.5-pro"]))

                # SIÊU PHẢN PHỐI PROMPT 2026: Ép cứng bộ sách "Kết nối tri thức với cuộc sống" độc tôn
                system_instruction = f"""
                Bạn là chuyên gia thẩm định chương trình giáo dục phổ thông cao cấp của Bộ GD&ĐT Việt Nam.
                [RÀNG BUỘC PHÁP LÝ TỐI CAO NĂM 2026]: Kể từ năm 2026, Bộ Giáo dục thống nhất sử dụng CHỈ DUY NHẤT bộ sách giáo khoa "Kết nối tri thức với cuộc sống" cho toàn quốc. Bạn phải bám sát cấu trúc phân phối chương trình, thuật ngữ và mục tiêu cốt lõi của duy nhất bộ sách độc tôn này.
                [LUẬT KIỂM TRA LỆCH MÔN]: Đối chiếu môn học được chọn là "{mon_hoc}" với file [TÀI LIỆU GỐC]. Nếu phát hiện mâu thuẫn môn học, bạn bắt buộc dừng lại lập tức và xuất dòng chữ in hoa: "⚠️ CẢNH BÁO: PHÁT HIỆN MÂU THUẪN KIẾN THỨC. FILE TẢI LÊN KHÔNG PHẢI MÔN KHỞI TẠO." và không soạn giáo án. Nếu file lỗi stream chữ, hãy tự gọi tri thức nội tại của bộ sách Kết nối tri thức bám sát chủ đề "{ten_bai}" để bù đắp 100% dữ liệu.
                [CẤU TRÚC GIÁO ÁN YÊU CẦU]: Biên soạn tệp Kế hoạch bài dạy môn {mon_hoc} {lop} theo đúng kiểu mẫu thiết kế: "{mau_thiet_ke}". Thời lượng: {thoi_luong} tiết.
                Nội dung xuất ra bắt buộc chia rõ:
                I. MỤC TIÊU BÀI DẠY (Năng lực đặc thù bám sát môn học, Phẩm chất chủ đạo).
                II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU.
                III. TIẾN TRÌNH DẠY HỌC (Gồm 4 Hoạt động chuẩn 5512: HĐ1: Xác định nhiệm vụ; HĐ2: Hình thành kiến thức; HĐ3: Luyện tập; HĐ4: Vận dụng. Mỗi hoạt động viết rõ: Mục tiêu, Nội dung, Sản phẩm, Tổ chức thực hiện bám sát tiến trình sư phạm).
                """
                
                response_text = None
                from google import genai
                try:
                    client = genai.Client(api_key=str(user_raw_key))
                    for current_model in fallback_queue:
                        try:
                            response = client.models.generate_content(
                                model=current_model, contents=[f"{system_instruction}\n\n[TÀI LIỆU GỐC ĐÍNH KÈM]:\n{file_context[:8000]}"]
                            )
                            if response and response.text:
                                response_text = response.text
                                break
                        except Exception as e:
                            if "503" in str(e) or "429" in str(e) or "UNAVAILABLE" in str(e): continue
                            else: raise e
                except Exception as api_err:
                    st.error(f"❌ Trục trặc kết nối AI: {api_err}")
                    return

                if response_text:
                    # Khóa dữ liệu tĩnh vào bộ đệm, loại bỏ st.rerun() để tránh làm mất file khi deploy online
                    st.session_state['current_khbd_data'] = {
                        "is_khbd": True, "title": ten_bai, "subject": mon_hoc, "grade": lop, "duration": str(thoi_luong), "style": mau_thiet_ke,
                        "ai_content_raw": response_text
                    }
                    st.success("✅ Đã khởi tạo giáo án điện tử thành công!")
                else:
                    st.error("❌ Tất cả các cổng máy chủ của Google hiện đang bận. Thầy cô vui lòng thử lại sau ít phút!")
    # 6. KHU VỰC KẾT XUẤT HỒ SƠ GIÁO ÁN VÀ ĐỒNG BỘ BỘ 3 NÚT CHỨC NĂNG (HÌNH 3)
    st.markdown("---")
    st.markdown("##### 📥 Kết Xuất Hồ Sơ Giáo Án Sư Phạm Chuyên Nghiệp")
    
    # Xử lý sự kiện click của nút xóa file rác khỏi bộ đệm
    if st.session_state.get('khbd_delete_trigger'):
        if 'current_khbd_data' in st.session_state: del st.session_state['current_khbd_data']
        st.session_state['khbd_delete_trigger'] = False
        st.rerun()

    # Xử lý sự kiện nút lưu file tạm thời thông báo trạng thái
    if st.session_state.get('khbd_save_trigger'):
        st.sidebar.success("💾 Đã khóa lưu trữ file giáo án tạm thời vào RAM phiên làm việc an toàn!")
        st.session_state['khbd_save_trigger'] = False

    khbd_cache = st.session_state.get('current_khbd_data')

    if khbd_cache:
        with st.expander("🔍 Xem trước Tiến trình Giáo án chi tiết (Chuẩn 5512)", expanded=True):
            st.markdown(khbd_cache["ai_content_raw"])

        WordEngine = get_word_engine()
        if WordEngine:
            try:
                word_file = WordEngine.export_to_word(khbd_cache)
                
                # ÉP CHUẨN HÌNH 3: Bung hàng ngang 3 cột chứa song song 3 nút chức năng đối xứng
                col_save, col_download, col_delete = st.columns(3)
                
                with col_save:
                    if st.button("💾 Lưu file tạm thời", type="secondary", use_container_width=True, key="btn_save_khbd"):
                        st.session_state['khbd_save_trigger'] = True
                        st.rerun()
                with col_download:
                    st.download_button(
                        label="📄 Tải file về máy",
                        data=word_file,
                        file_name=f"Giao_An_Kết_Nối_Tri_Thức_{lop.replace(' ', '')}_{ten_bai.replace(' ', '_')[:15]}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                        key="btn_download_khbd"
                    )
                with col_delete:
                    if st.button("❌ Xóa file", type="secondary", use_container_width=True, key="btn_delete_khbd"):
                        st.session_state['khbd_delete_trigger'] = True
                        st.rerun()
            except Exception as doc_err:
                st.error(f"⚠️ Trình kết xuất file Word đang được cập nhật: {doc_err}")
    else:
        # Khóa trạng thái chờ hiển thị 3 nút màu xám mồi trực quan bám sát layout hành chính
        col_save, col_download, col_delete = st.columns(3)
        with col_save: st.button("💾 Lưu file tạm thời", type="secondary", use_container_width=True, disabled=True)
        with col_download: st.button("📄 Tải file về máy", type="secondary", use_container_width=True, disabled=True)
        with col_delete: st.button("❌ Xóa file", type="secondary", use_container_width=True, disabled=True)
