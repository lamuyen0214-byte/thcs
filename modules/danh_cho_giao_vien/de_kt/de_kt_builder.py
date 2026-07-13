import streamlit as st
import sys, os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
if root_dir not in sys.path: sys.path.append(root_dir)
from ai_config import run_ai_with_fallback

def render_de_kt_module():
    # ... (Giữ nguyên toàn bộ giao diện của thầy) ...
    if st.button("🚀 KHỞI TẠO ĐỀ KIỂM TRA", type="primary", use_container_width=True):
        prompt = f"Soạn đề kiểm tra môn {mon_hoc} lớp {lop} với cấu trúc {cau_truc}..."
        with st.spinner("AI đang soạn đề..."):
            result, success = run_ai_with_fallback(prompt, model_display_name)
            if success:
                st.session_state['current_de_kt'] = result
                st.rerun()
            else: st.error(result)
