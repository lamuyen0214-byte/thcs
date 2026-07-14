import streamlit as st
import pandas as pd
import io
from supabase import create_client

# Kết nối Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# Dữ liệu tĩnh Danh sách giáo viên
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

# Hàm tải dữ liệu phân công từ Supabase
def load_phan_cong_data():
    try:
        response = supabase.table("phan_cong").select("*").execute()
        cols = ["ten_giao_vien", "mon_day", "lop_day", "so_tiet_tuan", "nhiem_vu_kiem_nhiem"]
        if not response.data:
            return pd.DataFrame(columns=cols)
        return pd.DataFrame(response.data)
    except Exception as e:
        return pd.DataFrame()

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
    df = get_static_team_data()

    tabs = st.tabs(["👥 Danh sách thành viên", "📋 Phân công", "📝 Biên bản", "📂 Kế hoạch", "🏆 Thi đua"])

    with tabs[0]:
        st.info("📌 Danh sách thành viên Tổ chuyên môn.")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ten": "Họ và tên", "ngay_sinh": "Năm sinh", "bang_cap": "Bằng cấp",
                "chu_the": "Môn dạy", "vai_tro": "Vai trò", "email": "Email", "dien_thoai": "SĐT"
            }
        )

    with tabs[1]:
        st.subheader("📋 Bảng Phân Công Chuyên Môn")
        
        # 1. Hiển thị dữ liệu đang có trên máy chủ
        df_pc_current = load_phan_cong_data()
        if not df_pc_current.empty:
            st.markdown("### Dữ liệu phân công hiện hành")
            st.dataframe(
                df_pc_current, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "ten_giao_vien": "Giáo viên",
                    "mon_day": "Môn dạy",
                    "lop_day": "Lớp dạy",
                    "so_tiet_tuan": "Số tiết/tuần",
                    "nhiem_vu_kiem_nhiem": "Kiêm nhiệm"
                }
            )
        else:
            st.info("Chưa có dữ liệu phân công trên hệ thống. Vui lòng tải file Excel lên để cập nhật.")

        # 2. Khu vực Upload Excel
        with st.expander("📤 CẬP NHẬT LỊCH TỪ EXCEL", expanded=True):
            st.download_button(
                "📥 Tải file Phân Công Mẫu", 
                data=get_phan_cong_template(), 
                file_name="Mau_Phan_Cong.xlsx", 
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            uploaded_pc = st.file_uploader("Upload bảng phân công đã điền (.xlsx)", type=["xlsx"], key="file_pc")
            
            if uploaded_pc is not None:
                try:
                    # Đọc file và chốt đúng 5 cột
                    df_pc = pd.read_excel(uploaded_pc, dtype=str).fillna("")
                    cols_chuan = ["ten_giao_vien", "mon_day", "lop_day", "so_tiet_tuan", "nhiem_vu_kiem_nhiem"]
                    df_pc = df_pc[cols_chuan]
                    
                    st.markdown("**👀 Xem trước dữ liệu sẽ nạp:**")
                    st.dataframe(df_pc, use_container_width=True)
                    
                    if st.button("💾 Lưu Bảng Phân Công Lên Hệ Thống"):
                        import_data = df_pc.to_dict(orient="records")
                        
                        # Xóa sạch dữ liệu cũ trên Supabase trước khi nạp dữ liệu mới để tránh bị trùng lặp
                        try:
                            supabase.table("phan_cong").delete().neq("ten_giao_vien", "XOA_DU_LIEU_CU").execute()
                        except:
                            pass
                            
                        # Lưu dữ liệu mới
                        supabase.table("phan_cong").insert(import_data).execute()
                        
                        st.success("🎉 Đã lưu Bảng phân công thành công!")
                        st.rerun()
                        
                except KeyError:
                    st.error("⚠️ Lỗi: Cột trong file Excel không khớp. Thầy hãy dùng đúng file mẫu nhé!")
                except Exception as e:
                    st.error(f"Lỗi hệ thống: {e}")
                    
    with tabs[2]:
        st.write("Đang phát triển...")
    with tabs[3]:
        st.write("Đang phát triển...")
    with tabs[4]:
        st.write("Đang phát triển...")
