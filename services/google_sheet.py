
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from datetime import datetime

# ================= CẤU HÌNH GOOGLE SHEETS =================
SPREADSHEET_ID = "1C6642jk_oQ0g9UC2By2qsNxxfQVR0MrZYj52tRdWDlY"
TAB_NAME = "DE_KT"

def get_exam_sheet():
    """Hàm hỗ trợ kết nối Google Sheets an toàn thông qua Streamlit Secrets"""
    try:
        # Đọc thông tin xác thực từ Streamlit Secrets
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
        )
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(SPREADSHEET_ID).worksheet(TAB_NAME)
        return sheet
    except Exception as e:
        st.error(f"⚠️ Lỗi kết nối Google Sheets: Vui lòng kiểm tra lại cấu hình gcp_service_account trong Secrets. Chi tiết: {e}")
        return None

def luu_lich_su_de_kt(mon_hoc, lop, ten_bai, hinh_thuc, tong_diem_tn, tong_diem_tl):
    """Hàm ghi thông tin đề kiểm tra mới tạo vào bảng tính"""
    sheet = get_exam_sheet()
    if sheet:
        try:
            thoi_gian_tao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # Nối một dòng mới vào Google Sheets
            sheet.append_row([
                thoi_gian_tao, 
                mon_hoc, 
                lop, 
                ten_bai, 
                hinh_thuc, 
                f"{tong_diem_tn} điểm", 
                f"{tong_diem_tl} điểm"
            ])
            return True
        except Exception as e:
            st.error(f"⚠️ Không thể lưu dữ liệu vào Sheets: {e}")
            return False
    return False
