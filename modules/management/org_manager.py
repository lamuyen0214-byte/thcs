import streamlit as st
from supabase import create_client
import pandas as pd

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

def render_org_management():
    # Lấy dữ liệu từ máy chủ
    df = load_data()
    
    # --- CHỨC NĂNG ADMIN (Thanh bên trái) ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔐 Quyền Quản Trị")
    admin_password = st.sidebar.text_input("Nhập mật khẩu Admin", type="password", help="Chỉ Tổ trưởng mới có quyền thay đổi dữ liệu.")
    
    # Mật khẩu đang được đặt mặc định là "admin" (Thầy có thể sửa chữ "admin" này thành bất kỳ mật khẩu nào thầy muốn)
    is_admin = (admin_password == "admin") 

    # --- GIAO DIỆN CŨ (CÁC TABS) ---
    tabs = st.tabs(["👥 Danh sách thành viên", "📋 Phân công", "📝 Biên bản", "📂 Kế hoạch", "🏆 Thi đua"])

    with tabs[0]:
        if is_admin:
            st.success("🔓 Đã xác thực quyền Admin! Thầy có thể Thêm, Sửa và Xóa thông tin bên dưới.")
            
            # KHU VỰC 1: THÊM THÀNH VIÊN
            with st.expander("➕ THÊM THÀNH VIÊN MỚI", expanded=False):
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
                    
                    if st.form_submit_button("Lưu thành viên"):
                        new_row = {
                            "ten": ten, "ngay_sinh": ngay_sinh, "bang_cap": bang_cap, 
                            "chu_the": chu_the, "vai_tro": vai_tro, "email": email, "dien_thoai": dien_thoai
                        }
                        supabase.table("quan_ly_tcm").insert(new_row).execute()
                        st.rerun()
            
            # KHU VỰC 2: BẢNG SỬA & XÓA
            st.markdown("### ✏️ CHỈNH SỬA & XÓA THÀNH VIÊN")
            st.info("💡 Hướng dẫn: \n"
                    "- **Để SỬA:** Nhấp đúp chuột vào ô bất kỳ để gõ nội dung mới.\n"
                    "- **Để XÓA:** Chọn hàng (bấm vào ô vuông nhỏ ngoài cùng bên trái của hàng) rồi nhấn phím 'Delete' trên bàn phím máy tính.")
            
            # Bảng cho phép thao tác trực tiếp
            edited_df = st.data_editor(
                df,
                use_container_width=True,
                num_rows="dynamic", # Cấp quyền cho phép xóa dòng
                disabled=["id"],    # Khóa không cho ai sửa mã ID của máy chủ
                key="admin_editor"
            )
            
            # Nút lưu thay đổi
            if st.button("💾 Đồng bộ thay đổi (Sửa/Xóa) lên máy chủ"):
                try:
                    # 1. Tìm và xóa các dòng đã bị người dùng xóa trên giao diện
                    original_ids = set(df['id'].dropna().tolist())
                    current_ids = set(edited_df['id'].dropna().tolist())
                    deleted_ids = original_ids - current_ids
                    
                    for d_id in deleted_ids:
                        supabase.table("quan_ly_tcm").delete().eq("id", d_id).execute()
                        
                    # 2. Cập nhật (Sửa) các dòng bị thay đổi nội dung
                    records_to_update = edited_df.dropna(subset=['id']).to_dict(orient="records")
                    if records_to_update:
                        supabase.table("quan_ly_tcm").upsert(records_to_update).execute()
                        
                    st.success("Đã đồng bộ toàn bộ thay đổi thành công!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi khi lưu thay đổi: {e}")

        else:
            # GIAO DIỆN CHO GIÁO VIÊN BÌNH THƯỜNG (CHỈ XEM)
            st.info("🔒 Đang ở chế độ CHỈ XEM. Để chỉnh sửa, vui lòng nhập mật khẩu Admin ở thanh menu bên trái.")
            # Bảng này chỉ hiển thị, không cho phép click vào để sửa
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tabs[1]:
        st.subheader("Phân công chuyên môn")
        st.write("Tính năng đang phát triển...")
    with tabs[2]:
        st.subheader("Biên bản cuộc họp")
        st.write("Tính năng đang phát triển...")
    with tabs[3]:
        st.subheader("Kế hoạch giáo dục")
        st.write("Tính năng đang phát triển...")
    with tabs[4]:
        st.subheader("Thi đua - Khen thưởng")
        st.write("Tính năng đang phát triển...")
