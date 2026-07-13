import streamlit as st
import sys
import os

# Cấu hình đường dẫn để import được từ thư mục cha/ngang hàng
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import logic xử lý từ tầng Engine (Service Layer)
# Giả định thầy đã chuyển logic vào file quiz_service.py hoặc tương tự trong ai_engine
try:
    from ai_engine.layer_5_output.quiz_generator import generate_quiz_logic 
except ImportError:
    st.error("❌ Chưa tìm thấy core logic trong ai_engine. Hãy kiểm tra lại đường dẫn import.")

def render_quiz_generator():
    st.subheader("🎯 Trình Tạo Đề Kiểm Tra Tự Động")
    
    # 1. UI: Giao diện người dùng
    uploaded_file = st.file_uploader("Tải tài liệu tham khảo (PDF, DOCX, TXT):", type=['pdf', 'docx', 'txt'])
    text_content = st.text_area("Nội dung bài giảng / Yêu cầu cụ thể:", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        num_mcq = st.number_input("Số câu trắc nghiệm:", min_value=0, value=20)
        num_essay = st.number_input("Số câu tự luận:", min_value=0, value=5)
    with col2:
        use_source = st.checkbox("Tuyệt đối bám sát tài liệu", value=True)
        include_digital = st.checkbox("Tích hợp Năng lực số", value=True)
    
    # 2. Controller: Điều khiển luồng xử lý
    if st.button("🚀 Tạo đề ngay", type="primary", use_container_width=True):
        if not uploaded_file and not text_content:
            st.warning("⚠️ Chưa có dữ liệu đầu vào.")
            return

        with st.spinner("AI đang xử lý..."):
            try:
                # Gọi hàm từ Engine (Service Layer)
                result = generate_quiz_logic(
                    uploaded_file=uploaded_file,
                    text_content=text_content,
                    num_mcq=num_mcq,
                    num_essay=num_essay,
                    use_source=use_source,
                    include_digital=include_digital
                )
                
                if result:
                    st.session_state.current_quiz = result
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Lỗi hệ thống: {str(e)}")

    # 3. View: Hiển thị kết quả
    if "current_quiz" in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state.current_quiz)
        # Nút tải file ở đây...
