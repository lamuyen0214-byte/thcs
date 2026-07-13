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
    st.error(f"❌ Kỹ thuật: Mất kết nối đường ống tới ai_config.py tại {root_dir}")
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

def render_de_kt_module():
    # 1. CẤU HÌNH CSS ĐỂ KHÓA BỐ CỤC CỐ ĐỊNH CHỐNG NHẢY DÒNG CHỮ
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

    # 2. HÀNG 1: MENU ĐIỀU HƯỚNG CỐ ĐỊNH 4 CỘT
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

    st.write("")

    # 3. HÀNG 2: TỶ LỆ MỨC ĐỘ NHẬN THỨC
    st.markdown('<p class="header-red-title">Tỷ lệ mức độ nhận thức (%):</p>', unsafe_allow_html=True)
    col_tl1, col_tl2, col_tl3, col_tl4 = st.columns(4)
    with col_tl1: nhan_biet = st.number_input("**Nhận biết:**", value=40, step=5, format="%d", key="num_nb_de_kt")
    with col_tl2: thong_hieu = st.number_input("**Thông hiểu:**", value=30, step=5, format="%d", key="num_th_de_kt")
    with col_tl3: van_dung = st.number_input("**Vận dụng:**", value=20, step=5, format="%d", key="num_vd_de_kt")
    with col_tl4: van_dung_cao = st.number_input("**Vận dụng cao:**", value=10, step=5, format="%d", key="num_vdc_de_kt")

    # 4. TÊN BÀI VÀ FILE UPLOAD
    col_ten, col_file1, col_file2 = st.columns(3)
    with col_ten:
        st.markdown('<p class="header-red-title">Tên bài kiểm tra / Đề số:</p>', unsafe_allow_html=True)
        ten_bai = st.text_input("Tên bài", placeholder="Ví dụ: Kiểm tra đánh giá giữa kì I", label_visibility="collapsed", key="txt_ten_bai_de_kt")
    with col_file1:
        st.markdown('<p class="text-red-italic">Tải Đề Cương (.docx, .pdf):</p>', unsafe_allow_html=True)
        de_cuong_file = st.file_uploader("Đề cương", type=['docx', 'pdf'], label_visibility="collapsed", key="file_de_cuong_de_kt")
    with col_file2:
        st.markdown('<p class="text-red-italic">Tải Đề mẫu ma trận (.docx, .pdf):</p>', unsafe_allow_html=True)
        ma_tran_file = st.file_uploader("Ma trận", type=['docx', 'pdf'], label_visibility="collapsed", key="file_ma_tran_de_kt")

    # ... [Giữ nguyên logic tạo cột Trắc nghiệm/Tự luận của thầy tại đây] ...
    
    # 5. XỬ LÝ AI
    col_btn_run, col_model_sel = st.columns(2)
    with col_model_sel:
        model_display_name = st.selectbox("Mô hình", ["3.1 Flash-Lite", "3.5 Flash", "3.1 Pro", "Tư duy mở rộng"], label_visibility="collapsed", index=0, key="sb_model_ai_de_kt_run")
    with col_btn_run:
        activated = st.button("🚀 TỰ ĐỘNG KHỞI TẠO MA TRẬN VÀ ĐỀ THI", type="primary", use_container_width=True, key="btn_submit_run_de_kt")

    if activated:
        client = get_ai_client()
        if not client:
            st.error("⚠️ Vui lòng nhập API Key ở Sidebar!")
        else:
            with st.spinner("🤖 AI đang soạn đề..."):
                prompt = f"Soạn đề kiểm tra môn {mon_hoc} lớp {lop}. Chủ đề: {ten_bai}."
                response_text = None
                
                # Logic né lỗi 429
                for model_name in get_fallback_queue(model_display_name):
                    try:
                        response = client.models.generate_content(model=model_name, contents=prompt)
                        if response and response.text:
                            response_text = response.text
                            break
                    except Exception as e:
                        if "429" in str(e): continue
                
                if response_text:
                    st.session_state['current_exam_data'] = {"ai_generated_content": response_text, "ten_bai_save": str(ten_bai)}
                    st.success("✅ Thành công!")
                    st.rerun()
                else:
                    st.error("❌ Hết Quota trên tất cả model.")
