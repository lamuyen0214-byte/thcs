import streamlit as st
import pandas as pd
from datetime import datetime

def render_org_management():
    # Khởi tạo data mẫu nếu chưa có
    if 'team_members' not in st.session_state:
        st.session_state['team_members'] = pd.DataFrame(columns=["Họ tên", "Chức vụ", "Môn dạy", "Ghi chú"])

    tabs = st.tabs([
        "👥 Danh sách thành viên", 
        "📋 Phân công chuyên môn", 
        "📝 Hỗ trợ sinh hoạt tổ", 
        "📅 Kế hoạch & Văn bản", 
        "🎯 Thi đua & Thành tích"
    ])

    # TAB 1: DANH SÁCH THÀNH VIÊN
    with tabs[0]:
        st.subheader("Quản lý thông tin giáo viên")
        with st.form("add_member"):
            col1, col2 = st.columns(2)
            name = col1.text_input("Họ và tên")
            role = col2.selectbox("Chức vụ", ["Tổ trưởng", "Tổ phó", "Giáo viên", "Thư ký"])
            subject = col1.text_input("Môn dạy")
            note = col2.text_input("Ghi chú/Điện thoại")
            if st.form_submit_button("➕ Thêm thành viên"):
                new_data = {"Họ tên": name, "Chức vụ": role, "Môn dạy": subject, "Ghi chú": note}
                st.session_state['team_members'] = pd.concat([st.session_state['team_members'], pd.DataFrame([new_data])], ignore_index=True)
                st.rerun()
        
        st.table(st.session_state['team_members'])

    # TAB 2: PHÂN CÔNG CHUYÊN MÔN
    with tabs[1]:
        st.info("Bảng phân công giảng dạy và nhiệm vụ kiêm nhiệm trong tổ.")
        # Dùng st.data_editor để chỉnh sửa trực tiếp
        st.data_editor(st.session_state['team_members'], use_container_width=True)

    # TAB 3: HỖ TRỢ SINH HOẠT TỔ (AI GỢI Ý BIÊN BẢN)
    with tabs[2]:
        st.subheader("Tạo biên bản họp nhanh")
        noidung = st.text_area("Nội dung chính cuộc họp", placeholder="Ví dụ: Rút kinh nghiệm chuyên đề tháng 4, triển khai thi học kỳ...")
        if st.button("✨ AI Soạn thảo biên bản"):
            st.success("AI đã tạo dự thảo biên bản dựa trên nội dung thầy cung cấp...")
            st.text("DỰ THẢO BIÊN BẢN SINH HOẠT TỔ:\n1. Thời gian: ...\n2. Thành phần: ...\n3. Nội dung: " + noidung)

    # TAB 4: KẾ HOẠCH
    with tabs[3]:
        st.subheader("Kho lưu trữ văn bản")
        uploaded_file = st.file_uploader("Tải lên kế hoạch tổ (Word/PDF)", type=['docx', 'pdf'])
        if uploaded_file:
            st.success(f"Đã tải lên: {uploaded_file.name}")

    # TAB 5: THI ĐUA
    with tabs[4]:
        st.subheader("Theo dõi thi đua")
        st.write("Cập nhật danh hiệu và thành tích cá nhân hàng tháng.")
