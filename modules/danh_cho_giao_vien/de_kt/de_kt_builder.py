import streamlit as st
import os
import sys
from export.export_word import WordExportEngine
from ai_engine.ai_config import get_api_key
from ai_engine.ai_runner import run_ai_with_fallback

# 1. ĐỊNH VỊ ĐƯỜNG DẪN GỐC
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = current_dir
while not os.path.exists(os.path.join(root_dir, 'ai_engine')) and root_dir != os.path.dirname(root_dir):
    root_dir = os.path.dirname(root_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# 2. HÀM ENGINE BỔ TRỢ
def get_word_engine():
    try:
        from export.export_word import WordExportEngine
        return WordExportEngine
    except Exception as e:
        st.error(f"Lỗi nạp module Word: {e}")
        return None

def render_de_kt_module(api_key=""):
    # Cấu hình CSS
    st.markdown("""
    <style>
    div[data-testid="stAppViewBlockContainer"] { max-width: 98% !important; }
    .header-blue {color: #0000FF; font-weight: bold; font-size: 16px; text-align: center;}
    .box-trac-nghiem {background-color: #FFF2CC; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
    .box-tu-luan {background-color: #D5E8D4; padding: 10px; border-radius: 5px; color: #0000FF; font-weight: bold; text-align: center; font-size: 18px;}
    </style>
    """, unsafe_allow_html=True)

    # Nhập liệu
    col1, col2, col3, col4 = st.columns(4)
    with col1: mon_hoc = st.selectbox("Môn", ["Ngữ văn", "Toán", "Ngoại ngữ", "Giáo dục công dân", "Lịch sử và Địa lý", "Khoa học tự nhiên", "Vật Lý", "Hóa Học", "Sinh Học", "Công nghệ", "Tin học", "GDĐP", "HĐTN-HN"], key="sb_mon_de_kt")
    with col2: lop = st.selectbox("Lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"], key="sb_lop_de_kt")
    with col3: hinh_thuc = st.selectbox("Hình thức", ["Trắc nghiệm & Tự luận", "Trắc nghiệm", "Tự Luận"], key="sb_ht_de_kt")
    with col4: thoi_gian = st.selectbox("Thời gian", ["45 phút", "60 phút", "90 phút", "120 phút"], key="sb_tg_de_kt")

    # Tỷ lệ nhận thức
    c_tl1, c_tl2, c_tl3, c_tl4 = st.columns(4)
    with c_tl1: nb = st.number_input("Nhận biết", value=40, key="nb_kt")
    with c_tl2: th = st.number_input("Thông hiểu", value=30, key="th_kt")
    with c_tl3: vd = st.number_input("Vận dụng", value=20, key="vd_kt")
    with c_tl4: vdc = st.number_input("Vận dụng cao", value=10, key="vdc_kt")

    # Thông số đề
    col_tn, spacer, col_tl = st.columns([12, 1, 12])
    with col_tn:
        sl1 = st.number_input("SL MCQ", value=12, key="sl1"); d1 = st.number_input("Điểm MCQ", value=3.0, key="d1")
        sl2 = st.number_input("SL Đúng/Sai", value=1, key="sl2"); d2 = st.number_input("Điểm Đ/S", value=0.25, key="d2")
        sl3 = st.number_input("SL Điền khuyết", value=1, key="sl3"); d3 = st.number_input("Điểm ĐK", value=0.25, key="d3")
        sl4 = st.number_input("SL Ngắn", value=2, key="sl4"); d4 = st.number_input("Điểm Ngắn", value=0.5, key="d4")
    
    with col_tl:
        so_cau_tl = st.number_input("Số câu Tự luận", value=4, key="so_tl")
        diem_tl_list = [1.0 for _ in range(int(so_cau_tl))]

    ten_bai = st.text_input("Tên bài kiểm tra", key="txt_ten_bai")
    
    # Nút khởi tạo
    if st.button("TỰ ĐỘNG KHỞI TẠO MA TRẬN VÀ ĐỀ THI", type="primary", use_container_width=True):
        final_key = api_key if api_key else get_api_key()
        if not final_key: st.error("Lỗi: Thiếu API Key"); st.stop()
        
        prompt = f"Soạn đề {mon_hoc} {lop} chủ đề {ten_bai}..."
        result = run_ai_with_fallback(prompt=prompt, api_key=final_key, model_mode="flash")
        
        if result.get("success"):
            # LƯU Ý: GẮN is_khbd = False ĐỂ EXPORT_WORD NHẬN DIỆN LÀ ĐỀ KIỂM TRA
            st.session_state['current_exam_data'] = {
                "is_khbd": False, 
                "title": ten_bai,
                "ai_generated_content": result.get("text"),
                "subject": mon_hoc,
                "grade": lop
            }
            st.rerun()

    # Nút xuất Word
    exam_cache = st.session_state.get('current_exam_data')
    if exam_cache:
        st.markdown("---")
        WordEngine = get_word_engine()
        try:
            word_file = WordEngine.export_to_word(exam_cache)
            st.download_button("Tải file Đề thi về máy", data=word_file, file_name="De_Thi.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
        except Exception as e:
            st.error(f"Lỗi xuất Word: {e}")

render_de_kt_module()
