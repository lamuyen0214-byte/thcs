import streamlit as st

def render_module():
    st.markdown("<h2 style='color: #2E86C1;'>🌱 Hỗ trợ Giảng dạy</h2>", unsafe_allow_html=True)
    
    # Tạo danh sách các tab tương ứng với menu của thầy
    tab_names = [
        "Hỏi-Đáp (RAG)", "Trò chơi", "Chấm bài", "Học liệu", 
        "Mô phỏng", "Phân tích", "Ngân hàng đề", "Sinh Video", 
        "Tương tác", "Cá nhân hóa"
    ]
    
    # Tạo tabs
    tabs = st.tabs(tab_names)
    
    # --- PHẦN NỘI DUNG CHO TỪNG TAB ---
    
    # Tab 1: Hỏi-Đáp (RAG)
    with tabs[0]:
        st.markdown("### 🤖 AI Hỏi - Đáp Theo Tài Liệu (RAG)")
        st.write("Hệ thống tự động phân tách tài liệu, nhúng vector và truy xuất dữ liệu có kèm trích dẫn nguồn.")
        
        st.markdown("#### 📥 Bước 1: Chọn nguồn tài liệu giảng dạy")
        nguon_cap = st.radio("Hình thức cung cấp học liệu:", ["Tài liệu tải lên (PDF, DOCX, Ảnh)", "Đường dẫn Website"], horizontal=True)
        
        if nguon_cap == "Tài liệu tải lên (PDF, DOCX, Ảnh)":
            uploaded_file = st.file_uploader("Tải lên tài liệu của thầy/cô (PDF, DOCX, PNG, JPG):", type=['pdf', 'docx', 'png', 'jpg'])
            if uploaded_file:
                st.success(f"Đã tải lên: {uploaded_file.name}")
        
        st.markdown("#### 💬 Bước 2: Tương tác và truy vấn với AI")
        st.info("💡 Vui lòng hoàn thành **Bước 1** (Tải tài liệu và bấm phân tích) để kích hoạt Trợ lý AI.")

    # Tab 2: Trò chơi
    with tabs[1]:
        st.write("### 🎮 Công cụ tạo trò chơi học tập")
        st.write("Tính năng đang được phát triển...")

    # Các tab khác thầy làm tương tự bằng cách sử dụng tabs[2], tabs[3]...
    with tabs[2]:
        st.write("### ✍️ Công cụ chấm bài tự động")

    with tabs[3]:
        st.write("### 📚 Kho học liệu số")

# Lưu ý: Các tab còn lại thầy có thể thêm tương tự vào danh sách tabs[4] đến tabs[9]
