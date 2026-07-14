import streamlit as st
import pandas as pd
import io

# Dữ liệu được đưa thẳng vào code theo đúng danh sách thầy cung cấp (Cố định, không chỉnh sửa)
def get_static_team_data():
    data = [
        {"ten": "Lê Hồng Dưỡng", "ngay_sinh": "1976", "bang_cap": "ĐH", "chu_the": "KHTN (Lý) - CN", "vai_tro": "Tổ trưởng", "email": "vjnagolf@gmail.com", "dien_thoai": "0984331178"},
        {"ten": "Nguyễn Thị Huyền Trang", "ngay_sinh": "1983", "bang_cap": "Thạc sĩ", "chu_the": "KHTN (Lý) - CN", "vai_tro": "Giáo viên", "email": "nguyenvana@gmail.com", "dien_thoai": "0909123457"},
        {"ten": "Lý Nguyễn Thu Nhi", "ngay_sinh": "1979", "bang_cap": "ĐH", "chu_the": "KHTN (Lý) - CN", "vai_tro": "Giáo viên", "email": "nguyenvana@gmail.com", "dien_thoai": "0909123458"},
        {"ten": "Khương Thị Thúy Vân", "ngay_sinh": "1979", "bang_cap": "ĐH", "chu_the": "KHTN (Sinh)", "vai_tro": "Giáo viên", "email": "nguyenvana@gmail.com", "dien_thoai": "0909123460"},
        {"ten": "Trần Xuân Hạnh", "ngay_sinh": "1985", "bang_cap": "ĐH", "chu_the": "GDTC", "vai_tro": "Giáo viên", "email": "nguyenvana@gmail.com", "dien_thoai": "0909123461"},
        {"ten": "Trương Vĩnh Văn", "ngay_sinh": "1981", "bang_cap": "ĐH", "chu_the": "KHTN (Sinh) - GDTC", "vai_tro": "Giáo viên", "email": "nguyenvana@gmail.com", "dien_thoai": "0909123462"},
        {"ten": "Phạm Xuân Thọ", "ngay_sinh": "1979", "bang_cap": "ĐH", "chu_the": "KHTN (Sinh) - GDTC", "vai_tro": "Giáo viên", "email": "nguyenvana@gmail.com", "dien_thoai": "0909123463"},
        {"ten": "Lê Hùng Cường", "ngay_sinh": "1988", "bang_cap": "ĐH", "chu_the": "KHTN (Lý) - CN", "vai_tro": "Giáo viên", "email": "nguyenvana@gmail.com", "dien_thoai": "0909123464"},
        {"ten": "Phạm Thùy Ngoan", "ngay_sinh": "1980", "bang_cap": "ĐH", "chu_the": "KHTN (Hóa)", "vai_tro": "Giáo viên", "email": "nguyenvana@gmail.com", "dien_thoai": "0909123465"},
        {"ten": "Phạm Thị Minh Anh", "ngay_sinh": "2002", "bang_cap": "ĐH", "chu_the": "KHTN (Hóa-Sinh)", "vai_tro": "Giáo viên", "email": "nguyenvana@gmail.com", "dien_thoai": "0909123466"},
    ]
    return pd.DataFrame(data)

@st.cache_data
def get_phan_cong_template():
    df_mau = pd.DataFrame({
        "ten_giao_vien": ["Lê Hồng Dưỡng", "Nguyễn Thị Huyền Trang"], "mon_day": ["KHTN", "KHTN"],
        "lop_day": ["9A1, 9A2", "9A3, 9A4"], "so_tiet_tuan": [10, 12],
        "nhiem_vu_kiem_nhiem": ["Bồi dưỡng HSG", "CN Lớp 9A3"]
    })
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_mau.to_excel(writer, index=False, sheet_name='Phan_Cong')
    return buffer.getvalue()

def render_org_management():
    # Lấy dữ liệu tĩnh đã lưu trong code
    df = get_static_team_data()

    tabs = st.tabs(["👥 Danh sách thành viên", "📋 Phân công", "📝 Biên bản", "📂 Kế hoạch", "🏆 Thi đua"])

    # ==========================================
    # TAB 0: DANH SÁCH THÀNH VIÊN (CHỈ XEM)
    # ==========================================
    with tabs[0]:
        st.info("📌 Danh sách thành viên Tổ chuyên môn.")
        # Cấu hình lại tiêu đề cột cho đẹp khi hiển thị
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ten": "Họ và tên",
                "ngay_sinh": "Năm sinh",
                "bang_cap": "Bằng cấp",
                "chu_the": "Môn dạy",
                "vai_tro": "Vai trò",
                "email": "Email",
                "dien_thoai": "SĐT"
            }
        )

    # ==========================================
    # TAB 1: PHÂN CÔNG CHUYÊN MÔN
    # ==========================================
    with tabs[1]:
        st.subheader("📋 Bảng Phân Công Chuyên Môn")
        with st.expander("📤 CẬP NHẬT LỊCH TỪ EXCEL", expanded=True):
            st.download_button(
                "📥 Tải file Phân Công Mẫu", 
                data=get_phan_cong_template(), 
                file_name="Mau_Phan_Cong.xlsx", 
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            uploaded_pc = st.file_uploader("Upload bảng phân công", type=["xlsx"], key="file_pc")
            
            if uploaded_pc is not None:
                try:
                    df_pc = pd.read_excel(uploaded_pc, dtype=str).fillna("")
                    st.dataframe(df_pc, use_container_width=True)
                    if st.button("💾 Lưu Bảng Phân Công"):
                        st.warning("⚠️ Chúng ta cần kết nối tính năng này với cơ sở dữ liệu.")
                except Exception as e:
                    st.error(f"Lỗi: {e}")
                    
    with tabs[2]:
        st.write("Đang phát triển...")
    with tabs[3]:
        st.write("Đang phát triển...")
    with tabs[4]:
        st.write("Đang phát triển...")
