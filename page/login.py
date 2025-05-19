# src/login.py

import streamlit as st

USER_CREDENTIALS = {
    "admin": "admin123",
    "user": "user123"
}

def login():
    st.title("🔐 Halaman Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.success("✅ Login berhasil!")
            st.rerun()
        else:
            st.error("❌ Username atau password salah.")
