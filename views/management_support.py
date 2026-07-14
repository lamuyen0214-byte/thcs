import streamlit as st
from modules.management.org_manager import render_org_management
def render_management_view():
    # Không cần header thừa nếu tab đã rõ ràng
    render_org_management()
