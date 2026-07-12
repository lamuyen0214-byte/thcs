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
    bam_sat = st.checkbox("🎯 Bám sát 100% tài liệu tải lên", value=True)
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
                st.error("🛑 Lỗi xác thực: Vui lòng cấu hình nhập API Key cá nhân ở thanh bên (Sidebar) trước!")
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
                            pages_to_read = min(len(reader.pages), 25)
                            for p_idx in range(pages_to_read):
                                p_text = reader.pages[p_idx].extract_text()
                                if p_text: 
                                    file_context += p_text + "\n"
                        elif ext == "docx":
                            import docx
                            file_context += "\n".join([p.text for p in docx.Document(tai_lieu_file).paragraphs])
                        elif ext == "txt":
                            file_context += tai_lieu_file.read().decode("utf-8")
                    except Exception as extract_err:
                        print(f"Cảnh báo trích xuất file stream: {extract_err}")

                if bam_sat and tai_lieu_file is None:
                    st.error("🛑 LỖI NGHIỆP VỤ: Thầy đã tích chọn 'Bám sát 100% tài liệu tải lên' nhưng chưa nạp file tài liệu hoặc sách giáo khoa.")
                    return
                    
                if not file_context.strip(): 
                    file_context = f"Chủ đề trọng tâm bài dạy: {ten_bai}. Phân phối chương trình môn {mon_hoc} {lop} chuẩn quốc gia."
                
                # Đồng bộ cơ chế kiểm tra đường dẫn linh hoạt (prompts hoặc prompt)
                prompt_file_content = ""
                possible_paths = ["prompt/khbd_prompt.txt", "prompts/khbd_prompt.txt"]
                for p_path in possible_paths:
                    if os.path.exists(p_path):
                        try:
                            with open(p_path, "r", encoding="utf-8") as f:
                                prompt_file_content = f.read()
                            break
                        except Exception: pass
                        
                if not prompt_file_content.strip():
                    prompt_file_content = "Yêu cầu bắt buộc: Tích hợp sâu sắc 'Năng lực số' và ứng dụng 'Trí tuệ nhân tạo (AI)' vào các chuỗi hoạt động sư phạm."
                    
                from config.models import get_fallback_queue
                fallback_queue = get_fallback_queue(model_display_name)
                response_text = None
                from google import genai
                
                try:
                    client = genai.Client(api_key=str(user_raw_key))
                    system_instruction = f"""Bạn là Viện trưởng Viện Khoa học Giáo dục kiêm Chuyên gia khảo thí cao cấp tối cao của Bộ GD&ĐT Việt Nam. Kể từ năm 2026, Việt Nam sử dụng CHỈ DUY NHẤT bộ sách giáo khoa "Kết nối tri thức với cuộc sống" cho toàn quốc. Bạn bắt buộc phải bám sát cấu trúc phân phối chương trình và nội dung của duy nhất bộ sách này.
                    
[CẤU TRÚC QUY ĐỊNH BẮT BUỘC TỪ THẦY]:
{prompt_file_content}
 
Biên soạn tệp Kế hoạch bài dạy môn {mon_hoc} {lop} kiểu mẫu kế hoạch '{mau_thiet_ke}' thời lượng {thoi_luong} tiết bám sát văn bản [TÀI LIỆU GỐC]. Đầu ra bắt buộc chia rõ mục I. Mục tiêu bài dạy, II. Thiết bị dạy học và học liệu, III. Tiến trình 4 hoạt động sư phạm chuẩn quy định 5512."""

                    for current_model in fallback_queue:
                        try:
                            response = client.models.generate_content(
                                model=current_model, 
                                contents=[f"{system_instruction}\n\n[TÀI LIỆU GỐC SÁCH GIÁO KHOA ĐÍNH KÈM]:\n{file_context[:8000]}"]
                            )
                            if response and response.text:
                                response_text = response.text
                                break
                        except Exception: continue
                except Exception as api_err:
                    st.error(f"❌ Trục trặc kết nối AI: {api_err}")
                    return
                    
                if response_text:
                    st.session_state['current_khbd_data'] = {
                        "is_khbd": True, "title": ten_bai, "ten_bai_save": str(ten_bai), "subject": mon_hoc, 
                        "grade": lop, "duration": str(thoi_luong), "style": mau_thiet_ke,
                        "ai_generated_content": response_text
                    }
                    st.success("🎉 Đã khởi tạo giáo án điện tử thành công bám sát tệp tài liệu!")
                    st.rerun()

        st.markdown("---")
    st.markdown("##### Kết Xuất Hồ Sơ Giáo Án Sư Phạm Chuyên Nghiệp")
    
    if st.session_state.get('khbd_delete_trigger'):
        if 'current_khbd_data' in st.session_state: del st.session_state['current_khbd_data']
        if 'cached_word_file_khbd' in st.session_state: del st.session_state['cached_word_file_khbd']
        st.session_state['khbd_delete_trigger'] = False
        st.rerun()
        
    khbd_cache = st.session_state.get('current_khbd_data')
    
    # Khởi tạo vùng lưu trữ tệp Word bền vững phục vụ mô-đun KHBD
    if 'cached_word_file_khbd' not in st.session_state:
        st.session_state['cached_word_file_khbd'] = None

    if khbd_cache:
        with st.expander("📝 Xem trước Tiến trình Giáo án chi tiết (Chuẩn 5512)", expanded=True):
            st.markdown(khbd_cache["ai_generated_content"])
            
        # Tiến hành biên dịch giáo án sang định dạng Word lưu vững chắc vào session_state
        if st.session_state['cached_word_file_khbd'] is None:
            WordEngine = get_word_engine()
            if WordEngine:
                try:
                    st.session_state['cached_word_file_khbd'] = WordEngine.export_to_word(khbd_cache)
                except Exception as e:
                    st.error(f"⚠️ Trình dịch biểu mẫu Word đang đồng bộ cấu trúc văn bản: {e}")
                
    col_save, col_download, col_delete = st.columns(3)
    with col_save:
        if st.button("💾 Lưu file tạm thời", use_container_width=True, disabled=(khbd_cache is None), key="btn_save_khbd_v7"):
            st.sidebar.success(" Đã lưu cấu hình giáo án vào RAM phiên làm việc an toàn!")
            
    with col_download:
        # LUỒNG LOGIC ÉP BUỘC: Khóa chặt nút tải đi chung nhánh điều kiện sinh tệp Word
        if khbd_cache is not None and st.session_state['cached_word_file_khbd'] is not None:
            saved_khbd_title = khbd_cache.get("ten_bai_save", "Moi").replace(" ", "_")
            st.download_button(
                label="📥 Tải file về máy", 
                data=st.session_state['cached_word_file_khbd'],
                file_name=f"Giao_An_Ket_Noi_Tri_Thuc_{saved_khbd_title}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True, 
                key="btn_dl_word_khbd_v7_real_active"
            )
        else:
            st.button("📥 Tải file về máy", disabled=True, use_container_width=True, key="btn_dl_word_khbd_v7_disabled")
            
    with col_delete:
        if st.button("🗑️ Xóa file", use_container_width=True, disabled=(khbd_cache is None), key="btn_del_khbd_v7"):
            st.session_state['khbd_delete_trigger'] = True
            st.rerun()


