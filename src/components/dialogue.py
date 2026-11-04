import streamlit as st
import segno
import io
import time

from src.db.controllers.student import is_student_enrolled, enroll_student_into_subject
from src.db.controllers.subject import create_new_subject, get_subject

@st.dialog("Create New Subject")
def create_subject(id) :
    st.write("Enter the details of new subject")

    sub_code = st.text_input("Subject Code", placeholder="CS101")
    sub_name = st.text_input("Subject Name", placeholder="Intoduction to Python")
    sub_section = st.text_input("Subject Section", placeholder="A")

    if st.button("Create Subject", type="primary", width="stretch") :
        if sub_code and sub_name and sub_section :
            response = create_new_subject(sub_code, sub_name, sub_section, id)
            if not response :
                st.warning("Something went wrong!")
            else :
                st.success("Created Subject")
        else :
            st.warning("All fields are required")

@st.dialog("Share Class Link")
def share_subject(sub_name, sub_code) :
    app_domain = st.secrets["APP_DOMAIN"]
    url = f"{app_domain}/?join-code={sub_code}"

    st.header("Scan to Join")

    qr = segno.make(url)
    out = io.BytesIO()
    qr.save(out, kind="png", scale=10, border=1)

    col1, col2 = st.columns(2)
    with col1 :
        st.markdown("### Copy Link")
        st.code(url, language="text")
        st.code(sub_code, language="text")
        st.info("Copy link to share")
    with col2 :
        st.markdown("### Scan to join")
        st.image(out.getvalue(), caption="QRCODE to join class")

@st.dialog("Enroll in Subject")
def enroll_subject(student) :
    st.write("Enter the subject code")
    join_code = st.text_input("Subject Code", placeholder="CS101")

    if st.button("Enroll Now", type="primary", width="stretch") :
        if not join_code :
            st.warning("Enter a subject code")
        else :
            subject = get_subject(join_code)
            if subject :
                student_id = student["student_id"]
                subject_id = subject["subject_id"]
                if is_student_enrolled(student_id, subject_id) :
                    st.warning("You are already enrolled in this subject")
                else :
                    response = enroll_student_into_subject(student_id, subject_id)
                    if response :
                        st.success("Successfully Enrolled!")
                        time.sleep(1)
                        st.rerun()
                    else :
                        st.warning("Something went wrong!\nCannot enroll into subject")

@st.dialog("Quick Enrollment")
def auto_enrollment(subject_code) :
    student = st.session_state["student_data"]
    student_id = student["student_id"]

    subject = get_subject(subject_code)
    if not subject :
        st.error("Subject doesn't exists")
        if st.button("Close") :
            st.query_params.clear()
            st.rerun()
        return

    subject_id = subject["subject_id"]
    if is_student_enrolled(student_id, subject_id) :
        st.info("You are already enrolled!")
        if st.button("Close") :
            st.query_params.clear()
            st.rerun()
        return

    st.markdown("Click Enter to enroll.")
    col1, col2 = st.columns(2)
    with col1 :
        if st.button("Go Back", type="tertiary") :
            st.query_params.clear()
            st.rerun()
    with col2 :
        if st.button("Enter", type="primary", width="stretch") :
            response = enroll_student_into_subject(student_id, subject_id)
            if response :
                st.success("Enrollment Successfull!")
                st.query_params.clear()
                time.sleep(1)
                st.rerun()
            else :
                st.warning("Something went wrong!\nCannot enroll")

