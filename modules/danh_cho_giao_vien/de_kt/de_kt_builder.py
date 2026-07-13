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
    from ai_config import get_ai_client
except ImportError:
    st.error(f"❌ Kỹ thuật: Mất kết nối đường ống tới ai_config.py")
    def get_ai_client(): return None

# Đường dẫn export giữ nguyên theo yêu cầu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

def get_word_engine():
    try:
        from export.export_word import WordExportEngine
        return WordExportEngine
    except Exception as e:
        print(f"Lỗi nạp module Word: {e}")
        return None

def render_de_kt_module():
    # 1. CẤU HÌNH CSS - GIỮ NGUYÊN
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

    # 2. GIAO DIỆN HÀNG 1, 2, 3 - GIỮ NGUYÊN TOÀN BỘ CẤU TRÚC VÀ KEY
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

    # ... (Giữ nguyên các khối input và layout còn lại của thầy) ...
    # [Để tiết kiệm không gian, tôi chỉ liệt kê logic xử lý AI ở dưới đây]
    
    # 5. XỬ LÝ AI - TÍCH HỢP LOGIC NÉ LỖI 429
    if st.button("🚀 TỰ ĐỘNG KHỞI TẠO MA TRẬN VÀ ĐỀ THI", type="primary", use_container_width=True, key="btn_submit_run_de_kt"):
        client = get_ai_client()
        if not client:
            st.error("⚠️ Lỗi: Chưa có API Key!")
            return

        with st.spinner("AI đang soạn đề..."):
            # Hệ thống fallback model tự động
            fallback_models = ["gemini-2.5-flash", "gemini-1.5-pro", "gemini-1.5-flash"]
            system_instruction = f"Soạn đề môn {mon_hoc} lớp {lop}..." # Prompt gốc của thầy
            
            response_text = None
            for m in fallback_models:
                try:
                    response = client.models.generate_content(model=m, contents=system_instruction)
                    if response and response.text:
                        response_text = response.text
                        break
                except Exception as e:
                    if "429" in str(e): continue
                    else: st.error(f"Lỗi: {e}"); break
            
            if response_text:
                st.session_state['current_exam_data'] = {"ai_generated_content": response_text, "ten_bai_save": str(ten_bai)}
                st.rerun()
            else:
                st.error("❌ Hết hạn mức Quota trên tất cả model.")
