import streamlit as st

def render_module():
    st.markdown("<h2 style='color: #27AE60;'>📊 Phân hệ: Quản lý Tổ chuyên môn</h2>", unsafe_allow_html=True)
    
    # Định nghĩa các thẻ chức năng
    tabs = st.tabs([
        "Danh sách thành viên", 
        "Quản lý & Phân công chuyên môn", 
        "Hỗ trợ sinh hoạt tổ", 
        "Kế hoạch Tổ", 
        "Kế hoạch cá nhân", 
        "Thành tích & Thi đua"
    ])
    
    # 1. Danh sách thành viên
    with tabs[0]:
        st.subheader("👥 Danh sách thành viên tổ")
        st.write("Quản lý thông tin, trình độ và chuyên môn của giáo viên trong tổ.")
        # Thêm code hiển thị bảng/danh sách tại đây
        
    # 2. Quản lý & Phân công chuyên môn
    with tabs[1]:
        st.subheader("📝 Quản lý & Phân công chuyên môn")
        st.write("Phân công giảng dạy, kiêm nhiệm và các nhiệm vụ chuyên môn khác.")
        
    # 3. Hỗ trợ sinh hoạt tổ chuyên môn
    with tabs[2]:
        st.subheader("💡 Hỗ trợ sinh hoạt tổ chuyên môn")
        st.write("AI gợi ý chủ đề sinh hoạt, hỗ trợ biên bản và tổng hợp ý kiến.")
        
    # 4. Kế hoạch Tổ
    with tabs[3]:
        st.subheader("🗓️ Kế hoạch Tổ chuyên môn")
        st.write("Xây dựng, duyệt và lưu trữ kế hoạch hoạt động của tổ theo tháng/kỳ/năm.")
        
    # 5. Kế hoạch cá nhân
    with tabs[4]:
        st.subheader("👤 Kế hoạch cá nhân")
        st.write("Theo dõi, đánh giá kế hoạch cá nhân của từng giáo viên trong tổ.")
        
    # 6. Thành tích và Thi đua
    with tabs[5]:
        st.subheader("🏆 Thành tích & Thi đua")
        st.write("Tổng hợp danh hiệu, thi đua, khen thưởng của tổ và cá nhân.")
