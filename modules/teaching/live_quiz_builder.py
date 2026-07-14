import streamlit as st
import time
import os  # <--- Dòng này là chìa khóa để sửa lỗi!

def render_live_quiz_module():
    # Tinh chỉnh CSS
    st.markdown("""
    <style>
    .stButton>button { font-weight: bold; border-radius: 6px; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("⚡ Hệ thống Trắc nghiệm Tương tác Trực tiếp")
    
    # --- PHẦN HIỂN THỊ ẢNH (ĐÃ FIX LỖI ĐƯỜNG DẪN) ---
    image_path = os.path.join("assets", "unnamed.jpg")
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.warning("Chưa tìm thấy ảnh 'unnamed.jpg' trong thư mục 'assets'.")

    # Khởi tạo session state cho quiz
    if 'quiz_started' not in st.session_state:
        st.session_state['quiz_started'] = False
        st.session_state['current_q'] = 0

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🛠 Cấu hình Quiz")
        ten_quiz = st.text_input("Tên phiên trắc nghiệm", "Kiểm tra 15' KHTN")
        so_cau = st.number_input("Số câu hỏi", min_value=1, max_value=20, value=5)
        thoi_gian = st.number_input("Thời gian mỗi câu (giây)", min_value=10, max_value=60, value=30)
        
        if not st.session_state['quiz_started']:
            if st.button("🚀 BẮT ĐẦU PHÁT SÓNG (LIVE)", type="primary", use_container_width=True):
                st.session_state['quiz_started'] = True
                st.rerun()
        else:
            if st.button("⏹️ KẾT THÚC PHIÊN", type="secondary", use_container_width=True):
                st.session_state['quiz_started'] = False
                st.rerun()

    with col2:
        if st.session_state['quiz_started']:
            st.success(f"✅ Phiên '{ten_quiz}' đang hoạt động!")
            st.info("Học sinh đang kết nối vào hệ thống...")
            
            # Mô phỏng dashboard thời gian thực
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)
            
            col_a, col_b = st.columns(2)
            col_a.metric("Số HS tham gia", "0")
            col_b.metric("Câu hỏi hiện tại", f"0/{so_cau}")
            
            st.write("---")
            st.markdown("### 📊 Kết quả trực tiếp (Live Feed)")
            st.write("Đang chờ phản hồi từ học sinh...")
        else:
            st.warning("Hệ thống đang ở chế độ chờ. Hãy nhấn nút Bắt đầu để kích hoạt phiên Quiz.")

    st.markdown("---")
    st.caption("💡 Lưu ý: Tính năng này giả lập môi trường server local.")
