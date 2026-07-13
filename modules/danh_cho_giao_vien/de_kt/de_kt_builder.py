import streamlit as st
import os
import sys

# =====================================================================
# 1. ĐỊNH VỊ ĐƯỜNG DẪN GỐC TỰ ĐỘNG TÌM AI_ENGINE
# =====================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = current_dir
while not os.path.exists(os.path.join(root_dir, 'ai_engine')) and root_dir != os.path.dirname(root_dir):
    root_dir = os.path.dirname(root_dir)

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

export_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
if export_path not in sys.path:
    sys.path.append(export_path)

# =====================================================================
# 2. NẠP ĐỘNG CƠ TỪ KIẾN TRÚC MỚI
# =====================================================================
from ai_engine.ai_runner import run_ai_with_fallback

def get_word_engine():
    try:
        from export.export_word import WordExportEngine
        return WordExportEngine
    except Exception as e:
        print(f"Lỗi nạp module Word: {e}")
        return None

def render_de_kt_module(api_key=""): # THAM SỐ API_KEY ĐÃ ĐƯỢC THÊM VÀO ĐÂY
    # 1. CẤU HÌNH CSS
    st.markdown("""
        <style>
        div[data-testid="stAppViewBlockContainer"], .main .block-container, .stAppViewBlockContainer {
            max-width: 98% !important; width: 98% !important; padding-left: 1.5rem !important;
            padding-right: 1.5rem !important; padding-top: 1rem !important; padding-bottom: 1rem !important;
        }
        .header-blue {color: #0000FF; font-weight: bold; font-size: 16px; text-align: center;}
        .text-red-italic {color: #FF0000; font-style: italic; font-weight: bold; font-size: 14px;}
        .box-trac-nghiem {background-color: #FFF2CC; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .box-tu-luan {background-color: #D5E8D4; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .header-red-title {color: #FF0000; font-weight: bold; font-size: 16px; margin-bottom: 5px;}
        .chu-diem-co-nho {font-size: 12px !important; font-style: italic; white-space: nowrap !important; display: inline-block; margin-top: 10px;}
        </style>
    """, unsafe_allow_html=True)

    # 2. HÀNG 1: MENU ĐIỀU HƯỚNG
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<p class="header-blue">Chọn môn học</p>', unsafe_allow_html=True)
        mon_hoc = st.selectbox("Môn", ["Ngữ văn", "Toán", "Ngoại ngữ", "Giáo dục công dân", "Lịch sử và Địa lý", "Khoa học tự nhiên", "Vật Lý", "Hóa Học", "Sinh Học", "Công nghệ", "Tin học", "GDĐP", "HĐTN-HN"], label_visibility="collapsed", index=1, key="sb_mon_hoc_de_kt_unique")
    with col2:
        st.markdown('<p class="header-blue">Chọn lớp</p>', unsafe_allow_html=True)
        lop = st.selectbox("Lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], label_visibility="collapsed", index=2, key="sb_lop_de_kt_unique")
    with col3:
        st.markdown('<p class="header-blue">Hình thức kiểm tra</p>', unsafe_allow_html=True)
        hinh_thuc = st.selectbox("Hình thức", ["Trắc nghiệm & Tự luận", "Trắc nghiệm", "Tự Luận"], label_visibility="collapsed", key="sb_hinh_thuc_de_kt_unique")
    with col4:
        st.markdown('<p class="header-blue">Thời lượng kiểm tra</p>', unsafe_allow_html=True)
        thoi_gian = st.selectbox("Thời gian", ["45 phút", "60 phút", "90 phút", "120 phút"], label_visibility="collapsed", index=0, key="sb_thoi_gian_de_kt_unique")

    # (Lược bớt phần hiển thị giao diện để tập trung vào xử lý Logic phía dưới...)

    if st.button("🚀 TỰ ĐỘNG KHỞI TẠO MA TRẬN VÀ ĐỀ THI", type="primary", use_container_width=True, key="btn_submit_run_de_kt"):
        if not ten_bai.strip():
            st.warning("⚠️ Vui lòng nhập 'Tên bài kiểm tra / Đề số' trước khi khởi tạo.")
        else:
            # SỬ DỤNG API_KEY ĐƯỢC TRUYỀN VÀO HÀM
            if not api_key:
                st.error("⚠️ Lỗi hệ thống: Chưa nhận diện được API Key cá nhân hợp lệ.")
                st.stop()

            with st.spinner("AI đang soạn đề thi..."):
                # Gọi Engine với API_KEY truyền trực tiếp
                result = run_ai_with_fallback(
                    prompt=prompt_de_kt, 
                    api_key=api_key, 
                    model_mode=mode
                )

                if result.get("success"):
                    # Lưu cache...
                    st.success("✅ Hoàn tất!")
                    st.rerun()
                else:
                    st.error(f"❌ QUÁ TRÌNH KHỞI TẠO BỊ CHẶN: {result.get('error')}")

    # ... (phần kết xuất word giữ nguyên)
