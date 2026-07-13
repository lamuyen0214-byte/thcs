import streamlit as st
import google.generativeai as genai
from io import BytesIO

def get_stable_model():
    """Hàm tự động lọc và lấy model ổn định nhất từ danh sách khả dụng"""
    # Danh sách ưu tiên các model ổn định, thông dụng
    priority_list = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-flash-latest"]
    
    try:
        available_models = {m.name: m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods}
        
        # Kiểm tra nếu model ưu tiên tồn tại trong danh sách của thầy
        for model_name in priority_list:
            # Kiểm tra cả dạng 'gemini-xxx' và 'models/gemini-xxx'
            if model_name in available_models:
                return genai.GenerativeModel(model_name)
            elif f"models/{model_name}" in available_models:
                return genai.GenerativeModel(f"models/{model_name}")
                
        # Nếu không có trong danh sách ưu tiên, lấy cái đầu tiên tìm thấy
        first_model = list(available_models.keys())[0]
        return genai.GenerativeModel(first_model)
    except Exception as e:
        st.error("Không thể kết nối API. Vui lòng kiểm tra lại Key.")
        return None

def render_quiz_generator():
    st.subheader("🎯 Trình Tạo Đề Kiểm Tra Tự Động")
    
    text_content = st.text_area("Nhập nội dung bài giảng:", height=200)
    
    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.number_input("Số lượng câu hỏi:", min_value=1, value=5)
    with col2:
        quiz_type = st.selectbox("Dạng bài:", ["Trắc nghiệm", "Tự luận"])
    
    if st.button("🚀 Tạo đề kiểm tra"):
        if not text_content:
            st.warning("Vui lòng nhập nội dung.")
        else:
            with st.spinner("Đang soạn đề (Đang kết nối Model ổn định nhất)..."):
                model = get_stable_model()
                if model:
                    prompt = f"Tạo {num_questions} câu hỏi {quiz_type} dựa trên nội dung: {text_content}. Trả về dạng CÂU HỎI và ĐÁP ÁN."
                    try:
                        response = model.generate_content(prompt)
                        st.session_state.current_quiz = response.text
                        st.success("Tạo đề thành công!")
                    except Exception as e:
                        st.error(f"Lỗi tạo đề: {e}. Vui lòng thử lại sau vài giây.")

    if "current_quiz" in st.session_state:
        st.text_area("Kết quả:", st.session_state.current_quiz, height=300)
