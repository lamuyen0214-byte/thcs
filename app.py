# --- 6. ROUTER PHÂN CẤP CHUẨN XÁC ---
# Lấy giá trị hiện tại của selectbox
phan_he_selected = phan_he 

if phan_he_selected == "Hỗ trợ Giáo viên":
    try:
        from views.teacher_support import render_module
        render_module()
    except Exception as e:
        st.error(f"Lỗi nạp Hỗ trợ Giáo viên: {e}")

elif phan_he_selected == "Hỗ trợ Giảng dạy":
    try:
        from views.teaching_support import render_module
        render_module()
    except Exception as e:
        st.error(f"Lỗi nạp Hỗ trợ Giảng dạy: {e}")

elif phan_he_selected == "Quản lý Tổ chuyên môn":
    try:
        from views.department_mgmt import render_module
        render_module()
    except Exception as e:
        st.error(f"Lỗi nạp Quản lý Tổ chuyên môn: {e}")
