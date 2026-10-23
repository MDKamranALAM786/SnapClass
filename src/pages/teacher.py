import streamlit as st
import time

from src.components.header import header_dashboard
from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.db.controllers.teacher import register_teacher, login_teacher

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
    if "teacher_data" in st.session_state :
        teacher_dashboard()
    elif "teacher_auth_type" not in st.session_state or st.session_state["teacher_auth_type"] == "login" :
        login_screen()
    else :
        register_screen()

def teacher_dashboard() :
    teacher = st.session_state["teacher_data"]
    name = teacher["name"]
    username = teacher["username"]
    st.header(f"""
        Welcome {name}
    """)

def register_screen() :
    # register header
    st.header("Register your teacher profile", text_alignment="center")
    st.space()
    st.space()

    name = st.text_input("Name", placeholder="enter full name")
    username = st.text_input("Enter username", placeholder="kawwa")
    password = st.text_input("Enter Password", placeholder="enter password", type="password")
    pass_confirm = st.text_input("Re-enter password", placeholder="re-enter password", type="password")

    st.divider()

    btn1, btn2 = st.columns(2)
    with btn1 :   # register button
        if st.button("Register", icon=":material/passkey:", shortcut="control+enter", width="stretch") :
            success, message = register(name, username, password, pass_confirm)
            if success :
                st.success(message)
                time.sleep(2)
                st.session_state["teacher_auth_type"] = "login"
                st.rerun()
            else :
                st.error(message)
    with btn2 :   # go to login button
        if st.button("Login Instead", type="primary", icon=":material/passkey:", width="stretch") :
            st.session_state["teacher_auth_type"] = "login"
            st.rerun()

def register(name, username, password, pass_confirm) :
    if not name or not username or not password or not pass_confirm :
        return False, "Enter all fields!"

    if password != pass_confirm :
        return False, "Password doesn't match!"

    message, response = register_teacher(name, username, password)
    if response :
        print(response)
        return True, message
    else :
        return False, message

def login_screen() :
    # login header
    st.header("Login using password", text_alignment="center")
    st.space()
    st.space()

    username = st.text_input("Enter username", placeholder="kawwa")
    password = st.text_input("Enter password", placeholder="password", type="password")

    st.divider()

    btn1, btn2 = st.columns(2)
    with btn1 :   # login button
        if st.button("Login", icon=":material/passkey:", shortcut="control+enter", width="stretch") :
            success, message = login(username, password)
            if success :
                st.toast(message)
                time.sleep(2)
                st.rerun()
            else :
                st.error(message)
    with btn2 :   # go to register button
        if st.button("Register Instead", type="primary", icon=":material/passkey:", width="stretch") :
            st.session_state["teacher_auth_type"] = "register"
            st.rerun()

def login(username, password) :
    if not username or not password :
        return False, "Enter all fields!"

    message, teacher = login_teacher(username, password)
    if teacher :
        st.session_state["role"] = "teacher"
        st.session_state["teacher_data"] = teacher
        st.session_state["is_logged_in"] = True

        print(teacher)
        return True, message
    else :
        return False, message

