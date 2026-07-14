import streamlit as st
from modules.teaching.rag_engine import process_rag_engine

def render_module():
    st.markdown("## 🌱 Hỗ trợ Giảng dạy")
    
    tabs = st.tabs([
        "Hỏi-Đáp (RAG)", "Trò chơi", "Chấm bài", "Học liệu", "Mô phỏng", 
        "Phân tích", "Ngân hàng đề", "Sinh Video", "Tương tác", "Cá nhân hóa",
        "📷 Camera chấm bài", "⚡ Trắc nghiệm Live"
    ])
    
    # --- THẺ 1: HỎI ĐÁP (RAG) ---
    with tabs[0]:
        st.markdown("### 🤖 AI Hỏi - Đáp Theo Tài Liệu (RAG)")
        st.markdown("Hệ thống tự động phân tách tài liệu và truy xuất dữ liệu.")
        
        st.markdown("#### 📥 Bước 1: Chọn nguồn tài liệu giảng dạy")
        
        hinh_thuc = st.radio(
            "Hình thức cung cấp học liệu:",
            ["Tài liệu tải lên (PDF, DOCX, Ảnh)", "Đường dẫn Website"],
            horizontal=True
        )
        
        uploaded_file = None
        hinh_thuc_url = None
        
        if hinh_thuc == "Tài liệu tải lên (PDF, DOCX, Ảnh)":
            st.write("Tải lên tài liệu của thầy/cô:")
            uploaded_file = st.file_uploader("Upload", type=['pdf', 'docx', 'png', 'jpg'], label_visibility="collapsed")
        else:
            hinh_thuc_url = st.text_input("Nhập đường dẫn Website (URL):")
            
        process_rag_engine(uploaded_file, hinh_thuc_url)

    # --- THẺ 2: TRÒ CHƠI ---
    with tabs[1]:
        st.subheader("🎮 Trò chơi")
        st.info("⏳ Đang chờ kết nối module trò chơi...")

    # --- THẺ 3: CHẤM BÀI ---
    with tabs[2]:
        from modules.teaching.grading_engine import render_grading_module
        render_grading_module()    
       
    # --- CÁC THẺ 4-10: GIAO DIỆN CHỜ ---
    for i in range(3, 10):
        with tabs[i]:
            st.info("⏳ Giao diện đang được cập nhật...")

    # --- THẺ 11: CAMERA CHẤM BÀI (AI VISION) ---
    with tabs[10]:
        st.subheader("📷 Camera chấm bài bằng AI Vision")
        st.info("Sử dụng Camera để quét và chấm điểm tự động bài kiểm tra.")
        # Thầy sẽ tích hợp module xử lý ảnh tại đây
        st.warning("🚧 Đang tích hợp thuật toán Computer Vision...")

    # --- THẺ 12: TRẮC NGHIỆM LIVE ---
    with tabs[11]:
        st.subheader("⚡ Trắc nghiệm tương tác trực tiếp")
        st.info("Tổ chức các phiên hỏi đáp, khảo sát thời gian thực cho học sinh.")
        # Thầy sẽ tích hợp module xử lý real-time tại đây
        st.warning("🚧 Đang tích hợp hệ thống thời gian thực...")
