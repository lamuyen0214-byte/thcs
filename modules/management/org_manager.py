import streamlit as st
import pandas as pd
from datetime import datetime

def render_org_management():
    def render_org_management():
    st.warning("ĐANG CHẠY CODE MỚI NHẤT") # <--- Thêm dòng này vào
    # ... các code phía dưới ...
    # Khởi tạo dữ liệu mẫu nếu chưa có trong session
    if 'team_members' not in st.session_state:
        st.session_state['team_members'] = pd.DataFrame(columns=["Họ tên", "Chức vụ", "Môn dạy", "Email/SĐT"])
    
    if 'meeting_logs' not in st.session_state:
        st.session_state['meeting_logs'] = []

    # Danh sách các Tab
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
        with st.form("add_member", clear_on_submit=True):
            col1, col2 = st.columns(2)
            name = col1.text_input("Họ và tên")
            role = col2.selectbox("Chức vụ", ["Tổ trưởng", "Tổ phó", "Giáo viên", "Thư ký"])
            subject = col1.text_input("Môn dạy")
            contact = col2.text_input("Email/SĐT")
            if st.form_submit_button("➕ Thêm thành viên"):
                new_row = {"Họ tên": name, "Chức vụ": role, "Môn dạy": subject, "Email/SĐT": contact}
                st.session_state['team_members'] = pd.concat([st.session_state['team_members'], pd.DataFrame([new_row])], ignore_index=True)
                st.rerun()
        
        st.dataframe(st.session_state['team_members'], use_container_width=True)

    # 2. QUẢN LÝ & PHÂN CÔNG
    with tabs[1]:
        st.subheader("Phân công chuyên môn")
        st.info("Chỉnh sửa trực tiếp trên bảng để phân công giảng dạy:")
        edited_df = st.data_editor(st.session_state['team_members'], use_container_width=True)
        if st.button("Lưu phân công"):
            st.session_state['team_members'] = edited_df
            st.success("Đã cập nhật phân công!")

    # 3. HỖ TRỢ SINH HOẠT TỔ
    with tabs[2]:
        st.subheader("Biên bản họp tổ nhanh")
        topic = st.text_input("Chủ đề cuộc họp")
        content = st.text_area("Nội dung thảo luận chính")
        if st.button("✨ Tạo biên bản"):
            report = f"BIÊN BẢN NGÀY {datetime.now().strftime('%d/%m/%Y')}\nChủ đề: {topic}\nNội dung: {content}"
            st.session_state['meeting_logs'].append(report)
            st.success("Biên bản đã được lưu!")
        
        st.write("---")
        for idx, log in enumerate(reversed(st.session_state['meeting_logs'])):
            st.text_area(f"Biên bản {idx+1}", value=log, height=100, disabled=True)

    # 4. KẾ HOẠCH TỔ & 5. KẾ HOẠCH CÁ NHÂN
    for tab_idx, title in [(3, "Kế hoạch Tổ"), (4, "Kế hoạch cá nhân")]:
        with tabs[tab_idx]:
            st.subheader(title)
            uploaded_file = st.file_uploader(f"Tải lên file {title} (Word/PDF/Excel)", type=['docx', 'pdf', 'xlsx'], key=title)
            if uploaded_file:
                st.success(f"Đã lưu: {uploaded_file.name}")

    # 6. THÀNH TÍCH & THI ĐUA
    with tabs[5]:
        st.subheader("Danh sách thi đua")
        score_df = st.session_state['team_members'][["Họ tên", "Môn dạy"]].copy()
        score_df["Điểm thi đua"] = 0
        score_df["Xếp loại"] = "Tốt"
        st.data_editor(score_df, use_container_width=True)
