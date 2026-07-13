import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from io import BytesIO
import json

def get_model(model_name):
    """Hàm khởi tạo model theo tên được chọn"""
    return genai.GenerativeModel(model_name)

def render_grading_module():
    st.subheader("📝 Chấm Trắc Nghiệm Hàng Loạt Bằng AI")
    
    # 1. Chọn Model (Dành cho mọi giáo viên)
    model_choice = st.selectbox(
        "Chọn Model AI:",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-lite"] 
    )

    # 2. Khởi tạo session lưu kết quả
    if "ket_qua_cham" not in st.session_state:
        st.session_state.ket_qua_cham = []

    # 3. Thiết lập đáp án
    dap_an = st.text_input("Nhập đáp án chuẩn (VD: 1A, 2B, 3C...):")
    
    # 4. Upload ảnh
    uploaded_files = st.file_uploader("Chọn nhiều ảnh phiếu bài làm:", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    
    # 5. Nút xử lý
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Chấm tất cả ảnh đã chọn"):
            if not dap_an or not uploaded_files:
                st.warning("Vui lòng nhập đáp án và chọn ảnh.")
            else:
                model = get_model(model_choice)
                for file in uploaded_files:
                    with st.spinner(f"Đang chấm: {file.name}..."):
                        try:
                            img = Image.open(file)
                            prompt = f"""
                            Bạn là giáo viên. Đối chiếu phiếu trắc nghiệm này với đáp án: {dap_an}.
                            Trả về kết quả DUY NHẤT dưới định dạng JSON:
                            {{"ten_file": "{file.name}", "so_cau_dung": 0, "tong_so_cau": 0, "diem": 0.0, "nhan_xet": "..."}}
                            """
                            response = model.generate_content([prompt, img])
                            res_text = response.text.replace('```json', '').replace('```', '')
                            ket_qua = json.loads(res_text)
                            st.session_state.ket_qua_cham.append(ket_qua)
                        except Exception as e:
                            st.error(f"Lỗi chấm file {file.name}: {e}")
                st.success("Đã chấm xong tất cả!")

    with col2:
        if st.button("🗑️ Xóa danh sách"):
            st.session_state.ket_qua_cham = []
            st.rerun()

    # 6. Bảng kết quả và Excel
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
