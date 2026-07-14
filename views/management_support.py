import streamlit as st
from modules.management.org_manager import render_org_management

def render_management_view():
    st.header("📊 Phân hệ: Quản lý Tổ chuyên môn")
    # Gọi hàm render đã thiết kế ở Bước 1
    render_org_management()
