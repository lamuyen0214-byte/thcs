import streamlit as st
import time

def render_live_quiz_module():
    # Tinh chỉnh CSS
    st.markdown("""
    <style>
    .stButton>button { font-weight: bold; border-radius: 6px; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

    # 1. KHU VỰC CẤU HÌNH LINK
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        image_url = st.text_input("🖼️ Dán link ảnh bìa:", placeholder="https://...")
    with col_input2:
        live_link = st.text_input("🔗 Dán link Quiz Live (Kahoot/Quizizz):", placeholder="https://...")

    # Hiển thị ảnh nếu có link
    if image_url:
        try:
            st.image(image_url, use_container_width=True)
        except:
            st.error("Link ảnh không hợp lệ, thầy kiểm tra lại nhé!")

    # 2. KHỞI TẠO SESSSION
    if 'quiz_started' not in st.session_state:
        st.session_state['quiz_started'] = False

    st.write("---")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🛠 Cấu hình Quiz")
        ten_quiz = st.text_input("Tên phiên trắc nghiệm", "Kiểm tra 15' KHTN")
        
        # Nút Mở Link Live
        if live_link:
            st.link_button("🚀 MỞ LINK QUIZ ĐÃ DÁN", url=live_link, use_container_width=True)
        
        if not st.session_state['quiz_started']:
            if st.button("▶️ BẮT ĐẦU PHÁT SÓNG TRONG APP", type="primary", use_container_width=True):
                st.session_state['quiz_started'] = True
                st.rerun()
        else:
            if st.button("⏹️ KẾT THÚC PHIÊN", type="secondary", use_container_width=True):
                st.session_state['quiz_started'] = False
                st.rerun()

    with col2:
        if st.session_state['quiz_started']:
            st.success(f"✅ Phiên '{ten_quiz}' đang hoạt động!")
            
            # Mô phỏng dashboard
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)
            
            col_a, col_b = st.columns(2)
            col_a.metric("Số HS tham gia", "0")
            col_b.metric("Câu hỏi hiện tại", "0/5")
            
            st.markdown("### 📊 Kết quả trực tiếp (Live Feed)")
            st.write("Đang chờ phản hồi từ học sinh...")
        else:
            st.info("Hệ thống đang ở chế độ chờ. Hãy dán link và bắt đầu phiên Quiz.")

    st.caption("💡 Lưu ý: Các link Quiz (Kahoot, Quizizz) sẽ được mở ở tab mới khi thầy nhấn nút.")
