import streamlit as st

USERS = {"admin": "1234", "user": "pass"}

def login():
    st.sidebar.subheader("Login")

    u = st.sidebar.text_input("Username")
    p = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if USERS.get(u) == p:
            st.session_state["user"] = u
            st.sidebar.success("Logged in")
        else:
            st.sidebar.error("Invalid")

def check():
    return st.session_state.get("user")
