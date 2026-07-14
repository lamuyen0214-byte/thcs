import streamlit as st
import pandas as pd
from datetime import datetime

def render_org_management():
    # 1. Khởi tạo dữ liệu
    if 'team_members' not in st.session_state:
        st.session_state['team_members'] = pd.DataFrame(columns=["Họ tên", "Chức vụ", "Môn dạy", "Email/SĐT"])
    
    if 'meeting_logs' not in st.session_state:
        st.session_state['meeting_logs'] = []

    # 2. Tạo các Tab
    tabs = st.tabs([
        "👥 Danh sách", 
        "📋 Phân công", 
        "📝 Biên bản", 
        "📂 Kế hoạch", 
        "📅 Cá nhân", 
        "🏆 Thi đua"
    ])

    # 3. Nội dung các Tab
    with tabs[0]:
        st.subheader("Danh sách thành viên tổ")
        with st.form("add_member", clear_on_submit=True):
            c1, c2 = st.columns(2)
            name = c1.text_input("Họ và tên")
            role = c2.selectbox("Chức vụ", ["Tổ trưởng", "Giáo viên"])
            if st.form_submit_button("➕ Thêm"):
                new_row = {"Họ tên": name, "Chức vụ": role, "Môn dạy": "...", "Email/SĐT": "..."}
                st.session_state['team_members'] = pd.concat([st.session_state['team_members'], pd.DataFrame([new_row])], ignore_index=True)
                st.rerun()
        st.dataframe(st.session_state['team_members'], use_container_width=True)

    with tabs[1]:
        st.subheader("Phân công chuyên môn")
        edited_df = st.data_editor(st.session_state['team_members'], use_container_width=True)
        if st.button("Lưu phân công"):
            st.session_state['team_members'] = edited_df
            st.success("Đã lưu!")

    with tabs[2]:
        st.subheader("Biên bản họp")
        topic = st.text_input("Chủ đề")
        if st.button("Tạo biên bản"):
            st.info(f"Đã tạo biên bản: {topic}")
