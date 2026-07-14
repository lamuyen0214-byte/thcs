import streamlit as st
import pandas as pd
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Cấu hình
SPREADSHEET_ID = "1C6642jk_oQ0g9UC2By2qsNxxfQVR0MrZYj52tRdWDlY"
SHEET_NAME = "TO_CM"

def get_gsheet_connection():
    # Lấy thông tin từ Secrets (đã thiết lập trong Streamlit Cloud)
    # Đảm bảo trong phần Secrets của Streamlit Cloud, thầy đã dán nội dung JSON vào key là GOOGLE_SHEETS_JSON
    secrets_dict = json.loads(st.secrets["GOOGLE_SHEETS_JSON"])
    
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Sử dụng from_json_keyfile_dict thay vì from_json_keyfile_name
    creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets_dict, scope)
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

def load_data():
    try:
        sheet = get_gsheet_connection()
        data = sheet.get_all_records()
        if not data:
            return pd.DataFrame(columns=["Họ và tên", "Năm sinh", "Trình độ", "Môn dạy", "Chức vụ", "Email", "SĐT"])
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Lỗi kết nối Sheet: {e}")
        return pd.DataFrame(columns=["Họ và tên", "Năm sinh", "Trình độ", "Môn dạy", "Chức vụ", "Email", "SĐT"])

def save_data(df):
    try:
        sheet = get_gsheet_connection()
        sheet.clear()
        # Chuyển đổi dataframe về dạng list để ghi vào Google Sheet
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
    except Exception as e:
        st.error(f"Lỗi lưu dữ liệu: {e}")

def render_org_management():
    # Load dữ liệu từ Sheet
    if 'team_members' not in st.session_state:
        st.session_state['team_members'] = load_data()

    tabs = st.tabs(["👥 Danh sách thành viên", "📋 Phân công", "📝 Biên bản", "📂 Kế hoạch", "🏆 Thi đua"])

    with tabs[0]:
        st.subheader("Quản lý thông tin giáo viên")
        
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
                save_data(st.session_state['team_members'])
                st.rerun()

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
