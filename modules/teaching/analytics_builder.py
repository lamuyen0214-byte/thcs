import streamlit as st
import pandas as pd
import io
import docx
from ai_engine.ai_config import get_api_key
from ai_engine.ai_runner import run_ai_with_fallback

def render_analytics_module(api_key=""):
    # Tinh chỉnh CSS
    st.markdown("""
    <style>
    div[data-testid="stAppViewBlockContainer"], .main .block-container { padding-top: 3.5rem !important; padding-bottom: 3rem !important; }
    .stSelectbox label p, .stFileUploader label p, .stTextArea label p { color: #0000FF !important; font-weight: 600 !important; font-size: 14px !important; }
    .stMarkdown p strong { color: #FF0000 !important; font-size: 15px !important; }
    .stButton>button { font-weight: bold; border-radius: 6px; }
    </style>
    """, unsafe_allow_html=True)

    # 1. GIAO DIỆN NHẬP LIỆU
    col1, col2 = st.columns([1, 1])
    with col1:
        file_diem = st.file_uploader("📥 Tải lên Bảng điểm (Excel hoặc CSV)", type=['xlsx', 'xls', 'csv'])
    with col2:
        yeu_cau = st.text_area("Yêu cầu phân tích cụ thể (Tùy chọn)", placeholder="Ví dụ: Lọc ra 5 học sinh có điểm thấp nhất và đề xuất kế hoạch phụ đạo môn KHTN...", height=100)

    # 2. XỬ LÝ DỮ LIỆU & AI PHÂN TÍCH
    if file_diem is not None:
        try:
            # Đọc file dữ liệu
            if file_diem.name.endswith('.csv'):
                df = pd.read_csv(file_diem)
            else:
                df = pd.read_excel(file_diem)
            
            st.markdown("**👀 Xem trước Dữ liệu:**")
            st.dataframe(df.head(5), use_container_width=True) # Chỉ hiển thị 5 dòng đầu cho gọn

            if st.button("🤖 AI PHÂN TÍCH PHỔ ĐIỂM & VIẾT BÁO CÁO SƯ PHẠM", type="primary", use_container_width=True):
                # Chuyển dữ liệu thành chuỗi text để đưa cho AI đọc (Giới hạn 100 dòng để tránh quá tải)
                data_str = df.head(100).to_csv(index=False)
                final_key = api_key if api_key else get_api_key()
                
                prompt = f"""
Bạn là chuyên gia Phân tích Dữ liệu và Đo lường Đánh giá trong giáo dục.
Dưới đây là dữ liệu bảng điểm của học sinh (định dạng CSV):
{data_str}

Yêu cầu phân tích của giáo viên: {yeu_cau}

Hãy phân tích số liệu trên và viết một "BÁO CÁO ĐÁNH GIÁ KẾT QUẢ HỌC TẬP" với cấu trúc:
1. TỔNG QUAN PHỔ ĐIỂM: Đánh giá chung về mặt bằng điểm số (tỷ lệ giỏi/khá/TB/yếu, điểm trung bình...).
2. NHẬN DIỆN VẤN ĐỀ: Phân tích sâu xem học sinh đang làm tốt ở đâu, hổng kiến thức ở phần nào (nếu có dữ liệu điểm từng câu/từng phần). Chỉ đích danh các học sinh cần quan tâm đặc biệt.
3. KHUYẾN NGHỊ SƯ PHẠM: Đề xuất phương án điều chỉnh phương pháp dạy, kế hoạch bồi dưỡng học sinh giỏi và phụ đạo học sinh yếu.

Trình bày bằng Markdown khoa học, rõ ràng.
"""
                with st.spinner("AI đang tính toán thống kê và phân tích phổ điểm..."):
                    result = run_ai_with_fallback(prompt=prompt, api_key=final_key, model_mode="flash")
                    if result.get("success"):
                        st.session_state['current_analytics'] = result.get("text")
                    else:
                        st.error(f"❌ Lỗi AI: {result.get('error')}")

        except Exception as e:
            st.error(f"❌ Lỗi khi đọc file bảng điểm: {str(e)}\n\nThầy lưu ý file phải đúng chuẩn định dạng Excel/CSV nhé!")

    # 3. KẾT QUẢ VÀ XUẤT FILE WORD
    if 'current_analytics' in st.session_state:
        st.markdown("---")
        with st.expander("📊 BÁO CÁO PHÂN TÍCH CHẤT LƯỢNG HỌC TẬP", expanded=True):
            st.markdown(st.session_state['current_analytics'])
            
            def export_analytics_to_word(content):
                doc = docx.Document()
                doc.add_heading(f"BÁO CÁO PHÂN TÍCH KẾT QUẢ HỌC TẬP", 0)
                doc.add_paragraph(content)
                buffer = io.BytesIO()
                doc.save(buffer)
                buffer.seek(0)
                return buffer

            if st.button("📥 Tải Báo cáo Phân tích (Word)", use_container_width=True):
                word_file = export_analytics_to_word(st.session_state['current_analytics'])
                st.download_button("Xác nhận Tải Báo cáo", data=word_file, file_name="Bao_Cao_Phan_Tich_Diem.docx", use_container_width=True)
