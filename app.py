import streamlit as st

from src.components.dialogue import auto_enrollment

from src.pages.home import home_page
from src.pages.teacher import teacher_page
from src.pages.student import student_page

def main() :
    st.set_page_config(
        page_title="Snap Class",
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png"
    )

    if "login_type" not in st.session_state :
        st.session_state["login_type"] = None

    match st.session_state["login_type"] :
        case "teacher" :
            teacher_page()
        case "student" :
            student_page()
        case None :
            home_page()

    join_code = st.query_params.get("join-code")
    if join_code :
        if st.session_state["login_type"] != "student" :
            st.session_state["login_type"] = "student"
            st.rerun()

        if st.session_state.get("is_logged_in") and st.session_state.get("role") == "student" :
            auto_enrollment(join_code)

main()

