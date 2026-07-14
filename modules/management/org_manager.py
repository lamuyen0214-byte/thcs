import streamlit as st
import pandas as pd
from datetime import datetime

def render_org_management():
    # 1. Khởi tạo dữ liệu persistent
    if 'team_members' not in st.session_state:
        st.session_state['team_members'] = pd.DataFrame(columns=["Họ tên", "Chức vụ", "Môn dạy", "Email/SĐT"])
    
    if 'meeting_logs' not in st.session_state:
        st.session_state['meeting_logs'] = []

    # 2. Tạo các Tab
    tabs = st.tabs([
        "👥 Danh sách thành viên", 
        "📋 Quản lý & Phân công", 
        "📝 Hỗ trợ sinh hoạt tổ", 
        "📂 Kế hoạch Tổ", 
        "📅 Kế hoạch cá nhân", 
        "🏆 Thành tích & Thi đua"
    ])

    # 3. Nội dung các Tab
    with tabs[0]:
        st.subheader("Danh sách thành viên tổ")
        with st.form("add_member", clear_on_submit=True):
            c1, c2 = st.columns(2)
            name = c1.text_input("Họ và tên")
            role = c2.selectbox("Chức vụ", ["Tổ trưởng", "Tổ phó", "Giáo viên", "Thư ký"])
            subject = c1.text_input("Môn dạy")
            contact = c2.text_input("Email/SĐT")
            if st.form_submit_button("➕ Thêm thành viên"):
                new_row = {"Họ tên": name, "Chức vụ": role, "Môn dạy": subject, "Email/SĐT": contact}
                st.session_state['team_members'] = pd.concat([st.session_state['team_members'], pd.DataFrame([new_row])], ignore_index=True)
                st.rerun()
        st.dataframe(st.session_state['team_members'], use_container_width=True)

    with tabs[1]:
        st.subheader("Bảng phân công chuyên môn")
        st.info("Chỉnh sửa trực tiếp trên bảng để phân công:")
        edited_df = st.data_editor(st.session_state['team_members'], use_container_width=True)
        if st.button("Lưu thay đổi phân công"):
            st.session_state['team_members'] = edited_df
            st.success("Đã cập nhật phân công!")

    with tabs[2]:
        st.subheader("Hỗ trợ biên bản họp")
        topic = st.text_input("Chủ đề cuộc họp")
        content = st.text_area("Nội dung chính")
        if st.button("✨ Lưu biên bản"):
            log = f"{datetime.now().strftime('%d/%m/%Y')} - {topic}: {content}"
            st.session_state['meeting_logs'].append(log)
            st.success("Đã lưu biên bản!")
        
        st.write("---")
        for log in reversed(st.session_state['meeting_logs']):
            st.info(log)

    with tabs[3]:
        st.subheader("Kho kế hoạch Tổ")
        st.file_uploader("Tải lên kế hoạch tổ (Word/PDF)", key="kht_upload")

    with tabs[4]:
        st.subheader("Kế hoạch giáo dục cá nhân")
        st.file_uploader("Tải lên KH cá nhân", key="khcn_upload")

    with tabs[5]:
        st.subheader("Thống kê thi đua")
        st.write("Dữ liệu thi đua sẽ tổng hợp từ hoạt động chuyên môn.")
        st.dataframe(st.session_state['team_members'], use_container_width=True)
