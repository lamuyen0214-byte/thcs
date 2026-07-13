import streamlit as st
import os
import sys

# =====================================================================
# 1. ĐỊNH VỊ ĐƯỜNG DẪN GỐC
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

from ai_engine.ai_config import get_api_key
from ai_engine.ai_runner import run_ai_with_fallback

def get_word_engine():
    try:
        from export.export_word import WordExportEngine
        return WordExportEngine
    except Exception as e:
        st.error(f"Lỗi nạp module Word: {e}")
        return None

# =====================================================================
# 2. HÀM RENDER CHÍNH (ĐÃ BỌC CƠ CHẾ XỬ LÝ LỖI)
# =====================================================================
def render_de_kt_module(api_key=""):
    # Bao bọc container để cách ly giao diện
    with st.container():
        st.markdown("""
        <style>
        .header-blue {color: #0000FF; font-weight: bold; font-size: 16px; text-align: center;}
        .text-red-italic {color: #FF0000; font-style: italic; font-weight: bold; font-size: 14px;}
        .box-trac-nghiem {background-color: #FFF2CC; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .box-tu-luan {background-color: #D5E8D4; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
        .header-red-title {color: #FF0000; font-weight: bold; font-size: 16px; margin-bottom: 5px;}
        .chu-diem-co-nho {font-size: 12px !important; font-style: italic; white-space: nowrap !important; display: inline-block; margin-top: 10px;}
        </style>
        """, unsafe_allow_html=True)

        # -- UI INPUT --
        col1, col2, col3, col4 = st.columns(4)
        with col1: mon_hoc = st.selectbox("Môn", ["Ngữ văn", "Toán", "Ngoại ngữ", "Giáo dục công dân", "Lịch sử và Địa lý", "Khoa học tự nhiên", "Vật Lý", "Hóa Học", "Sinh Học", "Công nghệ", "Tin học", "GDĐP", "HĐTN-HN"], index=1, key="sb_mon_de_kt")
        with col2: lop = st.selectbox("Lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], index=2, key="sb_lop_de_kt")
        with col3: hinh_thuc = st.selectbox("Hình thức", ["Trắc nghiệm & Tự luận", "Trắc nghiệm", "Tự Luận"], key="sb_ht_de_kt")
        with col4: thoi_gian = st.selectbox("Thời gian", ["45 phút", "60 phút", "90 phút", "120 phút"], key="sb_tg_de_kt")

        c_tl1, c_tl2, c_tl3, c_tl4 = st.columns(4)
        nhan_biet = c_tl1.number_input("Nhận biết (%)", value=40, key="nb_kt")
        thong_hieu = c_tl2.number_input("Thông hiểu (%)", value=30, key="th_kt")
        van_dung = c_tl3.number_input("Vận dụng (%)", value=20, key="vd_kt")
        van_dung_cao = c_tl4.number_input("Vận dụng cao (%)", value=10, key="vdc_kt")

        ten_bai = st.text_input("Tên bài kiểm tra / Đề số", key="txt_ten_bai")
        
        # -- NÚT KHỞI TẠO --
        if st.button(" TỰ ĐỘNG KHỞI TẠO MA TRẬN VÀ ĐỀ THI ", type="primary", use_container_width=True):
            if not ten_bai.strip():
                st.warning("Vui lòng nhập Tên bài kiểm tra!")
            else:
                final_key = api_key if api_key and api_key.strip() else get_api_key()
                if not final_key:
                    st.error("Lỗi: Không tìm thấy API Key. Vui lòng kiểm tra Sidebar.")
                else:
                    # Bắt đầu gọi AI với Spinner an toàn
                    try:
                        with st.spinner("Đang kết nối AI và khởi tạo cấu trúc đề..."):
                            prompt = f"Soạn đề {mon_hoc} {lop}, Tỷ lệ: {nhan_biet}/{thong_hieu}/{van_dung}/{van_dung_cao}. Chủ đề: {ten_bai}"
                            result = run_ai_with_fallback(prompt=prompt, api_key=final_key, model_mode="flash")
                        
                        if result.get("success"):
                            st.session_state['current_exam_data'] = {
                                "is_khbd": False,
                                "type": hinh_thuc,
                                "ten_bai_save": ten_bai,
                                "ai_generated_content": result.get("text")
                            }
                            st.success("Khởi tạo hoàn tất!")
                            st.rerun()
                        else:
                            st.error(f"AI từ chối phản hồi: {result.get('error', 'Lỗi không xác định')}")
                    except Exception as e:
                        st.error(f"Lỗi hệ thống nghiêm trọng: {str(e)}")

        # -- XỬ LÝ KẾT QUẢ --
        if 'current_exam_data' in st.session_state:
            exam_cache = st.session_state['current_exam_data']
            st.markdown("---")
            with st.expander("Xem nội dung đề thi", expanded=True):
                st.markdown(exam_cache["ai_generated_content"])
            
            WordEngine = get_word_engine()
            if WordEngine:
                if st.button("Tải file Đề thi (Word)", type="primary"):
                    try:
                        word_file = WordEngine.export_to_word(exam_cache)
                        st.download_button("Tải về máy", data=word_file, file_name=f"{exam_cache['ten_bai_save']}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                    except Exception as e:
                        st.error(f"Lỗi kết xuất Word: {e}")

            if st.button("Xóa đề hiện tại"):
                del st.session_state['current_exam_data']
                st.rerun()
