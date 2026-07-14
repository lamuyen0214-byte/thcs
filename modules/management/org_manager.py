import streamlit as st

def render_org_management():
    st.success("Test: Hàm render_org_management đã chạy thành công!")
    tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
    with tab1:
        st.write("Nội dung tab 1 đã hiển thị!")
    with tab2:
        st.write("Nội dung tab 2 đã hiển thị!")
