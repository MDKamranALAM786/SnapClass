import streamlit as st
import numpy as np
import time
from PIL import Image

from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.db.controllers.student import get_student, register_student

from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_model
from src.pipelines.voice_pipeline import get_voice_embeddings

def student_page() :
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state :
        student_dashboard(st.session_state["student_data"])
        return

    show_registration = False

    # header
    col1, col2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with col1 :
        header_dashboard()
    with col2 :
        if st.button("Go Back to Home", type="secondary", key="loginbackbtn", shortcut="control+backspace") :
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Login using Face ID", text_alignment="center")
    st.space()
    st.space()

    photo_captured = st.camera_input("Position your face in the center")
    if photo_captured :
        face_np = np.array(Image.open(photo_captured))

        with st.spinner("AI is scanning...") :
            detections, student_ids, total_embeddings = predict_attendance(face_np)
            if total_embeddings == 0 :
                st.warning("No faces detected!")
            elif total_embeddings != 1 :
                st.warning("Too many faces!")
            else :
                if detections :
                    stud_predicted = list(detections)[0]
                    student = get_student(stud_predicted)
                    if student :
                        st.session_state["role"] = "student"
                        st.session_state["student_data"] = student
                        st.session_state["is_logged_in"] = True
                        st.toast("Login Successful!")
                        time.sleep(2)
                        st.rerun()
                else :
                    st.info("Face not recognised. New Student?")
                    show_registration = True

    if show_registration :
        with st.container(border=True) :
            st.header("Register New Profile!")
            new_name = st.text_input("Enter your name", placeholder="Kamran")

            st.subheader("Optional : Voice Enrollment")
            st.info("Enroll for voice attendance")

            audio_data = None
            try :
                audio_data = st.audio_input("Record a short phrase. Eg: I am a student!")
            except Exception as err :
                print("Error in enrolling for voice attendance :", err)

            if st.button("Create Account", type="primary") :
                if not new_name :
                    st.warning("Please enter your name.")
                else :
                    with st.spinner("Creating profile...") :
                        face_np = np.array(Image.open(photo_captured))
                        face_embedding = get_face_embeddings(face_np)
                        if not face_embedding :
                            st.warning("Coundnt capture facial features!")
                        else :
                            face_embedding = face_embedding[0].tolist()

                            voice_embedding = None
                            if audio_data :
                                voice_embedding = get_voice_embeddings(audio_data.read())

                            student = register_student(new_name, face_embedding, voice_embedding)
                            if not student :
                                print("Registration Unsuccessful!")
                            else :
                                train_model()
                                st.session_state["role"] = "student"
                                st.session_state["student_data"] = student
                                st.session_state["is_logged_in"] = True
                                st.toast("Registration Successful!")
                                time.sleep(2)
                                st.rerun()

def student_dashboard(data) :
    st.header(f"Welcome to Dashboard {data["name"]}!")

