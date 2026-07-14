import streamlit as st
import google.generativeai as genai
from PIL import Image
from ai_engine.ai_config import get_api_key

def render_camera_module(api_key=""):
    # Tinh chỉnh CSS
    st.markdown("""
    <style>
    div[data-testid="stAppViewBlockContainer"], .main .block-container { padding-top: 3.5rem !important; padding-bottom: 3rem !important; }
    .stSelectbox label p, .stRadio label p, .stTextArea label p { color: #0000FF !important; font-weight: 600 !important; font-size: 14px !important; }
    .stMarkdown p strong { color: #FF0000 !important; font-size: 15px !important; }
    .stButton>button { font-weight: bold; border-radius: 6px; }
    </style>
    """, unsafe_allow_html=True)

    # 1. GIAO DIỆN NHẬP LIỆU: CAMERA VÀ ĐÁP ÁN
    col_img, col_key = st.columns([1, 1])
    
    with col_img:
        st.markdown("### 📷 Nguồn ảnh Bài làm")
        input_method = st.radio("Chọn phương thức tải ảnh:", ["Chụp trực tiếp từ Camera", "Tải ảnh từ máy tính"], horizontal=True)
        
        image_data = None
        if input_method == "Chụp trực tiếp từ Camera":
            img_file_buffer = st.camera_input("Đưa bài làm của học sinh vào khung hình", key="camera_input")
            if img_file_buffer is not None:
                image_data = Image.open(img_file_buffer)
        else:
            uploaded_file = st.file_uploader("Tải lên ảnh bài kiểm tra (JPG, PNG)", type=['jpg', 'jpeg', 'png'])
            if uploaded_file is not None:
                image_data = Image.open(uploaded_file)
                st.image(image_data, caption="📸 Ảnh đã tải lên", use_container_width=True)

    with col_key:
        st.markdown("### 📝 Tiêu chí & Đáp án")
        loai_bai = st.selectbox("Phân loại bài kiểm tra", [
            "Trắc nghiệm khách quan (MCQ)", 
            "Tự luận ngắn / Điền khuyết", 
            "Toán học / Tự nhiên (Cần kiểm tra bước giải)", 
            "Ngữ văn / Viết đoạn văn"
        ])
        
        dap_an = st.text_area("Nhập Đáp án chuẩn hoặc Tiêu chí chấm (Rubric):", 
                              placeholder="Ví dụ:\n- 1A, 2B, 3C...\n- Hoặc: Điểm tối đa nếu HS nêu được 3 ý: Mở bài (1đ), Phân tích (2đ), Kết luận (1đ).", 
                              height=200)

    # 2. XỬ LÝ ẢNH BẰNG AI VISION
    if st.button("🤖 AI KÍCH HOẠT QUÉT & CHẤM ĐIỂM", type="primary", use_container_width=True):
        if image_data is None:
            st.warning("⚠️ Thầy/Cô vui lòng chụp ảnh hoặc tải ảnh bài làm lên trước nhé!")
            st.stop()
        if not dap_an.strip():
            st.warning("⚠️ Thầy/Cô vui lòng cung cấp đáp án hoặc tiêu chí để AI có thước đo chấm điểm!")
            st.stop()
            
        final_key = api_key if api_key else get_api_key()
        try:
            genai.configure(api_key=final_key)
            model = genai.GenerativeModel('gemini-1.5-flash') # Model mạnh mẽ và tối ưu nhất cho Vision
            
            prompt = f"""
            Bạn là một Giám khảo chấm thi nghiêm khắc, công tâm và có chuyên môn sư phạm xuất sắc.
            Dưới đây là hình ảnh bài làm của học sinh.
            Loại hình kiểm tra: {loai_bai}.
            Thước đo / Đáp án chuẩn của giáo viên: {dap_an}
            
            Nhiệm vụ của bạn:
            1. Đọc và nhận diện chữ viết tay/đáp án khoanh của học sinh trong ảnh một cách cẩn thận.
            2. Đối chiếu tỉ mỉ với 'Đáp án chuẩn' đã cung cấp.
            3. Trình bày chi tiết phân tích: Học sinh trả lời đúng ở đâu, sai ở đâu. (Lưu ý: Nếu là bài Toán/Lý/Hóa, hãy chỉ điểm chính xác lỗi sai ở bước biến đổi nào).
            4. Tổng hợp ĐIỂM SỐ CUỐI CÙNG (Quy ra thang điểm 10).
            5. Viết 2 câu LỜI PHÊ (nhận xét) mang tính xây dựng để giáo viên có thể ghi thẳng vào bài của học sinh.
            
            Trình bày bằng định dạng Markdown rõ ràng, in đậm các điểm lỗi sai để giáo viên dễ nhìn.
            """
            
            with st.spinner("🔍 AI đang quét ảnh, nhận diện chữ viết và đối chiếu đáp án..."):
                response = model.generate_content([prompt, image_data])
                st.session_state['current_vision_grading'] = response.text
                
        except Exception as e:
            st.error(f"❌ Có lỗi xảy ra trong quá trình quét ảnh: {str(e)}")

    # 3. HIỂN THỊ KẾT QUẢ CHẤM ĐIỂM
    if 'current_vision_grading' in st.session_state:
        st.markdown("---")
        with st.expander("✅ KẾT QUẢ CHẤM BÀI CHI TIẾT", expanded=True):
            st.markdown(st.session_state['current_vision_grading'])
