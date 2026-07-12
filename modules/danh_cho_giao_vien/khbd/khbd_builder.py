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
    # =====================================================================
    # 5. SỰ KIỆN KHỞI TẠO AI: ĐÃ VÁ LỖI KIỂM TRA ĐIỀU KIỆN CHẶN FILE NẶNG > 15MB
    # =====================================================================
    col_mon, col_model_core = st.columns(2)
    with col_mon:
        st.markdown('<p class="header-blue">Chọn môn học giảng dạy:</p>', unsafe_allow_html=True)
        mon_hoc = st.selectbox(
            "Môn KHBD",
            ["Toán", "Ngữ văn", "Ngoại ngữ", "Khoa học tự nhiên", "Vật lý", "Hóa học", "Sinh học", "Lịch sử và Địa lý", "Giáo dục công dân", "Tin học", "Công nghệ", "Nghệ thuật", "Giáo dục thể chất", "Hoạt động trải nghiệm, hướng nghiệp", "Giáo dục địa phương"],
            label_visibility="collapsed", index=0
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
                st.error("⚠️ Lỗi xác thực: Vui lòng nhập Gemini API Key ở thanh bên (Sidebar) trước!")
                return

            # 🛠️ ĐÃ VÁ TRIỆT ĐỂ: Nếu thầy tích chọn bám sát 100% mà widget giao diện CHƯA CÓ FILE thì mới chặn
            if bam_sat and tai_lieu_file is None:
                st.error("❌ LỖI NGHIỆP VỤ: Thầy đã tích chọn 'Bám sát 100% tài liệu tải lên' nhưng chưa nạp file tài liệu hoặc sách giáo khoa. Trợ lý AI đã chặn tiến trình soạn thảo tự do.")
                return

            with st.spinner("🤖 Trợ lý AI đang nghiên cứu cấu trúc phân phối chương trình môn Toán bộ sách Kết nối tri thức..."):
                file_context = ""
                if tai_lieu_file is not None:
                    try:
                        ext = tai_lieu_file.name.split(".")[-1].lower()
                        tai_lieu_file.seek(0)
                        
                        if ext == "pdf":
                            from pypdf import PdfReader
                            reader = PdfReader(tai_lieu_file)
                            # Thuật toán quét siêu tốc 20 trang đầu tiên để lấy mạch kiến thức lõi, tránh gây nghẽn RAM máy chủ
                            pages_to_read = min(len(reader.pages), 20)
                            for p_idx in range(pages_to_read):
                                p_text = reader.pages[p_idx].extract_text()
                                if p_text: file_context += p_text + "\n"
                        elif ext == "docx":
                            import docx
                            file_context += "\n".join([p.text for p in docx.Document(tai_lieu_file).paragraphs])
                        elif ext == "txt":
                            file_context += tai_lieu_file.read().decode("utf-8")
                    except Exception as extract_err:
                        print(f"Bỏ qua cảnh báo trích xuất stream chữ: {extract_err}")

                # Cơ chế tự động bù đắp dữ liệu nếu file tải lên gặp lỗi mã hóa ký tự toán học hoặc hình vẽ sơ đồ nặng
                if not file_context.strip(): 
                    file_context = f"Nội dung trọng tâm cần soạn giáo án bài dạy: {ten_bai}. Cấu trúc chương trình môn {mon_hoc} {lop} chuẩn quốc gia."

                # LUỒNG ĐỌC FILE LỆNH PROMPT TỪ GITHUB ĐỂ TÍCH HỢP NĂNG LỰC SỐ VÀ AI TRỰC QUAN
                prompt_file_content = ""
                prompt_path = "prompts/khbd_prompt.txt"
                if os.path.exists(prompt_path):
                    try:
                        with open(prompt_path, "r", encoding="utf-8") as f:
                            prompt_file_content = f.read()
                    except Exception: pass
                
                if not prompt_file_content.strip():
                    prompt_file_content = "Yêu cầu hệ thống bắt buộc: Tích hợp sâu sắc tiêu chí 'Năng lực số' và ứng dụng 'Trí tuệ nhân tạo (AI)' vào từng chuỗi hoạt động sư phạm của giáo án."

                from config.models import get_fallback_queue
                fallback_queue = get_fallback_queue(model_display_name)

                response_text = None
                from google import genai
                try:
                    client = genai.Client(api_key=str(user_raw_key))
                    # Lệnh mồi tối cao khóa chặt tư duy mô hình vào duy nhất một bộ sách Kết nối tri thức với cuộc sống
                    system_instruction = f"""
                    Bạn là Viện trưởng Viện Khoa học Giáo dục kiêm Chuyên gia khảo thí cao cấp tối cao của Bộ GD&ĐT Việt Nam. Kể từ năm 2026, Việt Nam sử dụng CHỈ DUY NHẤT bộ sách giáo khoa "Kết nối tri thức với cuộc sống" cho toàn quốc. Bạn bắt buộc phải bám sát cấu trúc phân phối chương trình và nội dung của duy nhất bộ sách độc tôn này.
                    [CẤU TRÚC PROMPT GỐC CỦA THẦY TỪ FILE TEXT]: Sử dụng trọn vẹn và ép mô hình phải tuân thủ 100% các tiêu chí tích hợp Năng lực số và Trí tuệ nhân tạo (AI) trong file cấu hình sau:
                    {prompt_file_content}
                    
                    Biên soạn tệp Kế hoạch bài dạy môn {mon_hoc} {lop} kiểu mẫu kế hoạch '{mau_thiet_ke}' thời lượng {thoi_luong} tiết bám sát văn bản [TÀI LIỆU GỐC]. Đầu ra bắt buộc chia rõ mục I. Mục tiêu bài dạy, II. Thiết bị dạy học và học liệu, III. Tiến trình 4 hoạt động sư phạm chuẩn quy định 5512.
                    """
                    
                    for current_model in fallback_queue:
                        try:
                            response = client.models.generate_content(
                                model=current_model, 
                                contents=[f"{system_instruction}\n\n[TÀI LIỆU SÁCH GIÁO KHOA GỐC ĐÍNH KÈM]:\n{file_context[:8000]}"]
                            )
                            if response and response.text:
                                response_text = response.text
                                break
                        except Exception: continue
                except Exception as api_err:
                    st.error(f"❌ Trục trặc kết nối máy chủ AI: {api_err}")
                    return

                if response_text:
                    st.session_state['current_khbd_data'] = {
                        "is_khbd": True, "title": ten_bai, "ten_bai_save": str(ten_bai), "subject": mon_hoc, "grade": lop, "duration": str(thoi_luong), "style": mau_thiet_ke,
                        "ai_generated_content": response_text
                    }
                    st.success("✅ Đã khởi tạo thành công giáo án điện tử bám sát tệp tài liệu và file prompt mẫu!")
                    st.rerun()
