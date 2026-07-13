import streamlit as st
import google.generativeai as genai
from PIL import Image

def render_grading_module():
    st.subheader("📝 Chấm Trắc Nghiệm Bằng AI")
    
    # 1. Nhập đáp án chuẩn
    st.markdown("#### Bước 1: Thiết lập đáp án")
    dap_an = st.text_input("Nhập đáp án chuẩn (Ví dụ: 1A, 2B, 3C...)", placeholder="1A, 2B, 3C, 4D")
    
    # 2. Upload ảnh phiếu bài làm
    st.markdown("#### Bước 2: Tải lên phiếu bài làm")
    uploaded_file = st.file_uploader("Chọn ảnh phiếu làm bài của học sinh", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file and dap_an:
        if st.button("🚀 Bắt đầu chấm bài"):
            with st.spinner("AI đang phân tích ảnh..."):
                try:
                    # Cấu hình AI
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    img = Image.open(uploaded_file)
                    
                    # Prompt cho AI
                    prompt = f"""
                    Bạn là một giáo viên tận tâm. Hãy phân tích ảnh phiếu trắc nghiệm này.
                    Đáp án chuẩn là: {dap_an}.
                    Hãy đối chiếu các lựa chọn học sinh đã tô trên ảnh với đáp án chuẩn.
                    Trả về kết quả dưới dạng:
                    - Số câu đúng/tổng số câu.
                    - Điểm số (tính theo thang 10).
                    - Nhận xét ngắn gọn cho học sinh.
                    """
                    
                    response = model.generate_content([prompt, img])
                    st.markdown("### 📋 Kết quả chấm:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"Có lỗi xảy ra: {e}")
