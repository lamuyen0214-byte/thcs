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
    sys.path.insert(0, root_dir)

# Giữ nguyên khai báo đường dẫn cho thư mục export
export_path = os.path.abspath(os.path.join(root_dir, 'export'))
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

def render_khbd_module():
    # 1. CSS CỦA THẦY - GIỮ NGUYÊN
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

    # 2. GIAO DIỆN NHẬP LIỆU - GIỮ NGUYÊN CẤU TRÚC
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

    # =====================================================================
    # 3. LOGIC AI (ĐỘNG CƠ TRUNG TÂM MỚI)
    # =====================================================================
    if st.button("🚀 KHỞI TẠO TIẾN TRÌNH KẾ HOẠCH BÀI DẠY", type="primary", use_container_width=True, key="btn_run_khbd_unique"):
        if not ten_bai.strip():
            st.warning("⚠️ Vui lòng điền 'Tên bài học / Chủ đề bài dạy' trước khi kích hoạt.")
        else:
            api_key = get_api_key()
            if not api_key:
                st.error("⚠️ Lỗi xác thực: Vui lòng kiểm tra hoặc nhập lại API Key ở thanh bên (Sidebar)!")
                st.stop()

            with st.spinner("🤖 Trợ lý AI đang nghiên cứu tài liệu và thiết kế giáo án..."):
                # Đọc file tài liệu đính kèm
                file_context = ""
                if tai_lieu_file is not None:
                    try:
                        ext = tai_lieu_file.name.split(".")[-1].lower()
                        tai_lieu_file.seek(0)
                        if ext == "pdf":
                            from pypdf import PdfReader
                            reader = PdfReader(tai_lieu_file)
                            for page_idx in range(min(len(reader.pages), 15)):
                                p_text = reader.pages[page_idx].extract_text()
                                if p_text: file_context += p_text + "\n"
                        elif ext == "docx":
                            import docx
                            file_context += "\n".join([p.text for p in docx.Document(tai_lieu_file).paragraphs])
                        elif ext == "txt":
                            file_context = tai_lieu_file.read().decode("utf-8")
                    except Exception: pass

                if not file_context.strip(): 
                    file_context = "Không có tài liệu tham khảo cụ thể, giáo viên tự do phát triển nội dung."

                # Cấu trúc Prompt chuyên sâu
                system_instruction = f"Bạn là một Giáo viên xuất sắc và Chuyên gia sư phạm. Hãy thiết kế Kế hoạch bài dạy (Giáo án) môn {mon_hoc} dành cho học sinh {lop}. Chủ đề bài học: '{ten_bai}'. Thời lượng dự kiến: {thoi_luong} tiết. Trình bày nghiêm ngặt theo cấu trúc của mẫu: {mau_thiet_ke}. Yêu cầu đưa ra các hoạt động rõ ràng gồm: Mục tiêu, Nội dung, Sản phẩm dự kiến, và Tổ chức thực hiện."
                if bam_sat:
                    system_instruction += " Yêu cầu quan trọng: Phải bám sát 100% nội dung kiến thức trong tài liệu tham khảo được cung cấp."
                
                prompt_khbd = f"{system_instruction}\n\n[TÀI LIỆU THAM KHẢO]:\n{file_context[:6000]}"
                
                # Xác định mô hình
                mode = "pro" if "Pro" in model_display_name or "mở rộng" in model_display_name.lower() else "flash"
                
                # Gọi Engine AI
                result = run_ai_with_fallback(
                    prompt=prompt_khbd, 
                    api_key=api_key, 
                    model_mode=mode
                )

                if result.get("success"):
                    st.session_state['current_khbd_data'] = {
                        "is_khbd": True, "title": ten_bai, "ten_bai_save": str(ten_bai), 
                        "subject": mon_hoc, "grade": lop, "duration": str(thoi_luong), "style": mau_thiet_ke,
                        "ai_generated_content": result.get("text")
                    }
                    st.success(f"✅ Đã khởi tạo giáo án điện tử thành công trong {result.get('time'):.2f} giây! (Model: {result.get('model')})")
                    st.rerun()
                else:
                    st.error("❌ Lỗi hệ thống AI: Máy chủ từ chối phản hồi.")
                    with st.expander("🔍 Chi tiết lỗi kỹ thuật ngầm", expanded=True):
                        st.code(result.get("error"))

    # =====================================================================
    # 4. KẾT XUẤT VÀ LƯU TRỮ HỒ SƠ
    # =====================================================================
    st.markdown("---")
    st.markdown("##### 📥 Kết Xuất Kế Hoạch Bài Dạy")
    
    if st.session_state.get('delete_khbd_action'):
        if 'current_khbd_data' in st.session_state: del st.session_state['current_khbd_data']
        st.session_state['delete_khbd_action'] = False
        st.rerun()

    khbd_cache = st.session_state.get('current_khbd_data')
    word_file = None

    if khbd_cache:
        with st.expander("🔍 Xem trước Nội dung Kế hoạch bài dạy", expanded=True):
            st.markdown(khbd_cache["ai_generated_content"])
        
        WordEngine = get_word_engine()
        if WordEngine:
            try: word_file = WordEngine.export_to_word(khbd_cache)
            except Exception as e: st.error(f"💡 Trình kết xuất file Word đang đồng bộ: {e}")

    # BỘ 3 NÚT TĂM TẮP
    col_save, col_download, col_delete = st.columns(3)
    with col_save:
        if st.button("💾 Lưu file tạm thời", use_container_width=True, disabled=(khbd_cache is None), key="btn_save_khbd_final"):
            st.sidebar.success("💾 Đã lưu cấu hình giáo án vào phiên làm việc an toàn!")
    with col_download:
        if word_file is not None and khbd_cache is not None:
            saved_title = khbd_cache.get("ten_bai_save", "Giao_An").replace(" ", "_")
            st.download_button(label="📄 Tải file về máy", data=word_file, file_name=f"KHBD_{saved_title}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True, key="btn_dl_word_khbd_final")
        else:
            st.button("📄 Tải file về máy", disabled=True, use_container_width=True, key="btn_dl_word_khbd_dis_final")
    with col_delete:
        if st.button("❌ Xóa file", use_container_width=True, disabled=(khbd_cache is None), key="btn_del_khbd_final"):
            st.session_state['delete_khbd_action'] = True
            st.rerun()
