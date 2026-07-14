import streamlit as st
from supabase import create_client
import pandas as pd
import io

# Kết nối Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def load_data():
    try:
        response = supabase.table("quan_ly_tcm").select("*").execute()
        cols = ["id", "ten", "ngay_sinh", "bang_cap", "chu_the", "vai_tro", "email", "dien_thoai"]
        if not response.data:
            return pd.DataFrame(columns=cols)
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu: {e}")
        return pd.DataFrame()

# Hàm tạo file Excel mẫu
@st.cache_data
def get_member_template():
    df_mau = pd.DataFrame({
        "ten": ["Lê Hồng Dưỡng", "Nguyễn Văn A"], "ngay_sinh": ["1976", "1985"],
        "bang_cap": ["ĐH", "Thạc sĩ"], "chu_the": ["KHTN", "Toán"],
        "vai_tro": ["Tổ trưởng", "Giáo viên"], "email": ["vjnagolf@gmail.com", "nguyenvana@gmail.com"],
        "dien_thoai": ["0984331178", "0909123456"]
    })
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_mau.to_excel(writer, index=False, sheet_name='Danh_Sach')
    return buffer.getvalue()

@st.cache_data
def get_phan_cong_template():
    df_mau = pd.DataFrame({
        "ten_giao_vien": ["Lê Hồng Dưỡng", "Nguyễn Văn A"], "mon_day": ["KHTN", "Toán"],
        "lop_day": ["9A1, 9A2", "9A3, 9A4"], "so_tiet_tuan": [10, 12],
        "nhiem_vu_kiem_nhiem": ["Bồi dưỡng HSG", "CN Lớp 9A3"]
    })
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_mau.to_excel(writer, index=False, sheet_name='Phan_Cong')
    return buffer.getvalue()


def render_org_management():
    df = load_data()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔐 Quyền Quản Trị")
    admin_password = st.sidebar.text_input("Nhập mật khẩu", type="password")
    is_admin = (admin_password == "admin")

    tabs = st.tabs(["👥 Danh sách thành viên", "📋 Phân công", "📝 Biên bản", "📂 Kế hoạch", "🏆 Thi đua"])

    with tabs[0]:
        if is_admin:
            st.success("🔓 Chế độ Admin: Thầy có thể Thêm, Sửa, Xóa thành viên.")
            c1, c2 = st.columns(2)
            with c1:
                with st.expander("➕ THÊM 1 THÀNH VIÊN", expanded=False):
                    with st.form("add_member", clear_on_submit=True):
                        ten = st.text_input("Họ và tên")
                        ngay_sinh = st.text_input("Năm sinh")
                        bang_cap = st.text_input("Bằng cấp")
                        chu_the = st.text_input("Môn dạy")
                        vai_tro = st.selectbox("Vai trò", ["Tổ trưởng", "Tổ phó", "Giáo viên", "Thư ký"])
                        email = st.text_input("Email")
                        dien_thoai = st.text_input("SĐT")
                        if st.form_submit_button("Lưu thành viên"):
                            new_row = {"ten": ten, "ngay_sinh": ngay_sinh, "bang_cap": bang_cap, "chu_the": chu_the, "vai_tro": vai_tro, "email": email, "dien_thoai": dien_thoai}
                            supabase.table("quan_ly_tcm").insert(new_row).execute()
                            st.rerun()
            
            with c2:
                with st.expander("📤 THÊM HÀNG LOẠT TỪ EXCEL", expanded=False):
                    st.download_button("📥 Tải file Excel Mẫu", data=get_member_template(), file_name="Mau_Danh_Sach.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    uploaded_file = st.file_uploader("Upload file Danh sách (.xlsx)", type=["xlsx"], key="file_ds")
                    
                    if uploaded_file is not None:
                        try:
                            # Đọc Excel dưới dạng chuỗi
                            df_import = pd.read_excel(uploaded_file, dtype=str)
                            
                            # CỐ ĐỊNH CỘT: Chỉ lấy đúng 7 cột này, loại bỏ mọi cột thừa bị tràn
                            cols_chuan = ["ten", "ngay_sinh", "bang_cap", "chu_the", "vai_tro", "email", "dien_thoai"]
                            df_import = df_import[cols_chuan].fillna("")
                            
                            st.dataframe(df_import, height=150)
                            
                            if st.button("🚀 Nạp vào hệ thống"):
                                import_data = df_import.to_dict(orient="records")
                                supabase.table("quan_ly_tcm").insert(import_data).execute()
                                st.success("Nạp thành công!")
                                st.rerun()
                        except KeyError:
                            st.error("⚠️ Lỗi: File Excel không có đủ các cột chuẩn. Thầy hãy tải lại file mẫu nhé!")
                        except Exception as e:
                            st.error(f"Lỗi: {e}")
            
            st.markdown("### ✏️ CHỈNH SỬA & XÓA THÀNH VIÊN")
            edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic", disabled=["id"], key="admin_editor")
            
            if st.button("💾 Đồng bộ thay đổi (Sửa/Xóa)"):
                try:
                    original_ids = set(df['id'].dropna().tolist())
                    current_ids = set(edited_df['id'].dropna().tolist())
                    for d_id in (original_ids - current_ids):
                        supabase.table("quan_ly_tcm").delete().eq("id", d_id).execute()
                        
                    records_to_update = edited_df.dropna(subset=['id']).to_dict(orient="records")
                    if records_to_update:
                        supabase.table("quan_ly_tcm").upsert(records_to_update).execute()
                    st.success("Đã đồng bộ thành công!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi lưu: {e}")
        else:
            st.info("🔒 Đang ở chế độ CHỈ XEM.")
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tabs[1]:
        st.subheader("📋 Bảng Phân Công Chuyên Môn")
        if is_admin:
            with st.expander("📤 CẬP NHẬT LỊCH TỪ EXCEL", expanded=True):
                st.download_button("📥 Tải file Phân Công Mẫu", data=get_phan_cong_template(), file_name="Mau_Phan_Cong.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                uploaded_pc = st.file_uploader("Upload bảng phân công", type=["xlsx"], key="file_pc")
                if uploaded_pc is not None:
                    try:
                        df_pc = pd.read_excel(uploaded_pc, dtype=str).fillna("")
                        st.dataframe(df_pc, use_container_width=True)
                        if st.button("💾 Lưu Bảng Phân Công"):
                            st.warning("⚠️ Cần tạo bảng `phan_cong` trên Supabase trước khi lưu!")
                    except Exception as e:
                        st.error(f"Lỗi: {e}")
        else:
            st.info("🔒 Bảng phân công đang được cập nhật...")
            
    with tabs[2]:
        st.write("Biên bản cuộc họp")
    with tabs[3]:
        st.write("Kế hoạch giáo dục")
    with tabs[4]:
        st.write("Thi đua - Khen thưởng")
