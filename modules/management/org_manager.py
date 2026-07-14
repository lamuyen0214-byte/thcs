import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Cấu hình kết nối Google Sheets
SPREADSHEET_ID = "1C6642jk_oQ0g9UC2By2qsNxxfQVR0MrZYj52tRdWDlY"
SHEET_NAME = "TO_CM"

def get_gsheet_connection():
    # Thầy thay đường dẫn đến file JSON của thầy ở đây
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("gen-lang-client-0756857962-85230ff4f039.json", scope
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

def load_data():
    sheet = get_gsheet_connection()
    data = sheet.get_all_records()
    if not data:
        return pd.DataFrame(columns=["Họ và tên", "Năm sinh", "Trình độ", "Môn dạy", "Chức vụ", "Email", "SĐT"])
    return pd.DataFrame(data)

def save_data(df):
    sheet = get_gsheet_connection()
    sheet.clear() # Xóa cũ
    sheet.update([df.columns.values.tolist()] + df.values.tolist()) # Ghi mới

def render_org_management():
    # Load dữ liệu từ Sheet thay vì session_state
    if 'team_members' not in st.session_state:
        st.session_state['team_members'] = load_data()

    tabs = st.tabs(["👥 Danh sách thành viên", "📋 Phân công", "📝 Biên bản", "📂 Kế hoạch", "🏆 Thi đua"])

    with tabs[0]:
        st.subheader("Quản lý thông tin giáo viên (Lưu trực tiếp lên Sheet)")
        
        # --- PHẦN NHẬP LIỆU ---
        with st.form("add_member_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            name = c1.text_input("Họ và tên")
            dob = c2.text_input("Năm sinh")
            degree = c3.text_input("Trình độ")
            c4, c5, c6, c7 = st.columns(4)
            subject = c4.text_input("Môn dạy")
            role = c5.selectbox("Chức vụ", ["Tổ trưởng", "Tổ phó", "Giáo viên", "Thư ký"])
            email = c6.text_input("Email")
            phone = c7.text_input("SĐT")
            
            if st.form_submit_button("➕ Thêm vào danh sách"):
                new_row = pd.DataFrame([[name, dob, degree, subject, role, email, phone]], columns=st.session_state['team_members'].columns)
                st.session_state['team_members'] = pd.concat([st.session_state['team_members'], new_row], ignore_index=True)
                save_data(st.session_state['team_members']) # Lưu ngay lên Sheet
                st.rerun()

        # Hiển thị danh sách với Index từ 1
        df_display = st.session_state['team_members'].copy()
        df_display.index = df_display.index + 1
        st.dataframe(df_display, use_container_width=True)

    with tabs[1]:
        st.subheader("Phân công chuyên môn")
        edited_df = st.data_editor(st.session_state['team_members'], use_container_width=True)
        if st.button("Lưu thay đổi lên Sheet"):
            save_data(edited_df)
            st.session_state['team_members'] = edited_df
            st.success("Đã đồng bộ lên Sheet!")
