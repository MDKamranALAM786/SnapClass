import streamlit as st
import numpy as np
from PIL import Image

from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.pipelines.face_recognition import get_face_embeddings

def student_page() :
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

    st.header("Login using Face ID", text_alignment="center")
    st.space()
    st.space()

    photo_captured = st.camera_input("Position your face in the center")
    if photo_captured :
        face_np = np.array(Image.open(photo_captured))
        get_face_embeddings(face_np)

