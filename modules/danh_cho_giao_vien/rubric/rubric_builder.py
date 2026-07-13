import streamlit as st
import os
import sys

# =====================================================================
# KỸ THUẬT: ĐỊNH TUYẾN TỰ ĐỘNG TÌM "TRÁI TIM" AI_CONFIG.PY TẠI ROOT
# =====================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = current_dir
while not os.path.exists(os.path.join(root_dir, 'ai_config.py')) and root_dir != os.path.dirname(root_dir):
    root_dir = os.path.dirname(root_dir)

if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from ai_config import get_ai_client, get_fallback_queue
except ImportError:
    st.error(f"❌ Kỹ thuật: Mất kết nối đường ống tới ai_config.py")
    def get_ai_client(): return None
    def get_fallback_queue(m): return ["gemini-2.5-flash"]

# Đảm bảo hệ thống tìm thấy thư mục export
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

def get_word_engine():
    try:
        from export.export_word import WordExportEngine
        return WordExportEngine
    except Exception as e:
        st.error(f"Lỗi nạp module kết xuất Word: {e}")
        return None

def render_rubric_module():
    st.markdown("""
        <style>
        .header-blue {color: #0000FF; font-weight: bold; font-size: 15px; text-align: left; margin-bottom: 2px;}
        .header-red-title {color: #FF0000; font-weight: bold; font-size: 16px; margin-bottom: 5px;}
        .box-rubric {background-color: #D5E8D4; padding: 15px; border-radius: 8px; border-left: 5px solid #82B366; margin-bottom: 15px;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="box-rubric">📊 <b>Chuyên gia Khảo thí:</b> Khởi tạo bảng Rubric đánh giá đa chiều cho các dự án học tập, bài thuyết trình hoặc sản phẩm thực hành.</div>', unsafe_allow_html=True)

    # KHUNG NHẬP LIỆU
    st.markdown('<p class="header-red-title">Tên nhiệm vụ / Sản phẩm cần đánh giá:</p>', unsafe_allow_html=True)
    ten_nhiem_vu = st.text_input("Nhiệm vụ", placeholder="Ví dụ: Đánh giá dự án thiết kế hệ thống tiết kiệm điện thông minh...", label_visibility="collapsed")

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
        loai_rubric = st.selectbox("Loại Rubric", ["Đánh giá năng lực thực hành, thí nghiệm", "Đánh giá năng lực tư duy khoa học", "Đánh giá năng lực giao tiếp", "Đánh giá theo năng lực", "Đánh giá theo sản phẩm học tập"], label_visibility="collapsed", index=0)

    st.markdown('<p class="header-blue">Các tiêu chí trọng tâm (Tùy chọn):</p>', unsafe_allow_html=True)
    tieu_chi = st.text_area("Tiêu chí", placeholder="Ví dụ: Tính sáng tạo, Hoạt động nhóm, Khả năng ứng dụng thực tế...", height=70, label_visibility="collapsed")
    
    model_display_name = st.selectbox("Chọn mô hình AI:", ["3.1 Flash-Lite", "3.5 Flash", "3.1 Pro", "Tư duy mở rộng"], index=0)

    # XỬ LÝ AI VỚI LOGIC FALLBACK (NÉ LỖI 429)
    if st.button("🚀 TỰ ĐỘNG LẬP BẢNG RUBRIC", type="primary", use_container_width=True):
        if not ten_nhiem_vu.strip():
            st.warning("⚠️ Vui lòng nhập 'Tên nhiệm vụ' trước khi khởi tạo.")
            return

        client = get_ai_client()
        if not client:
            st.error("⚠️ Lỗi cấu hình: Vui lòng nhập Gemini API Key ở thanh bên (Sidebar)!")
            return

        with st.spinner("🤖 AI đang phân tích tiêu chí và lập ma trận đánh giá..."):
            system_instruction = f"Bạn là chuyên gia giáo dục. Hãy thiết kế bảng Rubric cho {ten_nhiem_vu} môn {mon_hoc} {lop}. Thang điểm: {thang_diem}. Tiêu chí: {tieu_chi}."
            
            response_text = None
            for model_name in get_fallback_queue(model_display_name):
                try:
                    response = client.models.generate_content(model=model_name, contents=system_instruction)
                    if response and response.text:
                        response_text = response.text
                        break
                except Exception as e:
                    if "429" in str(e): continue
                    else: st.error(f"Lỗi hệ thống: {e}"); break
            
            if response_text:
                st.session_state['current_rubric_data'] = {
                    "title": f"Rubric - {ten_nhiem_vu}",
                    "subject": mon_hoc, "grade": lop, "ten_bai_save": "Rubric_Danh_Gia",
                    "ai_generated_content": response_text
                }
                st.success("✅ Đã khởi tạo bảng Rubric thành công!")
                st.rerun()
            else:
                st.error("❌ Hệ thống AI hiện đang bận (hết Quota). Vui lòng thử lại sau giây lát.")

    # KẾT XUẤT WORD
    rubric_cache = st.session_state.get('current_rubric_data')
    if rubric_cache:
        with st.expander("🔍 Xem trước Bảng Rubric Đánh Giá", expanded=True):
            st.markdown(rubric_cache["ai_generated_content"])
        
        WordEngine = get_word_engine()
        if WordEngine:
            try:
                word_file = WordEngine.export_to_word(rubric_cache)
                st.download_button("📄 Tải Rubric (Word)", word_file, "Rubric_Danh_Gia.docx", use_container_width=True)
            except Exception as e: st.error(f"Lỗi kết xuất Word: {e}")
            
        if st.button("❌ Xóa bản nháp"):
            del st.session_state['current_rubric_data']
            st.rerun()
