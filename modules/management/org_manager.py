import streamlit as st
import pandas as pd
import io

def render_org_management():
    # Khởi tạo data với các cột mới
    cols = ["Họ và tên", "Năm sinh", "Trình độ", "Môn dạy", "Chức vụ", "Email", "SĐT"]
    if 'team_members' not in st.session_state:
        st.session_state['team_members'] = pd.DataFrame(columns=cols)

    tabs = st.tabs(["👥 Danh sách thành viên", "📋 Phân công", "📝 Biên bản", "📂 Kế hoạch", "🏆 Thi đua"])

    with tabs[0]:
        st.subheader("Quản lý thông tin giáo viên")
        
        # --- PHẦN IMPORT / EXPORT EXCEL ---
        col_up, col_down = st.columns(2)
        with col_up:
            uploaded_file = st.file_uploader("📥 Nhập từ Excel", type=["xlsx"])
            if uploaded_file:
                st.session_state['team_members'] = pd.read_excel(uploaded_file)
                st.success("Đã cập nhật danh sách!")
        
        with col_down:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                st.session_state['team_members'].to_excel(writer, index=False)
            st.download_button(label="📤 Tải xuống Excel", data=buffer.getvalue(), file_name="Danh_sach_Giao_vien.xlsx", mime="application/vnd.ms-excel")

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
                new_row = pd.DataFrame([[name, dob, degree, subject, role, email, phone]], columns=cols)
                st.session_state['team_members'] = pd.concat([st.session_state['team_members'], new_row], ignore_index=True)
                st.rerun()

        # Hiển thị danh sách
        st.dataframe(st.session_state['team_members'], use_container_width=True)

    # Các tab còn lại giữ nguyên
    with tabs[1]:
        st.info("Sử dụng bảng trên để quản lý phân công.")
        st.data_editor(st.session_state['team_members'], use_container_width=True)
    with tabs[2]:
        st.write("Tính năng biên bản đang được phát triển...")
    with tabs[3]:
        st.write("Kế hoạch tổ...")
    with tabs[4]:
        st.write("Thành tích...")
