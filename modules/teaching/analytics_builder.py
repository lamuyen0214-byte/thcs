import streamlit as st
import pandas as pd
import io
import docx
from ai_engine.ai_config import get_api_key
from ai_engine.ai_runner import run_ai_with_fallback

def load_and_clean_data(file):
    """Hàm xử lý thông minh để dọn rác file Excel từ SMAS, vnEdu"""
    try:
        if hasattr(file, 'seek'):
            file.seek(0)
            
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
            
        df_raw = pd.read_excel(file, header=None)
        
        header_idx = -1
        for i in range(min(20, len(df_raw))):
            row_values = [str(val).lower() for val in df_raw.iloc[i].values]
            if any('họ và tên' in val or 'họ tên' in val for val in row_values):
                header_idx = i
                break
                
        if header_idx != -1:
            header_row_1 = df_raw.iloc[header_idx].ffill()
            
            if header_idx + 1 < len(df_raw):
                header_row_2 = df_raw.iloc[header_idx + 1].fillna('')
            else:
                header_row_2 = [''] * len(header_row_1)
            
            new_headers = []
            for h1, h2 in zip(header_row_1, header_row_2):
                h1_str = str(h1).strip() if pd.notna(h1) else ""
                h2_str = str(h2).strip() if pd.notna(h2) and str(h2).strip() not in ['', 'nan', 'none'] else ""
                
                if h2_str:
                    new_headers.append(f"{h1_str} ({h2_str})")
                else:
                    new_headers.append(h1_str)
                    
            df_clean = df_raw.iloc[header_idx + 2:].copy()
            df_clean.columns = [str(c) for c in new_headers]
            
            # Xóa các cột trống
            df_clean = df_clean.loc[:, [c for c in df_clean.columns if str(c).lower() not in ['nan', 'none', ''] and str(c).strip() != '']]
            
            # Xóa các dòng rỗng (Không có dữ liệu ở cột Họ và tên)
            name_col_list = [c for c in df_clean.columns if 'họ và tên' in str(c).lower() or 'họ tên' in str(c).lower()]
            if name_col_list:
                name_col = name_col_list[0]
                df_clean = df_clean.dropna(subset=[name_col])
            
            # Ép kiểu điểm về dạng số
            for col in df_clean.columns:
                if any(x in str(col) for x in ['ĐĐG', 'TBM', 'Điểm', 'TX', 'GK', 'CK']):
                    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            
            # TỰ ĐỘNG ẨN CÁC CỘT MÃ KHÔNG CẦN THIẾT
            cols_to_hide = [c for c in df_clean.columns if any(x in str(c).lower() for x in ['studentid', 'mã học sinh', 'stt'])]
            df_clean = df_clean.drop(columns=cols_to_hide, errors='ignore')
            
            return df_clean
            
        else:
            if hasattr(file, 'seek'):
                file.seek(0)
            return pd.read_excel(file)
            
    except Exception as e:
        raise Exception(f"{e}")


def render_analytics_module(api_key=""):
    st.markdown("""
    <style>
    div[data-testid="stAppViewBlockContainer"], .main .block-container { padding-top: 3.5rem !important; padding-bottom: 3rem !important; }
    .stSelectbox label p, .stFileUploader label p, .stTextArea label p { color: #0000FF !important; font-weight: 600 !important; font-size: 14px !important; }
    .stMarkdown p strong { color: #FF0000 !important; font-size: 15px !important; }
    .stButton>button { font-weight: bold; border-radius: 6px; }
    </style>
    """, unsafe_allow_html=True)

    col_mode, col_req = st.columns([1, 1])
    with col_mode:
        che_do = st.selectbox("🎯 Chọn Chế độ Phân tích", [
            "1. Phân tích Tổng quan Phổ điểm & Xếp loại",
            "2. Phân tích Chất lượng Câu hỏi (Item Analysis)",
            "3. Phân tích Đánh giá Năng lực / Rubric Dự án"
        ])
        file_diem = st.file_uploader("📥 Tải Bảng điểm (Hỗ trợ file xuất từ SMAS, vnEdu, Excel, CSV)", type=['xlsx', 'xls', 'csv'])
    
    with col_req:
        yeu_cau = st.text_area("Yêu cầu trọng tâm cho AI (Tùy chọn)", placeholder="Ví dụ: Chỉ ra 5 học sinh yếu nhất cần phụ đạo gấp, phân tích xem học sinh hổng kiến thức ở câu nào nhiều nhất...", height=115)

    if file_diem is not None:
        try:
            df = load_and_clean_data(file_diem)
            
            st.markdown("---")
            st.markdown("### 📊 Dashboard Thống kê Nhanh")
            
            tab_data, tab_stats = st.tabs(["1️⃣ Dữ liệu Đã làm sạch", "2️⃣ Thống kê độ phân tán"])
            
            with tab_data:
                # THIẾT LẬP CẤU HÌNH ĐỘ RỘNG CỘT (ÉP NHỎ CỘT ĐIỂM)
                col_cfg = {}
                for c in df.columns:
                    if 'họ' in str(c).lower() or 'tên' in str(c).lower():
                        # Cột tên thì để độ rộng vừa (medium) để không bị khuất chữ
                        col_cfg[c] = st.column_config.TextColumn(str(c), width="medium")
                    else:
                        # Tất cả các cột điểm, nhận xét... ép nhỏ lại (small)
                        col_cfg[c] = st.column_config.Column(str(c), width="small")
                        
                st.dataframe(df.head(15), column_config=col_cfg, use_container_width=True)
                
            with tab_stats:
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    st.write(df[numeric_cols].describe())
                else:
                    st.info("Hệ thống không tìm thấy cột số nào để thống kê.")

            if st.button("🤖 TIẾN HÀNH PHÂN TÍCH CHUYÊN SÂU", type="primary", use_container_width=True):
                data_str = df.head(150).to_csv(index=False)
                final_key = api_key if api_key else get_api_key()
                
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
Bạn là {sys_role} hàng đầu. Dưới đây là bảng điểm đã được làm sạch của học sinh (định dạng CSV):
{data_str}

Yêu cầu cụ thể của giáo viên: {yeu_cau}

Dựa vào bảng số liệu trên, hãy viết một "BÁO CÁO SƯ PHẠM" bám sát các trọng tâm sau:
{focus}

Yêu cầu trình bày:
- Dùng định dạng Markdown rõ ràng, chia mục khoa học.
- Dùng bảng biểu Markdown nếu cần so sánh.
- TUYỆT ĐỐI trung thực với số liệu, không bịa đặt tên học sinh hoặc điểm số không có trong file.
"""
                with st.spinner(f"AI đang phân tích dữ liệu SMAS và kích hoạt {che_do}..."):
                    result = run_ai_with_fallback(prompt=prompt, api_key=final_key, model_mode="flash")
                    if result.get("success"):
                        st.session_state['current_analytics'] = result.get("text")
                    else:
                        st.error(f"❌ Lỗi AI: {result.get('error')}")

        except Exception as e:
            st.error(f"❌ Lỗi xử lý file: {str(e)}")

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
