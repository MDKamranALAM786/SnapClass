import streamlit as st

from src.pages.home import home_page
from src.pages.teacher import teacher_page
from src.pages.student import student_page

def main() :
    if "login_type" not in st.session_state :
        st.session_state["login_type"] = None

    match st.session_state["login_type"] :
        case "teacher" :
            teacher_page()
        case "student" :
            student_page()
        case None :
            home_page()

main()
