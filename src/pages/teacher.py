import streamlit as st

from src.components.home_header import header_dashboard
from src.ui.base_layout import style_background_dashboard, style_base_layout

def teacher_page() :
    # styles
    style_background_dashboard()
    style_base_layout()

    # header
    col1, col2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with col1 :
        header_dashboard()
    with col2 :
        if st.button("Go Back to Home", type="secondary", key="loginbackbtn", shortcut="control+backspace") :
            st.session_state["login_type"] = None
            st.rerun()

    # display login/register portal
    if "teacher_auth_type" not in st.session_state or st.session_state["teacher_auth_type"] == "login" :
        login_screen()
    else :
        register_screen()

def login_screen() :
    st.header("Login using password", text_alignment="center")

    st.space()
    st.space()

    st.text_input("Enter username", placeholder="kawwa")
    st.text_input("Enter password", placeholder="password", type="password")

    st.divider()

    btn1, btn2 = st.columns(2)
    with btn1 :
        st.button("Login", icon=":material/passkey:", shortcut="control+enter", width="stretch")
    with btn2 :
        if st.button("Register Instead", type="primary", icon=":material/passkey:", width="stretch") :
            st.session_state["teacher_auth_type"] = "register"
            st.rerun()

def register_screen() :
    # register header
    st.header("Register your teacher profile", text_alignment="center")
    st.space()
    st.space()

    st.text_input("Name", placeholder="enter full name")
    st.text_input("Enter username", placeholder="kawwa")
    st.text_input("Enter Email", placeholder="kawwa@gmail.com", type="email")
    st.text_input("Enter Password", placeholder="enter password", type="password")
    st.text_input("Re-enter password", placeholder="re-enter password", type="password")

    st.divider()

    btn1, btn2 = st.columns(2)
    with btn1 :
        st.button("Register", icon=":material/passkey:", shortcut="control+enter", width="stretch")
    with btn2 :
        if st.button("Login Instead", type="primary", icon=":material/passkey:", width="stretch") :
            st.session_state["teacher_auth_type"] = "login"
            st.rerun()

