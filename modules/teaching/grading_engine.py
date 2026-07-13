import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from io import BytesIO
import json
def get_model(loai_bai_tap):
    if loai_bai_tap == "trac_nghiem":
        return genai.GenerativeModel('gemini-1.5-flash-latest')
    else:
        return genai.GenerativeModel('gemini-1.5-pro-latest')
def render_grading_module():
    st.subheader("📝 Chấm Trắc Nghiệm Hàng Loạt Bằng AI")
    # Thêm vào trong hàm render_grading_module()
model_choice = st.selectbox(
    "Chọn Model AI (Tùy vào quyền truy cập của tài khoản thầy/cô):",
    ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-lite"] 
)

# Sử dụng lựa chọn đó để khởi tạo model
model = genai.GenerativeModel(model_choice)
    # Khởi tạo session để lưu kết quả chấm hàng loạt
        if "ket_qua_cham" not in st.session_state:
            st.session_state.ket_qua_cham = []

    # 1. Thiết lập đáp án
    dap_an = st.text_input("Nhập đáp án chuẩn (VD: 1A, 2B, 3C, 4D...):")
    
    # 2. Upload nhiều ảnh
    uploaded_files = st.file_uploader("Chọn nhiều ảnh phiếu bài làm:", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    
    # 3. Nút hành động
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Chấm tất cả ảnh đã chọn"):
            if not dap_an or not uploaded_files:
                st.warning("Vui lòng nhập đáp án và chọn ảnh.")
            else:
                for file in uploaded_files:
                    with st.spinner(f"Đang chấm: {file.name}..."):
                        try:
                            model = get_model("trac_nghiem")
                            img = Image.open(file)
                            
                            prompt = f"""
                            Bạn là giáo viên. Đối chiếu phiếu trắc nghiệm này với đáp án: {dap_an}.
                            Trả về kết quả duy nhất dưới định dạng JSON:
                            {{"ten_file": "{file.name}", "so_cau_dung": 0, "tong_so_cau": 0, "diem": 0.0, "nhan_xet": "..."}}
                            """
                            response = model.generate_content([prompt, img])
                            # Xử lý lấy JSON từ response
                            res_text = response.text.replace('```json', '').replace('```', '')
                            ket_qua = json.loads(res_text)
                            st.session_state.ket_qua_cham.append(ket_qua)
                        except Exception as e:
                            st.error(f"Lỗi chấm file {file.name}: {e}")
                st.success("Đã chấm xong tất cả!")

    with col2:
        if st.button("🗑️ Xóa danh sách kết quả"):
            st.session_state.ket_qua_cham = []
            st.rerun()

    # 4. Hiển thị bảng tổng hợp và Xuất Excel
    if st.session_state.ket_qua_cham:
        df = pd.DataFrame(st.session_state.ket_qua_cham)
        st.table(df)
        
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='TongHop')
        
        st.download_button(
            label="📥 Tải file Excel tổng hợp",
            data=buffer,
            file_name="Ket_qua_tong_hop.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
