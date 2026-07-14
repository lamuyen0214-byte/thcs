import streamlit as st
from supabase import create_client
import pandas as pd

# Kết nối Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def load_data():
    try:
        response = supabase.table("quan_ly_tcm").select("*").execute()
        if not response.data:
            return pd.DataFrame(columns=["id", "ten", "ngay_sinh", "bang_cap", "chu_the", "vai_tro", "email", "dien_thoai"])
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu: {e}")
        return pd.DataFrame()

def save_data(df):
    try:
        # Cập nhật từng dòng (upsert)
        data = df.to_dict(orient='records')
        supabase.table("quan_ly_tcm").upsert(data).execute()
        st.success("Đã đồng bộ!")
    except Exception as e:
        st.error(f"Lỗi lưu: {e}")

def render_org_management():
    st.session_state['team_members'] = load_data()
    tabs = st.tabs(["👥 Danh sách", "📋 Phân công"])

    with tabs[0]:
        with st.form("add_member", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            ten = c1.text_input("Họ và tên")
            ngay_sinh = c2.text_input("Ngày sinh")
            bang_cap = c3.text_input("Bằng cấp")
            c4, c5, c6, c7 = st.columns(4)
            chu_the = c4.text_input("Môn dạy")
            vai_tro = c5.selectbox("Vai trò", ["Tổ trưởng", "Tổ phó", "Giáo viên", "Thư ký"])
            email = c6.text_input("Email")
            dien_thoai = c7.text_input("SĐT")
            
            if st.form_submit_button("➕ Thêm thành viên"):
            try:
                # Đảm bảo các key ở đây KHÔNG CÓ DẤU, khớp 100% với tên cột trên Supabase
                new_row = {
                    "ten": ten, 
                    "ngay_sinh": ngay_sinh, 
                    "bang_cap": bang_cap, 
                    "chu_the": chu_the, 
                    "vai_tro": vai_tro, 
                    "email": email, 
                    "dien_thoai": dien_thoai
                }
                supabase.table("quan_ly_tcm").insert(new_row).execute()
                st.success("Thêm thành công!")
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi: {e}")
