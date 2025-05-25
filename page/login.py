# page/login.py

import streamlit as st
from src.db import check_user_credentials

def login():
    st.title("🔐 Halaman Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if check_user_credentials(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success("✅ Login berhasil!")
            st.rerun()
        else:
            st.error("❌ Username atau password salah.")
