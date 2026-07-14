import streamlit as st
from supabase import create_client
import pandas as pd

# Kết nối Supabase sử dụng Secrets
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def load_data():
    try:
        response = supabase.table("quan_ly_tcm").select("*").execute()
        if not response.data:
            return pd.DataFrame(columns=["id", "tên", "ngày sinh", "bằng cấp", "chủ thể", "vai trò", "email", "phone"])
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu: {e}")
        return pd.DataFrame()

def save_data(df):
    try:
        # Xóa hết dữ liệu cũ và thêm lại dữ liệu mới (đơn giản nhất)
        supabase.table("quan_ly_tcm").delete().neq("id", 0).execute()
        data = df.to_dict(orient='records')
        supabase.table("quan_ly_tcm").insert(data).execute()
        st.success("Đã đồng bộ lên Supabase!")
    except Exception as e:
        st.error(f"Lỗi lưu dữ liệu: {e}")

def render_org_management():
    # Load dữ liệu
    st.session_state['team_members'] = load_data()

    tabs = st.tabs(["👥 Danh sách thành viên", "📋 Phân công", "📝 Biên bản", "📂 Kế hoạch", "🏆 Thi đua"])

    with tabs[0]:
        st.subheader("Quản lý thông tin giáo viên")
        
        with st.form("add_member_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            name = c1.text_input("Họ và tên")
            dob = c2.text_input("Ngày sinh")
            degree = c3.text_input("Bằng cấp")
            c4, c5, c6, c7 = st.columns(4)
            subject = c4.text_input("Chủ thể (Môn)")
            role = c5.selectbox("Vai trò", ["Tổ trưởng", "Tổ phó", "Giáo viên", "Thư ký"])
            email = c6.text_input("Email")
            phone = c7.text_input("SĐT")
            
            if st.form_submit_button("➕ Thêm vào danh sách"):
                new_row = {
                    "tên": name, "ngày sinh": dob, "bằng cấp": degree, 
                    "chủ thể": subject, "vai trò": role, "email": email, "phone": phone
                }
                supabase.table("quan_ly_tcm").insert(new_row).execute()
                st.rerun()

        st.dataframe(st.session_state['team_members'], use_container_width=True)

    with tabs[1]:
        st.subheader("Phân công chuyên môn")
        edited_df = st.data_editor(st.session_state['team_members'], use_container_width=True)
        if st.button("Lưu thay đổi"):
            save_data(edited_df)
            st.rerun()
