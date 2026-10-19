import streamlit as st

from src.components.home_header import header_home
from src.ui.base_layout import style_background_home, style_base_layout

def home_page() :
    header_home()
    style_background_home()
    style_base_layout()

    col1, col2 = st.columns(2)

    with col1 :
        if st.button("Teacher Page", key="Teacher") :
            print("Redirected to Teacher Page")
            st.session_state["login_type"] = "teacher"
            st.rerun()

    with col2 :
        if st.button("Stuent Page", key="Student") :
            print("Redirecting to Student Page")
            st.session_state["login_type"] = "student"
            st.rerun()

