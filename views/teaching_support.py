import streamlit as st

# Tạm thời khóa dòng import này lại để chờ Streamlit Cloud cài thư viện LangChain
# from modules.rag_engine import process_rag_engine

def render_module():
    st.markdown("## 🌱 Hỗ trợ Giảng dạy")
    
    # Khôi phục đúng 10 thẻ chức năng theo thiết kế của thầy
    tabs = st.tabs([
        "Hỏi-Đáp (RAG)", 
        "Trò chơi", 
        "Chấm bài", 
        "Học liệu", 
        "Mô phỏng", 
        "Phân tích", 
        "Ngân hàng đề", 
        "Sinh Video", 
        "Tương tác", 
        "Cá nhân hóa"
    ])
    
    # --- THẺ 1: HỎI ĐÁP (RAG) ---
    with tabs[0]:
        st.markdown("### 🤖 AI Hỏi - Đáp Theo Tài Liệu (RAG)")
        st.markdown("Hệ thống tự động phân tách tài liệu, nhúng vector và truy xuất dữ liệu có kèm trích dẫn nguồn.")
        
        st.write("")
        st.markdown("#### 📥 Bước 1: Chọn nguồn tài liệu giảng dạy")
        
        # Radio button chọn hình thức
        hinh_thuc = st.radio(
            "Hình thức cung cấp học liệu:",
            ["Tài liệu tải lên (PDF, DOCX, Ảnh)", "Đường dẫn Website"],
            horizontal=True
        )
        
        # Khung tải tài liệu
        if hinh_thuc == "Tài liệu tải lên (PDF, DOCX, Ảnh)":
            st.write("Tải lên tài liệu của thầy/cô (PDF, DOCX, PNG, JPG):")
            uploaded_file = st.file_uploader("", type=['pdf', 'docx', 'png', 'jpg'], label_visibility="collapsed")
        else:
            st.text_input("Nhập đường dẫn Website (URL):")
            
        st.markdown("---")
        
        # Phần truy vấn AI
        st.markdown("#### 💬 Bước 2: Tương tác và truy vấn với AI")
        st.info("💡 Vui lòng hoàn thành Bước 1 (Tải tài liệu và bấm phân tích) để kích hoạt Trợ lý AI.")

    # --- CÁC THẺ CÒN LẠI (Chờ tích hợp) ---
    with tabs[1]:
        st.subheader("🎮 Trò chơi")
        st.info("⏳ Đang chờ kết nối module trò chơi...")
        
    with tabs[2]:
        st.subheader("📝 Chấm bài")
        st.info("⏳ Đang chờ kết nối module chấm bài tự động...")
        
    with tabs[3]:
        st.subheader("📚 Học liệu")
        st.info("⏳ Giao diện đang được cập nhật...")
        
    with tabs[4]:
        st.subheader("🔬 Mô phỏng")
        st.info("⏳ Giao diện đang được cập nhật...")
        
    with tabs[5]:
        st.subheader("📊 Phân tích")
        st.info("⏳ Giao diện đang được cập nhật...")
        
    with tabs[6]:
        st.subheader("📑 Ngân hàng đề")
        st.info("⏳ Giao diện đang được cập nhật...")
        
    with tabs[7]:
        st.subheader("🎬 Sinh Video")
        st.info("⏳ Giao diện đang được cập nhật...")
        
    with tabs[8]:
        st.subheader("🤝 Tương tác")
        st.info("⏳ Giao diện đang được cập nhật...")
        
    with tabs[9]:
        st.subheader("👤 Cá nhân hóa")
        st.info("⏳ Giao diện đang được cập nhật...")
