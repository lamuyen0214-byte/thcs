import streamlit as st
import google.generativeai as genai
from io import BytesIO

def generate_quiz(text_content, num_questions, quiz_type):
    """Hàm xử lý chính gọi AI để tạo đề"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Bạn là một giáo viên THCS chuyên nghiệp. Hãy dựa vào nội dung bài giảng dưới đây để tạo một đề kiểm tra.
    Nội dung bài giảng: {text_content}
    
    Yêu cầu:
    - Tạo {num_questions} câu hỏi dạng {quiz_type}.
    - Chỉ trả về nội dung gồm: Bộ câu hỏi và Đáp án.
    - Không giải thích dài dòng.
    
    Định dạng:
    CÂU HỎI:
    1. ...
    2. ...
    
    ĐÁP ÁN:
    1. ...
    2. ...
    """
    
    response = model.generate_content(prompt)
    return response.text

def render_quiz_generator():
    st.subheader("🎯 Trình Tạo Đề Kiểm Tra Tự Động")
    
    # 1. Nhập liệu
    text_content = st.text_area("Nhập nội dung bài giảng/văn bản cần tạo đề:", height=200)
    
    # 2. Cấu hình đề
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.number_input("Số lượng câu hỏi:", min_value=1, max_value=20, value=5)
    with col2:
        quiz_type = st.selectbox("Dạng bài:", ["Trắc nghiệm", "Tự luận", "Trắc nghiệm & Tự luận"])
    
    # 3. Xử lý
    if st.button("🚀 Tạo đề kiểm tra ngay"):
        if not text_content:
            st.warning("Vui lòng nhập nội dung bài giảng.")
        else:
            with st.spinner("AI đang soạn đề cho thầy..."):
                try:
                    result = generate_quiz(text_content, num_questions, quiz_type)
                    st.session_state.current_quiz = result
                except Exception as e:
                    st.error(f"Lỗi tạo đề: {e}")

    # 4. Hiển thị & Xuất kết quả
    if "current_quiz" in st.session_state:
        st.markdown("---")
        st.markdown("### 📝 Kết quả đề kiểm tra:")
        st.text_area("Đề bài (Thầy có thể copy):", st.session_state.current_quiz, height=400)
        
        # Nút tải xuống
        st.download_button(
            label="📥 Tải bộ đề về máy (.txt)",
            data=st.session_state.current_quiz,
            file_name="De_kiem_tra.txt",
            mime="text/plain"
        )
