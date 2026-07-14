import streamlit as st
import pandas as pd

def render_org_management():
    # Khởi tạo data mẫu nếu chưa có
    if 'team_members' not in st.session_state:
        st.session_state['team_members'] = pd.DataFrame(columns=["Họ tên", "Chức vụ", "Môn dạy", "Ghi chú"])

    # Danh sách các Tab khớp với screenshot của thầy
    tabs = st.tabs([
        "👥 Danh sách thành viên", 
        "📋 Quản lý & Phân công", 
        "📝 Hỗ trợ sinh hoạt tổ", 
        "📂 Kế hoạch Tổ", 
        "📅 Kế hoạch cá nhân", 
        "🏆 Thành tích & Thi đua"
    ])

    # 1. DANH SÁCH THÀNH VIÊN
    with tabs[0]:
        st.subheader("Quản lý thông tin giáo viên")
        with st.form("add_member"):
            col1, col2 = st.columns(2)
            name = col1.text_input("Họ và tên")
            role = col2.selectbox("Chức vụ", ["Tổ trưởng", "Tổ phó", "Giáo viên", "Thư ký"])
            subject = col1.text_input("Môn dạy")
            note = col2.text_input("Ghi chú")
            if st.form_submit_button("➕ Thêm thành viên"):
                new_data = {"Họ tên": name, "Chức vụ": role, "Môn dạy": subject, "Ghi chú": note}
                st.session_state['team_members'] = pd.concat([st.session_state['team_members'], pd.DataFrame([new_data])], ignore_index=True)
                st.rerun()
        st.table(st.session_state['team_members'])

    # 2. PHÂN CÔNG CHUYÊN MÔN
    with tabs[1]:
        st.info("Chỉnh sửa bảng phân công chuyên môn trực tiếp bên dưới:")
        st.data_editor(st.session_state['team_members'], use_container_width=True)

    # 3. HỖ TRỢ SINH HOẠT TỔ
    with tabs[2]:
        st.subheader("Hỗ trợ soạn Biên bản họp")
        noidung = st.text_area("Nội dung chính cuộc họp:")
        if st.button("✨ AI Soạn biên bản"):
            st.success("AI đã tạo dự thảo:")
            st.info("Dự thảo biên bản sinh hoạt tổ tháng này...")

    # 4. KẾ HOẠCH TỔ
    with tabs[3]:
        st.subheader("Kho lưu trữ Kế hoạch Tổ")
        st.file_uploader("Tải lên kế hoạch (Word/PDF)", key="kht")

    # 5. KẾ HOẠCH CÁ NHÂN
    with tabs[4]:
        st.subheader("Kế hoạch giáo dục cá nhân")
        st.write("Quản lý kế hoạch giảng dạy của từng giáo viên.")
        st.file_uploader("Tải lên KH cá nhân", key="khcn")

    # 6. THÀNH TÍCH & THI ĐUA
    with tabs[5]:
        st.subheader("Thống kê thi đua")
        st.metric("Tổng số danh hiệu đạt được", "12")
