import streamlit as st
import time

from src.components.dialogue import create_subject, share_subject
from src.components.header import header_dashboard
from src.components.subject_card import subject_card
from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.db.controllers.teacher import register_teacher, login_teacher
from src.db.controllers.subject import get_all_subjects

def teacher_page() :
    # styles
    style_background_dashboard()
    style_base_layout()

    # display login/register portal
    if "teacher_data" in st.session_state :
        teacher_dashboard()
    elif "teacher_auth_type" not in st.session_state or st.session_state["teacher_auth_type"] == "login" :
        login_screen()
    else :
        register_screen()

def teacher_dashboard() :
    teacher = st.session_state["teacher_data"]

    # header
    col1, col2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with col1 :
        header_dashboard()
    with col2 :
        st.subheader(f"Welcome, {teacher["name"]}")
        if st.button("Logout", type="secondary", shortcut="control+backspace") :
            st.session_state["is_logged_in"] = False
            del st.session_state.teacher_data
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state :
        st.session_state["current_teacher_tab"] = "take_attendance"

    # tabs for teacher
    tab1, tab2, tab3 = st.columns(3)
    with tab1 :
        type1 = "primary" if st.session_state["current_teacher_tab"] == "take_attendance" else "tertiary"
        if st.button("Take Attendance", type=type1, width="stretch", icon=":material/ar_on_you:") :
            st.session_state["current_teacher_tab"] = "take_attendance"
            st.rerun()
    with tab2 :
        type2 = "primary" if st.session_state["current_teacher_tab"] == "manage_subjects" else "tertiary"
        if st.button("Manage Subjects", type=type2, width="stretch", icon=":material/book_ribbon:") :
            st.session_state["current_teacher_tab"] = "manage_subjects"
            st.rerun()
    with tab3 :
        type3 = "primary" if st.session_state["current_teacher_tab"] == "attendance_records" else "tertiary"
        if st.button("Attendance Records", type=type3, width="stretch", icon=":material/cards_stack:") :
            st.session_state["current_teacher_tab"] = "attendance_records"
            st.rerun()

    st.divider()

    # contents to be displayed under each tab
    if st.session_state["current_teacher_tab"] == "take_attendance" :
        take_attendance(teacher)
    elif st.session_state["current_teacher_tab"] == "manage_subjects" :
        manage_subjects(teacher)
    elif st.session_state["current_teacher_tab"] == "attendance_records" :
        attendance_records(teacher)

def take_attendance(teacher) :
    st.subheader("Take Attendance")

def manage_subjects(teacher) :
    id = teacher["teacher_id"]

    col1, col2 = st.columns(2)
    with col1 :
        st.subheader("Manage Subjects", width="stretch")
    with col2 :
        if st.button("Create New Subject", width="stretch") :
            create_subject(id)

    # List all subjects
    subjects = get_all_subjects(id)
    if not subjects :
        st.info("No subjects. Create one")
    else :
        for subject in subjects :
            stats = [("👥", "Students", subject["total_students"]), ("🕰", "Classes", subject["total_classes"])]

            def share_btn() :
                if st.button(f"Share Code : {subject["name"]}", key=f"share_{subject["subject_code"]}", icon=":material/share:") :
                    share_subject(subject["name"], subject["subject_code"])
                st.space()

            subject_card(name=subject["name"], code=subject["subject_code"], section=subject["section"], stats=stats, footer_callback=share_btn)

def attendance_records(teacher) :
    st.subheader("Attendance Records")

def register_screen() :
    # header
    col1, col2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with col1 :
        header_dashboard()
    with col2 :
        if st.button("Go Back to Home", type="secondary", key="loginbackbtn", shortcut="control+backspace") :
            st.session_state["login_type"] = None
            st.rerun()

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
    # header
    col1, col2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with col1 :
        header_dashboard()
    with col2 :
        if st.button("Go Back to Home", type="secondary", key="loginbackbtn", shortcut="control+backspace") :
            st.session_state["login_type"] = None
            st.rerun()

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

