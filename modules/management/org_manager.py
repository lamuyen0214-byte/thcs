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

    # TAB 3: BIÊN BẢN (THIẾT KẾ MỚI)
    with tabs[2]:
        st.markdown("## 📝 Quản Lý Hồ Sơ Biên Bản Tổ Chuyên Môn")
        
        bb_tabs = st.tabs(["📋 Kho Biên Bản", "➕ Viết Biên Bản Mới"])
        
        # Giao diện Nhập biên bản mới
        with bb_tabs[1]:
            st.markdown("### ✍️ Soạn thảo biên bản")
            with st.form("form_bien_ban", clear_on_submit=True):
                c1, c2 = st.columns([2, 1])
                tieu_de = c1.text_input("Tiêu đề cuộc họp", placeholder="VD: Sinh hoạt chuyên môn định kỳ tháng 9")
                ngay_hop = c2.date_input("Ngày họp")
                
                c3, c4, c5 = st.columns(3)
                dia_diem = c3.text_input("Địa điểm", value="Văn phòng trường")
                chu_tri = c4.text_input("Chủ trì", value="Lê Hồng Dưỡng")
                thu_ky = c5.text_input("Thư ký", placeholder="Nhập tên thư ký...")
                
                vang_mat = st.text_input("Thành viên vắng mặt (có phép/không phép)", placeholder="VD: Cô Trang (có phép), Không có (để trống)")
                
                st.markdown("**Nội dung cuộc họp:**")
                noi_dung = st.text_area("Nhập chi tiết nội dung triển khai...", height=200)
                
                st.markdown("**Kết luận / Biểu quyết:**")
                ket_luan = st.text_area("Nhập kết luận của chủ tọa...", height=100)
                
                if st.form_submit_button("💾 Lưu Biên Bản", type="primary"):
                    new_bb = {
                        "tieu_de": tieu_de,
                        "ngay_hop": str(ngay_hop),
                        "dia_diem": dia_diem,
                        "chu_tri": chu_tri,
                        "thu_ky": thu_ky,
                        "vang_mat": vang_mat if vang_mat else "Không",
                        "noi_dung": noi_dung,
                        "ket_luan": ket_luan
                    }
                    try:
                        supabase.table("bien_ban").insert(new_bb).execute()
                        st.success("🎉 Đã lưu biên bản thành công!")
                        st.rerun()
                    except Exception as e:
                        st.error("⚠️ Lỗi: Không thể lưu! Có thể thầy chưa tạo bảng 'bien_ban' trên Supabase.")
        
        # Giao diện Xem danh sách biên bản
        with bb_tabs[0]:
            df_bb = load_bien_ban_data()
            if df_bb.empty:
                st.info("📭 Tổ chuyên môn chưa có biên bản nào được lưu.")
            else:
                st.markdown(f"**Tổng số biên bản đã lưu:** `{len(df_bb)}`")
                for index, row in df_bb.iterrows():
                    # Thiết kế mỗi biên bản như một tập hồ sơ có thể xổ ra
                    with st.expander(f"📌 {row['ngay_hop']} | {row['tieu_de']}"):
                        st.markdown(f"""
                        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0;'>
                            <h3 style='text-align: center; color: #1f3a93;'>BIÊN BẢN CUỘC HỌP</h3>
                            <p style='text-align: center; font-style: italic;'>{row['tieu_de']}</p>
                            <hr>
                            <p><b>⏰ Thời gian:</b> {row['ngay_hop']}</p>
                            <p><b>📍 Địa điểm:</b> {row['dia_diem']}</p>
                            <p><b>👤 Chủ trì:</b> {row['chu_tri']} &nbsp;&nbsp;&nbsp;&nbsp; <b>📝 Thư ký:</b> {row['thu_ky']}</p>
                            <p><b>🚫 Vắng mặt:</b> {row['vang_mat']}</p>
                            <hr>
                            <h4 style='color: #2c3e50;'>I. Nội dung triển khai:</h4>
                            <p style='white-space: pre-wrap;'>{row['noi_dung']}</p>
                            <br>
                            <h4 style='color: #2c3e50;'>II. Kết luận:</h4>
                            <p style='white-space: pre-wrap;'>{row['ket_luan']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Nút xóa biên bản
                        if st.button("🗑️ Xóa biên bản này", key=f"del_{row['id']}"):
                            supabase.table("bien_ban").delete().eq("id", row['id']).execute()
                            st.rerun()

    with tabs[3]:
        st.write("Đang phát triển...")
    with tabs[4]:
        st.write("Đang phát triển...")
