import streamlit as st


def Navbar():
    with st.sidebar:
        st.page_link("streamlit_app.py", label="首页")
        st.page_link("pages/bh3.py", label="崩坏3")
        st.page_link("pages/hk4e.py", label="原神")
        st.page_link("pages/hkrpg.py", label="崩坏：星穹铁道")
