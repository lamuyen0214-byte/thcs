import streamlit as st
# Import hàm quản lý tổ từ module chuyên trách
from modules.management.org_manager import render_org_management

def render_module():
    """Hàm này được app.py gọi để hiển thị nội dung"""
    st.header("📊 Phân hệ: Quản lý Tổ chuyên môn")
    # Gọi hàm render từ module management
    render_org_management()
