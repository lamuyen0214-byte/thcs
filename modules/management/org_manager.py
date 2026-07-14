import streamlit as st
from supabase import create_client
import pandas as pd

# Kết nối Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def load_data():
    try:
        response = supabase.table("quan_ly_tcm").select("*").execute()
        # Đảm bảo danh sách này KHỚP 100% với tên cột trên Supabase
        cols = ["id", "ten", "ngay_sinh", "bang_cap", "chu_the", "vai_tro", "email", "dien_thoai"]
        if not response.data:
            return pd.DataFrame(columns=cols)
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu: {e}")
        return pd.DataFrame()

def render_org_management():
    st.session_state['team_members'] = load_data()
    st.subheader("Quản lý Tổ chuyên môn")

    with st.form("add_member", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)
        ten = c1.text_input("Họ và tên")
        ngay_sinh = c2.text_input("Năm sinh")
        bang_cap = c3.text_input("Bằng cấp")
        c5, c6, c7, c8 = st.columns(4)
        chu_the = c5.text_input("Môn dạy")
        vai_tro = c6.selectbox("Vai trò", ["Tổ trưởng", "Tổ phó", "Giáo viên", "Thư ký"])
        email = c7.text_input("Email")
        dien_thoai = c8.text_input("SĐT")
        
        if st.form_submit_button("➕ Thêm thành viên"):
            try:
                # CÁC TÊN TRONG DẤU NGOẶC KÉP PHẢI KHỚP TUYỆT ĐỐI VỚI SUPABASE
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
                st.error(f"Lỗi Supabase: {e}")

    st.dataframe(st.session_state['team_members'], use_container_width=True)
