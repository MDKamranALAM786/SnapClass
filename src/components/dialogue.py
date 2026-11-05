import segno
import io
import time
import pandas as pd
import streamlit as st
from PIL import Image
from datetime import datetime

from src.db.controllers.student import is_student_enrolled, enroll_student_into_subject
from src.db.controllers.subject import create_new_subject, get_subject, upload_attendance, get_subject_enrolled_students

from src.pipelines.voice_pipeline import process_bulk_audio

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
    app_domain = "snapclass-main.streamlit.app"
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

@st.dialog("Capture or Upload Photos")
def add_photos() :
    st.write("Add classroom photos to scan")

    if "photo_tab" not in st.session_state :
        st.session_state["photo_tab"] = "camera"

    col1, col2 = st.columns(2)
    with col1 :
        type_camera = "primary" if st.session_state.get("photo_tab") == "camera" else "tertiary"
        if st.button("Camera", type=type_camera, width="stretch") :
            st.session_state["photo_tab"] = "camera"
    with col2 :
        type_upload = "primary" if st.session_state.get("photo_tab") == "upload" else "tertiary"
        if st.button("Upload Photos", type=type_upload, width="stretch") :
            st.session_state["photo_tab"] = "upload"

    if st.session_state.get("photo_tab") == "camera" :
        captured_photo = st.camera_input("Take class photo", key="dialog_cam")
        if captured_photo :
            st.session_state.attendance_images.append(Image.open(captured_photo))
            st.toast("Photo Captured!")
            st.rerun()
    else :
        uploaded_photos = st.file_uploader("Choose images", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key="dialog_upload")
        if uploaded_photos :
            for photo in uploaded_photos :
                st.session_state.attendance_images.append(Image.open(photo))
            st.toast("Photos Uploaded!")
            st.rerun()

    st.divider()

    if st.button("Done", type="secondary", width="stretch") :
        st.rerun()

@st.dialog("Attendance Result")
def show_attendance_results(result_df, attendance_to_log) :
    attendance_result(result_df, attendance_to_log)

def attendance_result(result_df, attendance_to_log) :
    st.write("Please review attendace before updating")
    st.dataframe(result_df, hide_index=True, width="stretch")

    col1, col2 = st.columns(2)
    with col1 :
        if st.button("Discard Attendance", type="tertiary", width="stretch") :
            st.session_state.attendance_images = []
            st.session_state.voice_attendance_results = None
            st.rerun()
    with col2 :
        if st.button("Upload Attendance", type="primary", width="stretch") :
            if upload_attendance(attendance_to_log) :
                st.toast("Attendance Uploaded!")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            else :
                st.error("Something went wrong.\nCound not upload attendace")

@st.dialog("Voice Attendance")
def voice_attendance(selected_subject_id) :
    audio_data = None

    st.write("Record student audio")
    audio_data = st.audio_input("Record audio")

    if st.button("Analyze Audio", width="stretch", type="primary") :
        with st.spinner("Processing Audio...") :
            enrolled_students = get_subject_enrolled_students(selected_subject_id)
            if not enrolled_students :
                st.warning("No students are enrolled!")
                return

            student_dict = {enrolled_student["students"]["student_id"] : enrolled_student["students"]["voice_embedding"] for enrolled_student in enrolled_students if enrolled_student["students"].get("voice_embedding")}
            if not student_dict :
                st.error("No students have submitted their voice profiles!")
                return

            detected_student_ids = process_bulk_audio(audio_data.read(), student_dict)

            results, attendance_to_log = [], []
            current_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for enrolled_student in enrolled_students :
                student = enrolled_student["students"]
                student_id = student["student_id"]

                score = detected_student_ids.get(student_id, -1)
                is_present = bool(score != -1)

                results.append({
                    "Name" : student["name"],
                    "ID" : student_id,
                    "Score" : score if is_present else "-",
                    "Status" : is_present
                })

                attendance_to_log.append({
                    "subject_id" : selected_subject_id,
                    "student_id" : student_id,
                    "time" : current_datetime,
                    "is_present" : is_present
                })

            st.session_state["voice_attendance_results"] = (results, attendance_to_log)

    if st.session_state.get("voice_attendance_results") :
        st.divider()
        results, attendance_to_log = st.session_state.get("voice_attendance_results")
        attendance_result(pd.DataFrame(results), attendance_to_log)

