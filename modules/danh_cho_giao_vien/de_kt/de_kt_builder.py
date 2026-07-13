import streamlit as st
import sys, os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
if root_dir not in sys.path: sys.path.append(root_dir)
from ai_config import run_ai_with_fallback

def render_de_kt_module():
    st.markdown("""<style>.header-blue {color: #0000FF; font-weight: bold;}</style>""", unsafe_allow_html=True)
    st.markdown("### 📝 Trình tạo Đề kiểm tra")
    
    col1, col2 = st.columns(2)
    with col1:
        mon_hoc = st.selectbox("Môn học", ["Toán", "Vật lý", "Hóa học", "Sinh học", "Ngữ văn"])
        lop = st.selectbox("Khối lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"])
    with col2:
        cau_truc = st.text_input("Cấu trúc đề", "Trắc nghiệm 70% - Tự luận 30%")
        model_display_name = st.selectbox("Model", ["3.1 Flash-Lite", "3.5 Flash", "3.1 Pro"])

    noi_dung = st.text_area("Nội dung trọng tâm")

    if st.button("🚀 KHỞI TẠO ĐỀ KIỂM TRA", type="primary", use_container_width=True):
        prompt = f"Soạn đề kiểm tra môn {mon_hoc} lớp {lop}, cấu trúc {cau_truc}. Nội dung: {noi_dung}"
        with st.spinner("AI đang soạn đề..."):
            result, success = run_ai_with_fallback(prompt, model_display_name)
            if success:
                st.session_state['current_de_kt'] = result
                st.success("✅ Thành công!")
                st.rerun()
            else: st.error(result)
            
    if 'current_de_kt' in st.session_state:
        st.markdown(st.session_state['current_de_kt'])
