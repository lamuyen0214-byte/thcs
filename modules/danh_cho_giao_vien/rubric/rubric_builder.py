import streamlit as st
import os
import sys

# =====================================================================
# KỸ THUẬT: ĐỊNH TUYẾN TỰ ĐỘNG TÌM "TRÁI TIM" AI_CONFIG.PY TẠI ROOT (GIỮ NGUYÊN 100%)
# =====================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = current_dir
while not os.path.exists(os.path.join(root_dir, 'ai_config.py')) and root_dir != os.path.dirname(root_dir):
    root_dir = os.path.dirname(root_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from ai_config import get_ai_client
except ImportError:
    st.error(f" Kỹ thuật: Mất kết nối đường ống tới ai_config.py tại {root_dir}")
    def get_ai_client(api_key=""): return None

# Đảm bảo hệ thống tìm thấy thư mục export (GIỮ NGUYÊN 100%)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

def get_word_engine():
    try:
        from export.export_word import WordExportEngine
        return WordExportEngine
    except Exception as e:
        st.error(f"Lỗi nạp module kết xuất Word: {e}")
        return None

# CẤY DUY NHẤT THAM SỐ api_key ĐỂ ĐỒNG BỘ ĐĂNG NHẬP TRÊN CÁC MÁY TÍNH KHÁC NHAU
def render_rubric_module(api_key=""):
    st.markdown("""
    <style>
    .header-blue {color: #0000FF; font-weight: bold; font-size: 15px; text-align: left; margin-bottom: 2px;}
    .header-red-title {color: #FF0000; font-weight: bold; font-size: 16px; margin-bottom: 5px;}
    .box-rubric {background-color: #D5E8D4; padding: 15px; border-radius: 8px; border-left: 5px solid #82B366; margin-bottom: 15px;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="box-rubric"> <b>Chuyên gia Khảo thí:</b> Khởi tạo bảng Rubric đánh giá đa chiều cho các dự án học tập, bài thuyết trình hoặc sản phẩm thực hành.</div>', unsafe_allow_html=True)
    
    # KHUNG NHẬP LIỆU (GIỮ NGUYÊN 100%)
    st.markdown('<p class="header-red-title">Tên nhiệm vụ / Sản phẩm cần đánh giá:</p>', unsafe_allow_html=True)
    ten_nhiem_vu = st.text_input("Nhiệm vụ", placeholder="Ví dụ: Đánh giá dự án thiết kế hệ thống tiết kiệm điện thông minh...", label_visibility="collapsed")
    
    # --- ĐOẠN CHIA 4 CỘT CÙNG HÀNG Ở ĐÂY (GIỮ NGUYÊN 100%) ---
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1.5])
    with col1:
        st.markdown('<p class="header-blue">Môn học:</p>', unsafe_allow_html=True)
        mon_hoc = st.selectbox("Môn học Rubric", ["Khoa học tự nhiên", "Vật lý", "Hóa học", "Sinh học", "Toán", "Công nghệ"], label_visibility="collapsed", index=0)
    with col2:
        st.markdown('<p class="header-blue">Đối tượng:</p>', unsafe_allow_html=True)
        lop = st.selectbox("Lớp Rubric", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], label_visibility="collapsed", index=3)
    with col3:
        st.markdown('<p class="header-blue">Thang điểm:</p>', unsafe_allow_html=True)
        thang_diem = st.selectbox("Thang điểm", ["Thang điểm 10", "Thang điểm 100", "Theo mức độ (Tốt, Khá, Đạt, CĐ)"], label_visibility="collapsed", index=0)
    with col4:
        st.markdown('<p class="header-blue">Loại Rubric:</p>', unsafe_allow_html=True)
        loai_rubric = st.selectbox(
            "Loại Rubric", 
            [
                "Đánh giá năng lực thực hành, thí nghiệm",
                "Đánh giá năng lực tư duy khoa học",
                "Đánh giá năng lực giao tiếp",
                "Đánh giá năng lực sử dụng CNTT",
                "Đánh giá theo năng lực",
                "Đánh giá theo sản phẩm học tập",
                "Đánh giá theo hoạt động",
                "Đánh giá theo bài kiểm tra",
                "Đánh giá theo quá trình",
                "Đánh giá phẩm chất",
                "Đánh giá năng lực chung",
                "Đánh giá năng lực đặc thù môn học",
                "Đánh giá khác"
            ], 
            label_visibility="collapsed", 
            index=0
        )
        
    st.markdown('<p class="header-blue">Các tiêu chí trọng tâm (Tùy chọn):</p>', unsafe_allow_html=True)
    tieu_chi = st.text_area("Tiêu chí", placeholder="Ví dụ: Tính sáng tạo, Hoạt động nhóm, Khả năng ứng dụng thực tế, Trình bày báo cáo...", height=70, label_visibility="collapsed")
    st.write("")
    # XỬ LÝ AI VỚI MÃ LỆNH MỚI BÁM SÁT GDPT 2018 (SỬA ĐỔI DUY NHẤT: ĐỒNG BỘ KEY CẤU HÌNH)
    if st.button(" TỰ ĐỘNG LẬP BẢNG RUBRIC", type="primary", use_container_width=True):
        if not ten_nhiem_vu.strip():
            st.warning(" Vui lòng nhập 'Tên nhiệm vụ' trước khi khởi tạo.")
            return
            
        # =====================================================================
        # GỌI BỘ ĐIỀU KHIỂN TRUNG TÂM & KIỂM TRA CHỐNG LỖI NONETYPE (ĐÃ TRUYỀN THAM SỐ)
        # =====================================================================
        # Chuyển tiếp tham số api_key nhận từ file chạy chính xuống hàm tạo client để xử lý thiết bị khác nhau
        client = get_ai_client(api_key=api_key)
        
        if client is None:
            st.error(" Lỗi cấu hình: Vui lòng nhập Gemini API Key ở thanh bên (Sidebar) trước!")
            return
        if not hasattr(client, 'models'):
            st.error(" Lỗi kỹ thuật: Client không đúng chuẩn SDK google-genai mới.")
            return
            
        with st.spinner(" AI đang phân tích tiêu chí và lập ma trận đánh giá..."):
            try:
                # Hệ thống cấu trúc tạo ma trận Rubric chuyên sâu (GIỮ NGUYÊN TOÀN VẸN 100%)
                system_instruction = f"""
Bạn là Chuyên gia Đo lường và Đánh giá Giáo dục, am hiểu sâu sắc Chương trình GDPT 2018. Nhiệm vụ của bạn là thiết kế một bảng Rubric đánh giá chi tiết cho môn {mon_hoc} {lop}.
Thông tin dự án/nhiệm vụ:
- Nhiệm vụ/Sản phẩm học sinh cần thực hiện: {ten_nhiem_vu}.
- Thang điểm áp dụng: {thang_diem}.
- Loại hình/Đối tượng đánh giá: {loai_rubric}.
- Các tiêu chí trọng tâm: {tieu_chi if tieu_chi else 'Kiến thức chuyên môn, Kỹ năng thực hành, Trình bày & Thái độ'}.
YÊU CẦU ĐỊNH DẠNG ĐẦU RA (BẮT BUỘC):
1. NGÔN NGỮ: Bắt buộc viết 100% bằng Tiếng Việt. Văn phong khoa học, chuẩn sư phạm.
2. CẤU TRÚC TRÌNH BÀY:
 - Phần 1: Mục đích đánh giá (Viết ngắn gọn 2-3 dòng).
 - Phần 2: Bảng Rubric chính (Trình bày bằng BẢNG MARKDOWN). Gồm các cột: Tiêu chí, Trọng số (%), Tốt, Khá, Đạt, Cần cố gắng. Mô tả hành vi năng lực phải rõ ràng.
 - Phần 3: Biểu mẫu ghi chú. TUYỆT ĐỐI KHÔNG dùng các đường kẻ ngang liên tục. Hãy tạo một Bảng Markdown gồm 3 cột: "STT", "Họ tên học sinh/Nhóm", "Ghi chú minh chứng".
 """
                
                # Gọi API chuẩn SDK mới (GIỮ NGUYÊN 100%)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=system_instruction
                )
                
                result = getattr(response, "text", "")
                
                if result:
                    st.session_state['current_rubric_data'] = {
                        "is_khbd": True, # Mượn cờ True để dùng cấu trúc xuất Word ổn định nhất
                        "title": f"Rubric - {ten_nhiem_vu}",
                        "subject": mon_hoc,
                        "grade": lop,
                        "ten_bai_save": "Rubric_Danh_Gia",
                        "ai_generated_content": result
                    }
                    st.success(" Đã khởi tạo bảng Rubric thành công!")
                    st.rerun()
                else:
                    st.warning(" AI không trả về nội dung. Có thể bị chặn bởi bộ lọc an toàn.")
            except Exception as api_err:
                st.error(f" Lỗi máy chủ AI: {api_err}")

    # KẾT XUẤT WORD (GIỮ NGUYÊN TOÀN VẸN CẤU TRÚC PHÂN TÁCH HAI CỘT ĐỀU NHAU CỦA THẦY)
    st.markdown("---")
    rubric_cache = st.session_state.get('current_rubric_data')
    if rubric_cache:
        with st.expander(" Xem trước Bảng Rubric Đánh Giá", expanded=True):
            st.markdown(rubric_cache["ai_generated_content"])
            
        WordEngine = get_word_engine()
        word_file = None
        if WordEngine:
            try:
                word_file = WordEngine.export_to_word(rubric_cache)
            except Exception as e:
                st.error(f" Trình xuất Word đang gặp sự cố đồng bộ: {e}")
                
        col_dl, col_del = st.columns(2)
        with col_dl:
            if word_file:
                st.download_button(
                    label=" Tải Rubric (Word)", 
                    data=word_file, 
                    file_name="Rubric_Danh_Gia.docx", 
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            else:
                st.button(" Tải Rubric (Đang chờ xử lý)", disabled=True, use_container_width=True)
                
        with col_del:
            if st.button(" Xóa bản nháp", use_container_width=True):
                del st.session_state['current_rubric_data']
                st.rerun()
