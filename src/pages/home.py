import streamlit as st

from src.components.header import header_home
from src.ui.base_layout import style_background_home, style_base_layout

def home_page() :
    header_home()
    style_background_home()
    style_base_layout()

    col1, col2 = st.columns(2, gap="large")

    with col1 :
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button("Stuent Page", key="Student", type="primary") :
            print("Redirecting to Student Page")
            st.session_state["login_type"] = "student"
            st.rerun()

    with col2 :
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)
        if st.button("Teacher Page", key="Teacher", type="primary") :
            print("Redirected to Teacher Page")
            st.session_state["login_type"] = "teacher"
            st.rerun()

