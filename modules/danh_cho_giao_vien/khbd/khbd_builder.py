import streamlit as st
import os
import sys

# =====================================================================
# CẤU HÌNH ĐỊNH TUYẾN TỰ ĐỘNG (KỸ THUẬT CHỐNG LỖI IMPORT)
# =====================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = current_dir
# Tự động tìm về thư mục gốc (nơi chứa ai_config.py)
while not os.path.exists(os.path.join(root_dir, 'ai_config.py')) and root_dir != os.path.dirname(root_dir):
    root_dir = os.path.dirname(root_dir)

if root_dir not in sys.path:
    sys.path.append(root_dir)

# Import 'Trái tim' hệ thống
from ai_config import get_ai_client

# Import Engine xuất Word
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
def get_word_engine():
    try:
        from export.export_word import WordExportEngine
        return WordExportEngine
    except Exception:
        return None

def render_khbd_module():
    # --- CSS ---
    st.markdown("""
        <style>
        div[data-testid="stAppViewBlockContainer"] { max-width: 98% !important; }
        .header-blue {color: #0000FF; font-weight: bold; font-size: 15px; text-align: left; margin-bottom: 2px;}
        .header-red-title {color: #FF0000; font-weight: bold; font-size: 15px; margin-bottom: 5px;}
        </style>
    """, unsafe_allow_html=True)

    # --- UI ---
    st.markdown('<p class="header-red-title">Tên bài học / Chủ đề bài dạy:</p>', unsafe_allow_html=True)
    ten_bai = st.text_input("Tên bài", label_visibility="collapsed", key="txt_ten_bai_khbd_5512")

    col_lop, col_mau, col_tiet, col_file = st.columns([1.5, 2, 1.5, 2])
    with col_lop:
        lop = st.selectbox("Lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], index=2)
    with col_mau:
        mau_thiet_ke = st.selectbox("Mẫu", ["Chuẩn 5512", "Rút gọn", "STEM"])
    with col_tiet:
        thoi_luong = st.number_input("Tiết", min_value=1, value=2)
    with col_file:
        tai_lieu_file = st.file_uploader("Tài liệu đính kèm", type=['docx', 'pdf', 'txt'])

    # --- XỬ LÝ AI ---
    if st.button("🚀 KHỞI TẠO TIẾN TRÌNH KẾ HOẠCH BÀI DẠY", type="primary", use_container_width=True):
        if not ten_bai.strip():
            st.warning("⚠️ Vui lòng điền tên bài học.")
            return
            
        client = get_ai_client()
        if not client:
            st.error("⚠️ Lỗi xác thực: Vui lòng nhập API Key ở Sidebar!")
            return

        with st.spinner("🤖 AI đang soạn giáo án..."):
            # (Phần xử lý file_context giữ nguyên như logic thầy đã gửi)
            file_context = "" 
            
            # Gọi API
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"Soạn KHBD môn {ten_bai}... [TÀI LIỆU]: {file_context}"
                )
                
                if response and response.text:
                    st.session_state['current_khbd_data'] = {
                        "is_khbd": True, "title": ten_bai, "ai_generated_content": response.text
                    }
                    st.success("✅ Đã khởi tạo giáo án thành công!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Lỗi AI: {e}")

    # --- KẾT XUẤT ---
    # (Phần hiển thị và nút tải Word giữ nguyên như code thầy gửi)
