import streamlit as st
from modules.teaching.rag_engine import process_rag_engine
from modules.teaching.game_builder import render_game_module
from modules.teaching.hoc_lieu_builder import render_hoc_lieu_module
from modules.teaching.simulation_builder import render_simulation_module
from modules.teaching.analytics_builder import render_analytics_module
from modules.teaching.bank_builder import render_bank_module
from modules.teaching.video_builder import render_video_module
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
        hinh_thuc = st.radio("Hình thức cung cấp học liệu:", ["Tài liệu tải lên (PDF, DOCX, Ảnh)", "Đường dẫn Website"], horizontal=True)
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
        st.subheader("🎮 Trò chơi học tập (Gamification)")
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

    # --- THẺ 6: PHÂN TÍCH DỮ LIỆU ---
    with tabs[5]:
        st.subheader("📊 Phân tích Kết quả Học tập")
        try:
            render_analytics_module()
        except Exception as e:
            st.error(f"Lỗi tải module Phân tích: {e}. (Gợi ý: Thầy kiểm tra đã cài thư viện pandas và openpyxl chưa nhé)")

    # --- THẺ 7: NGÂN HÀNG ĐỀ ---
    with tabs[6]:
        st.subheader("📚 Ngân hàng đề & Trộn đề thông minh")
        try:
            render_bank_module()
        except Exception as e:
            st.error(f"Lỗi tải module Ngân hàng đề: {e}")

    # --- THẺ 8: SINH VIDEO BÀI GIẢNG ---
    with tabs[7]:
        st.subheader("🎥 AI Sinh Kịch bản & Audio Video Bài giảng")
        try:
            render_video_module()
        except Exception as e:
            st.error(f"Lỗi tải module Sinh Video: {e}")

    # --- CÁC THẺ 9-10: GIAO DIỆN CHỜ (Sửa dải số thành từ 8 đến 9) ---
    for i in range(8, 10):
        with tabs[i]:
            st.info("⏳ Giao diện đang được cập nhật...")
