import time
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime

from src.components.dialogue import create_subject, share_subject, add_photos, show_attendance_results, voice_attendance
from src.components.header import header_dashboard
from src.components.subject_card import subject_card
from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.db.controllers.teacher import register_teacher, login_teacher, get_attendance_for_teacher
from src.db.controllers.subject import get_all_subjects, get_subject_enrolled_students

from src.pipelines.face_pipeline import predict_attendance

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
    teacher_id = teacher["teacher_id"]
    st.subheader("Take Attendance")

    if "attendance_images" not in st.session_state :
        st.session_state["attendance_images"] = []

    subjects = get_all_subjects(teacher_id)
    if not subjects :
        st.warning("No Subjects Found!")
        return

    subject_options = {f"{subject["name"]} - {subject["subject_code"]}" : f"{subject["subject_id"]}" for subject in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    with col1 :
        selected_subject_label = st.selectbox("Select Subjects", options=list(subject_options.keys()))
    with col2 :
        if st.button("Add Photos", type="primary", width="stretch") :
            add_photos()

    st.divider()

    selected_subject_id = subject_options[selected_subject_label]

    if st.session_state.attendance_images :
        st.header("Add Photos")

        gallery_cols = st.columns(4)
        for i, img in enumerate(st.session_state.attendance_images) :
            with gallery_cols[i % 4] :
                st.image(img, width="stretch", caption=f"Photo {i+1}")

    c1, c2, c3 = st.columns(3)
    with c1 :
        if st.button("Clear all images", width="stretch", type="tertiary", icon=":material/delete:") :
            st.session_state.attendance_images = []
            st.rerun()
    with c2 :
        has_photos = bool(st.session_state.attendance_images)
        if st.button("Run Face Analysis", width="stretch", type="secondary", icon=":material/analytics:", disabled=not has_photos) :
            with st.spinner("Deep student photos...") :
                print("\nScanning student photos")
                detected_student_ids = {}

                for i, img in enumerate(st.session_state.attendance_images) :
                    img_np = np.array(img.convert("RGB"))
                    present_student_ids, _, _ = predict_attendance(img_np)

                    if present_student_ids :
                        for i, student_id in enumerate(present_student_ids) :
                            detected_student_ids.setdefault(student_id, []).append(f"Photo {i+1}")

                enrolled_students = get_subject_enrolled_students(selected_subject_id)
                if not enrolled_students :
                    st.warning("No students are enrolled!")
                else :
                    results, attendance_to_log = [], []
                    current_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for enrolled_student in enrolled_students :
                        student = enrolled_student["students"]
                        student_id = student["student_id"]

                        photo_sources = detected_student_ids.get(student_id, [])
                        is_present = len(photo_sources) != 0

                        results.append({
                            "Name" : student["name"],
                            "ID" : student_id,
                            "Sources" : ", ".join(photo_sources) if is_present else "-",
                            "Status" : is_present
                        })

                        attendance_to_log.append({
                            "subject_id" : selected_subject_id,
                            "student_id" : student_id,
                            "time" : current_datetime,
                            "is_present" : is_present
                        })

                show_attendance_results(pd.DataFrame(results), attendance_to_log)
    with c3 :
        if st.button("Use Voice Attendance", type="primary", width="stretch", icon=":material/mic:") :
            voice_attendance(selected_subject_id)

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

    teacher_id = teacher["teacher_id"]
    teacher_attendances = get_attendance_for_teacher(teacher_id)

    if not teacher_attendances :
        st.info("No records to show!")
        return

    data = []
    for record in teacher_attendances :
        timestamp = record["time"]

        data.append({
            "time_group" : timestamp.split(".")[0] if timestamp else None,
            "Time" : datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %I:%M %p") if timestamp else "N/A",
            "Subject" : record["subjects"]["name"],
            "Subject Code" : record["subjects"]["subject_code"],
            "Is Present" : bool(record.get("is_present", False))
        })

    df = pd.DataFrame(data)
    summary = (
        df.groupby(["time_group", "Time", "Subject", "Subject Code"])
        .agg(
            Present_Count = ("Is Present", "sum"),
            Total_Count = ("Is Present", "count")
        ).reset_index()
    )

    summary["Attendance Stats"] = (summary["Present_Count"].astype("str") + " / " + summary["Total_Count"].astype("str"))

    display_df = summary.sort_values(by="time_group", ascending=False)[["Time", "Subject", "Subject Code", "Attendance Stats"]]
    st.dataframe(display_df, width="stretch", hide_index=True)

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
                time.sleep(1)
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
                time.sleep(1)
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

