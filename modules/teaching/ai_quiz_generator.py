import streamlit as st
import google.generativeai as genai
from io import BytesIO

def get_stable_model():
    """Tự động lọc và lấy model ổn định nhất"""
    priority_list = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    try:
        available_models = {m.name: m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods}
        for name in priority_list:
            if name in available_models: return genai.GenerativeModel(name)
            if f"models/{name}" in available_models: return genai.GenerativeModel(f"models/{name}")
        return genai.GenerativeModel(list(available_models.keys())[0])
    except:
        return None

def render_quiz_generator():
    st.subheader("🎯 Trình Tạo Đề Kiểm Tra Tự Động")
    
    text_content = st.text_area("Nhập nội dung bài giảng để AI soạn đề:", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.number_input("Số lượng câu hỏi:", min_value=1, max_value=20, value=5)
    with col2:
        quiz_type = st.selectbox("Dạng bài:", ["Trắc nghiệm", "Tự luận", "Trắc nghiệm & Tự luận"])
    
    # Nút Tạo đề
    if st.button("🚀 Tạo đề kiểm tra ngay"):
        if not text_content:
            st.warning("Vui lòng nhập nội dung bài giảng trước khi tạo đề.")
        else:
            with st.spinner("Đang soạn đề (Đang kết nối Model ổn định nhất)..."):
                model = get_stable_model()
                if model:
                    prompt = f"Soạn {num_questions} câu hỏi {quiz_type} dựa trên nội dung bài giảng: {text_content}. Trình bày rõ ràng phần CÂU HỎI và phần ĐÁP ÁN ở cuối."
                    try:
                        response = model.generate_content(prompt)
                        st.session_state.current_quiz = response.text
                        st.rerun() # Tự làm mới để hiện kết quả và nút tải
                    except Exception as e:
                        st.error(f"Lỗi tạo đề: {e}")

    # Hiển thị kết quả và Nút xuất file
    if "current_quiz" in st.session_state:
        st.markdown("---")
        st.markdown("### 📝 Kết quả đề kiểm tra:")
        st.text_area("Đề bài (Thầy có thể copy):", st.session_state.current_quiz, height=300)
        
        # Nút xuất file (Nút Tải về)
        st.download_button(
            label="📥 Tải bộ đề về máy (.txt)",
            data=st.session_state.current_quiz,
            file_name="De_kiem_tra_AI.txt",
            mime="text/plain"
        )
