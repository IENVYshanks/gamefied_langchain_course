import streamlit as st 

st.title("Welcome to Gamefied Agentic AI")

with st.form("user_form"):

    name = st.text_input("Enter your name")
    email = st.text_input("Enter your email")
    submit_button = st.form_submit_button("Submit")


if submit_button:
    st.write(f"Hello {name}! Your email {email} has been received.")
    