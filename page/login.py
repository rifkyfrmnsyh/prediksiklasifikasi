from src.db import check_user_credentials
import streamlit as st

def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = check_user_credentials(username, password)
        if role:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = role 
            st.success("Login berhasil!")
            st.rerun()
        else:
            st.error("Username atau password tidak ditemukan.")
