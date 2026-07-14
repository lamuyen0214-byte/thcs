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

    # 1. GIAO DIỆN NHẬP LIỆU ĐA CHIỀU
    col_mode, col_req = st.columns([1, 1])
    with col_mode:
        che_do = st.selectbox("🎯 Chọn Chế độ Phân tích", [
            "1. Phân tích Tổng quan Phổ điểm & Xếp loại",
            "2. Phân tích Chất lượng Câu hỏi (Item Analysis)",
            "3. Phân tích Đánh giá Năng lực / Rubric Dự án"
        ])
        file_diem = st.file_uploader("📥 Tải Bảng điểm (Excel/CSV)", type=['xlsx', 'xls', 'csv'])
    
    with col_req:
        yeu_cau = st.text_area("Yêu cầu trọng tâm cho AI (Tùy chọn)", placeholder="Ví dụ: Chỉ ra 5 học sinh yếu nhất cần phụ đạo gấp, phân tích xem học sinh hổng kiến thức ở câu nào nhiều nhất...", height=115)

    # 2. XỬ LÝ DASHBOARD & AI PHÂN TÍCH
    if file_diem is not None:
        try:
            # Đọc file
            df = pd.read_csv(file_diem) if file_diem.name.endswith('.csv') else pd.read_excel(file_diem)
            
            st.markdown("---")
            st.markdown("### 📊 Dashboard Thống kê Nhanh")
            
            # Giao diện Tabs cho Dashboard
            tab_data, tab_stats = st.tabs(["1️⃣ Dữ liệu thô", "2️⃣ Thống kê độ phân tán (Dành cho Cột số)"])
            with tab_data:
                st.dataframe(df.head(10), use_container_width=True)
            with tab_stats:
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    st.write(df[numeric_cols].describe())
                else:
                    st.info("Hệ thống không tìm thấy các cột định dạng số nguyên/số thực để thống kê phân tán.")

            if st.button("🤖 TIẾN HÀNH PHÂN TÍCH CHUYÊN SÂU", type="primary", use_container_width=True):
                # Chuyển đổi tối đa 150 dòng để AI không bị quá tải token
                data_str = df.head(150).to_csv(index=False)
                final_key = api_key if api_key else get_api_key()
                
                # THIẾT LẬP PROMPT ĐỘNG THEO CHẾ ĐỘ PHÂN TÍCH
                if "1" in che_do:
                    sys_role = "Chuyên gia Thống kê Giáo dục"
                    focus = "- Tỷ lệ phân bổ điểm (Giỏi/Khá/TB/Yếu).\n- Điểm mạnh chung của toàn lớp.\n- Phân nhóm học sinh: Nhóm nòng cốt và Nhóm rủi ro cần phụ đạo."
                elif "2" in che_do:
                    sys_role = "Chuyên gia Khảo thí và Đo lường"
                    focus = "- Nhận diện các câu hỏi/phần thi có tỷ lệ làm sai cao nhất.\n- Chẩn đoán nguyên nhân hổng kiến thức từ những câu sai đó.\n- Đề xuất điều chỉnh ma trận đề thi cho lần sau."
                else:
                    sys_role = "Chuyên gia Đánh giá Năng lực"
                    focus = "- Sự đồng đều giữa các tiêu chí (VD: Điểm thuyết trình vs Điểm sản phẩm).\n- Đánh giá kỹ năng thực hành/làm việc nhóm.\n- Nhận xét định tính rút ra từ dữ liệu."

                prompt = f"""
Bạn là {sys_role} hàng đầu. Dưới đây là dữ liệu điểm số/đánh giá (định dạng CSV):
{data_str}

Yêu cầu cụ thể của giáo viên: {yeu_cau}

Dựa vào bảng số liệu trên, hãy viết một "BÁO CÁO SƯ PHẠM" bám sát các trọng tâm sau:
{focus}

Yêu cầu trình bày:
- Dùng định dạng Markdown rõ ràng, chia mục khoa học.
- Dùng bảng biểu Markdown nếu cần so sánh.
- TUYỆT ĐỐI trung thực với số liệu, không bịa đặt tên học sinh hoặc điểm số không có trong file.
"""
                with st.spinner(f"AI đang kích hoạt {che_do}..."):
                    result = run_ai_with_fallback(prompt=prompt, api_key=final_key, model_mode="flash")
                    if result.get("success"):
                        st.session_state['current_analytics'] = result.get("text")
                    else:
                        st.error(f"❌ Lỗi AI: {result.get('error')}")

        except Exception as e:
            st.error(f"❌ Lỗi khi đọc file bảng điểm: {str(e)}\n\nThầy kiểm tra lại cấu trúc file Excel xem có bị gộp ô (merge cells) quá phức tạp không nhé.")

    # 3. KẾT QUẢ VÀ XUẤT FILE WORD
    if 'current_analytics' in st.session_state:
        st.markdown("---")
        with st.expander("📑 BÁO CÁO PHÂN TÍCH CHUYÊN SÂU SƯ PHẠM", expanded=True):
            st.markdown(st.session_state['current_analytics'])
            
            def export_analytics_to_word(content):
                doc = docx.Document()
                doc.add_heading(f"BÁO CÁO ĐÁNH GIÁ SƯ PHẠM", 0)
                doc.add_paragraph(content)
                buffer = io.BytesIO()
                doc.save(buffer)
                buffer.seek(0)
                return buffer

            if st.button("📥 Tải Báo cáo Phân tích (Word)", use_container_width=True):
                word_file = export_analytics_to_word(st.session_state['current_analytics'])
                st.download_button("Xác nhận Tải Báo cáo", data=word_file, file_name="Bao_Cao_Spham_AI.docx", use_container_width=True)
