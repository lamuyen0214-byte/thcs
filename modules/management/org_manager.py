import streamlit as st
import pandas as pd
import io
from supabase import create_client
from datetime import datetime

# Kết nối Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- CÁC HÀM TẢI DỮ LIỆU ---
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

def load_phan_cong_data():
    try:
        response = supabase.table("phan_cong").select("*").execute()
        cols = ["ten_giao_vien", "mon_day", "lop_day", "so_tiet_tuan", "nhiem_vu_kiem_nhiem"]
        if not response.data:
            return pd.DataFrame(columns=cols)
        return pd.DataFrame(response.data)
    except:
        return pd.DataFrame()

def load_bien_ban_data():
    try:
        # Sắp xếp biên bản mới nhất lên đầu
        response = supabase.table("bien_ban").select("*").order("ngay_hop", desc=True).execute()
        if not response.data:
            return pd.DataFrame()
        return pd.DataFrame(response.data)
    except:
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

# --- GIAO DIỆN CHÍNH ---
def render_org_management():
    df_team = get_static_team_data()
    tabs = st.tabs(["👥 Danh sách thành viên", "📋 Phân công", "📝 Biên bản", "📂 Kế hoạch", "🏆 Thi đua"])

    # TAB 1: DANH SÁCH
    with tabs[0]:
        st.info("📌 Danh sách thành viên Tổ chuyên môn.")
        st.dataframe(df_team, use_container_width=True, hide_index=True,
            column_config={"ten": "Họ và tên", "ngay_sinh": "Năm sinh", "bang_cap": "Bằng cấp", "chu_the": "Môn dạy", "vai_tro": "Vai trò", "email": "Email", "dien_thoai": "SĐT"})

    # TAB 2: PHÂN CÔNG
    with tabs[1]:
        st.subheader("📋 Bảng Phân Công Chuyên Môn")
        df_pc_current = load_phan_cong_data()
        if not df_pc_current.empty:
            st.dataframe(df_pc_current, use_container_width=True, hide_index=True,
                column_config={"ten_giao_vien": "Giáo viên", "mon_day": "Môn dạy", "lop_day": "Lớp dạy", "so_tiet_tuan": "Số tiết/tuần", "nhiem_vu_kiem_nhiem": "Kiêm nhiệm"})
        
        with st.expander("📤 CẬP NHẬT LỊCH TỪ EXCEL", expanded=False):
            st.download_button("📥 Tải file Phân Công Mẫu", data=get_phan_cong_template(), file_name="Mau_Phan_Cong.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            uploaded_pc = st.file_uploader("Upload bảng phân công", type=["xlsx"], key="file_pc")
            if uploaded_pc is not None:
                try:
                    df_pc = pd.read_excel(uploaded_pc, dtype=str).fillna("")
                    cols_chuan = ["ten_giao_vien", "mon_day", "lop_day", "so_tiet_tuan", "nhiem_vu_kiem_nhiem"]
                    df_pc = df_pc[cols_chuan]
                    st.dataframe(df_pc, use_container_width=True)
                    if st.button("💾 Lưu Bảng Phân Công"):
                        import_data = df_pc.to_dict(orient="records")
                        try:
                            supabase.table("phan_cong").delete().neq("ten_giao_vien", "XOA_DU_LIEU_CU").execute()
                        except:
                            pass
                        supabase.table("phan_cong").insert(import_data).execute()
                        st.success("Đã lưu thành công!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Lỗi: {e}")

    # ... (các tab danh sách, phân công giữ nguyên) ...

    # TAB 3: BIÊN BẢN (GỌI TỪ FILE BIEN_BAN.PY)
    with tabs[2]:
        # Trỏ tới thư mục chứa file bien_ban.py
        from modules.management.bien_ban import render_bien_ban
        render_bien_ban(supabase)

    with tabs[3]:
        st.write("Đang phát triển...")

    with tabs[4]:
        st.write("Đang phát triển...")
