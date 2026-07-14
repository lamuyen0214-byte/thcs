import streamlit as st
from modules.teaching.rag_engine import process_rag_engine
from modules.teaching.game_builder import render_game_module
from modules.teaching.hoc_lieu_builder import render_hoc_lieu_module
from modules.teaching.simulation_builder import render_simulation_module
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

    # --- THẺ 2: TRÒ CHƠI (ĐÃ ĐƯỢC KẾT NỐI LÊN GIAO DIỆN) ---
    with tabs[1]:
        st.subheader("🎮 Trò chơi học tập (Gamification)")
        # 2. GỌI HÀM GIAO DIỆN TRÒ CHƠI
        render_game_module() 

    # --- THẺ 3: CHẤM BÀI ---
    with tabs[2]:
        from modules.teaching.grading_engine import render_grading_module
        render_grading_module()    
    # --- THẺ 4: HỌC LIỆU ---
    with tabs[3]:
        st.subheader("📚 Kho Học liệu (Biên soạn tự động)")
        try:
            render_hoc_lieu_module()
        except Exception as e:
            st.error(f"Lỗi tải module Học liệu: {e}")
    # --- THẺ 5: MÔ PHỎNG TRỰC QUAN ---
    with tabs[4]:
        st.subheader("🔬 Mô phỏng Tương tác & Khám phá")
        try:
            render_simulation_module()
        except Exception as e:
            st.error(f"Lỗi tải module Mô phỏng: {e}")

    # --- CÁC THẺ 6-10: GIAO DIỆN CHỜ (Sửa dải số thành từ 5 đến 9) ---
    for i in range(5, 10):
        with tabs[i]:
            st.info("⏳ Giao diện đang được cập nhật...")
    # --- CÁC THẺ 5-10: GIAO DIỆN CHỜ (Đã sửa dải số từ 4 đến 9) ---
    for i in range(4, 10):
        with tabs[i]:
            st.info("⏳ Giao diện đang được cập nhật...")   
    # --- CÁC THẺ 4-10: GIAO DIỆN CHỜ ---
    for i in range(3, 10):
        with tabs[i]:
            st.info("⏳ Giao diện đang được cập nhật...")

    # --- THẺ 11: CAMERA CHẤM BÀI (AI VISION) ---
    with tabs[10]:
        st.subheader("📷 Camera chấm bài bằng AI Vision")
        st.info("Sử dụng Camera để quét và chấm điểm tự động bài kiểm tra.")
        st.warning("🚧 Đang tích hợp thuật toán Computer Vision...")

    # --- THẺ 12: TRẮC NGHIỆM LIVE ---
    with tabs[11]:
        st.subheader("⚡ Trắc nghiệm tương tác trực tiếp")
        st.info("Tổ chức các phiên hỏi đáp, khảo sát thời gian thực cho học sinh.")
        st.warning("🚧 Đang tích hợp hệ thống thời gian thực...")
