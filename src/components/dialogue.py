import streamlit as st

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

