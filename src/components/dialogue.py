import streamlit as st
import segno
import io

from src.db.controllers.subject import create_new_subject

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
    app_domain = "http://localhost:8501"
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

