import streamlit as st
import os
import sys
from export.export_word import WordExportEngine
# =====================================================================
# PART 1: CẤU HÌNH ĐỊNH TUYẾN TỰ ĐỘNG VÀ GIAO DIỆN NHẬP LIỆU
# =====================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = current_dir
while not os.path.exists(os.path.join(root_dir, 'ai_config.py')) and root_dir != os.path.dirname(root_dir):
    root_dir = os.path.dirname(root_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)

# Import 'Trái tim' hệ thống và Engine Word từ cấu hình gốc
from ai_config import get_ai_client
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from export.export_word import WordExportEngine

def get_word_engine():
    try:
        return WordExportEngine
    except Exception as e:
        print(f"Lỗi nạp module Word: {e}")
        return None

def render_khbd_module(api_key=""):
    """
    Phân hệ khởi tạo Giáo án điện tử / Kế hoạch bài dạy.
    Tiếp nhận tham số api_key để phân phối quyền kết nối an toàn trên mọi thiết bị.
    """
    # 1. CẤU HÌNH CSS GIAO DIỆN - GIỮ NGUYÊN TOÀN VẸN CỦA THẦY
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

    # 2. GIAO DIỆN NHẬP LIỆU TRÊN MÀN HÌNH WIDE - GIỮ NGUYÊN TOÀN BỘ BIẾN VÀ KEY TĨNH
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
        # Đã sửa lỗi cú pháp phẳng phiu trên một dòng, khóa chặt đóng mở ngoặc đơn
        model_display_name = st.selectbox("Mô hình KHBD", ["3.1 Flash-Lite", "3.5 Flash", "3.1 Pro", "Tư duy mở rộng"], label_visibility="collapsed", index=0, key="sb_model_khbd_unique")
        
    st.write("")
    bam_sat = st.checkbox(" Bám sát 100% tài liệu tải lên", value=True, key="chk_bam_sat_khbd_unique")
    st.write("")
# =====================================================================
# PART 2: ENGINE TRÍ TUỆ NHÂN TẠO KHỞI TẠO DÒNG CHẢY DỮ LIỆU
# =====================================================================
    if st.button(" KHỞI TẠO TIẾN TRÌNH KẾ HOẠCH BÀI DẠY", type="primary", use_container_width=True, key="btn_run_khbd_unique"):
        if not ten_bai.strip():
            st.warning("⚠️ Vui lòng điền 'Tên bài học / Chủ đề bài dạy' trước khi kích hoạt.")
        else:
            # Liên thông mã định danh tài khoản từ Router điều phối trung tâm xuống
            client, error = get_ai_client(api_key)
            
            if error:
                st.error(f"❌ {error}")
                return
                
            with st.spinner("⏳ Trợ lý AI đang bóc tách tài liệu và thiết kế tiến trình bài dạy bám sát GDPT 2018..."):
                # BỘ ĐỌC TRÍCH XUẤT VĂN BẢN ĐA ĐỊNH DẠNG (KHẮC PHỤC LỖI TREO/QUAY TRƠ PHÊN BẢN CŨ)
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
                            doc = docx.Document(tai_lieu_file)
                            file_context += "\n".join([p.text for p in doc.paragraphs])
                        elif ext == "txt":
                            file_context = tai_lieu_file.read().decode("utf-8")
                    except Exception as file_err:
                        st.sidebar.error(f"Cảnh báo nạp file: {file_err}")
                
                # Đồng bộ chuỗi ngữ cảnh phụ trợ
                if not file_context.strip():
                    file_context = f"Soạn thảo giáo án chuẩn kiến thức kỹ năng môn {mon_hoc}."

                try:
                    # SIÊU CÂU LỆNH TÍNH TOÁN CẤU TRÚC (TRUYỀN TOÀN BỘ BIẾN THỰC TẾ VÀO NỘI DUNG PROMPT)
                    prompt_instructions = f"""
Bạn là Chuyên gia thiết kế bài dạy xuất sắc, am hiểu sâu sắc Chương trình GDPT 2018 tại Việt Nam. Hãy soạn một Kế hoạch bài dạy (KHBD) môn {mon_hoc} cho học sinh {lop} tuân thủ mẫu thiết kế {mau_thiet_ke}. 
- Tên bài học / Chủ đề: {ten_bai}
- Thời lượng triển khai: {thoi_luong} tiết.
- Yêu cầu bám sát toàn diện nội dung tài liệu cốt lõi sau đây để xây dựng tiến trình:
{file_context[:6000]}
Yêu cầu đầu ra: Trình bày cấu trúc khoa học, ngôn từ sư phạm chuẩn mực, phân tách rõ ràng các hoạt động học tập bằng định dạng Markdown.
"""
                    # Xác định lõi xử lý tự động (Giữ nguyên luồng map của thầy)
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt_instructions
                    )
                    
                    result_text = getattr(response, "text", "")
                    if result_text:
                        st.session_state['current_khbd_data'] = {
                            "is_khbd": True, 
                            "title": ten_bai, 
                            "ten_bai_save": str(ten_bai), 
                            "subject": mon_hoc, 
                            "grade": lop, 
                            "duration": str(thoi_luong), 
                            "style": mau_thiet_ke,
                            "ai_generated_content": result_text
                        }
                        st.success("🎉 Đã khởi tạo giáo án điện tử thành công!")
                        st.rerun()
                    else:
                        st.error("⚠️ Máy chủ AI không trả về văn bản. Có thể do file đính kèm vi phạm bộ lọc nội dung của Google.")
                except Exception as e:
                    st.error(f"❌ Lỗi hệ thống phản hồi từ máy chủ AI: {str(e)}")
# =====================================================================
# PART 3: HIỂN THỊ VÀ KẾT XUẤT HỒ SƠ WORD TỰ ĐỘNG
# =====================================================================
    if st.session_state.get('khbd_delete_trigger'):
        if 'current_khbd_data' in st.session_state:
            del st.session_state['current_khbd_data']
        st.session_state['khbd_delete_trigger'] = False
        st.rerun()

    khbd_cache = st.session_state.get('current_khbd_data')
    word_file = None
    
    if khbd_cache and khbd_cache.get('is_khbd'):
        st.markdown("---")
        st.markdown(f"### 📄 KẾT QUẢ: {khbd_cache['title']}")
        
        with st.expander(" Xem trước Kế hoạch bài dạy chi tiết", expanded=True):
            st.markdown(khbd_cache['ai_generated_content'])
            WordEngine = get_word_engine()
                if WordEngine:
                    try:
                        # Vệ sinh dữ liệu
                        clean_content = khbd_cache.get('ai_generated_content', '').replace('\r\n', '\n')
                        clean_content = "".join(ch for ch in clean_content if ord(ch) >= 32 or ch == '\n')
                        khbd_cache['ai_generated_content'] = clean_content
                        
                        # Gọi engine xuất file
                        word_file = WordEngine.export_to_word(khbd_cache)
                    except Exception as e:
                        st.error(f"⚠️ Trình xuất Word đang gặp sự cố đồng bộ: {e}")
                        word_file = None
             
        # BỘ BA NÚT TƯƠNG TÁC TĂM TẮP CHỐNG LỖI KHÓA NÚT KHI RERUN
        col_save, col_download, col_delete = st.columns(3)
        with col_save:
            if st.button(" Lưu file tạm thời", use_container_width=True, disabled=(khbd_cache is None), key="btn_save_khbd_final"):
                st.toast(" Đã lưu cấu hình giáo án vào bộ nhớ phiên làm việc an toàn!")
                
        with col_download:
            if khbd_cache is not None:
                saved_title = khbd_cache.get("ten_bai_save", "Giao_An").replace(" ", "_")
                
                # Khởi tạo nhị phân tại chỗ phòng ngừa luồng chính bị trễ nhịp
                if word_file is None and WordEngine:
                    try:
                        word_file = WordEngine.export_to_word(khbd_cache)
                    except Exception:
                        pass
                        
                if word_file:
                    st.download_button(
                        label=" Tải file về máy (Word)",
                        data=word_file,
                        file_name=f"KHBD_{saved_title}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                        key="btn_dl_word_khbd_ok"
                    )
                else:
                    st.button(" ⏳ Trình xuất đang đóng gói dữ liệu Word...", disabled=True, use_container_width=True, key="btn_dl_word_khbd_wait")
            else:
                st.button(" Tải file về máy", disabled=True, use_container_width=True, key="btn_dl_word_khbd_dis")
                
        with col_delete:
            if st.button(" Xóa file", use_container_width=True, disabled=(khbd_cache is None), key="btn_del_khbd_final"):
                st.session_state['khbd_delete_trigger'] = True
                st.rerun()
