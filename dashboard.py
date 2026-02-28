import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}{endpoint}")
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict):
            data = [data]

        return data
    except Exception as e:
        st.error(f"API error: {e}")
        return []

st.title("Task Management Dashboard")

menu = st.sidebar.selectbox("Navigation", ["Dashboard","Users","Projects","Tasks"])

if menu == "Dashboard":
    users = fetch_data("/users/")
    projects = fetch_data("/projects/")
    tasks = fetch_data("/tasks/")

    col1, col2, col3 = st.columns(3)
    col1.metric("Users", len(users))
    col2.metric("Projects", len(projects))
    col3.metric("Tasks", len(tasks))

elif menu == "Users":
    users = fetch_data("/users/")
    if users:
        st.dataframe(pd.DataFrame(users))

elif menu == "Projects":
    st.subheader("Create Project")

    name = st.text_input("Project Name")
    description = st.text_area("Description")

    if st.button("Create"):
        requests.post(f"{API_URL}/projects/", json={
            "name": name,
            "description": description
        })
        st.success("Project created")

    projects = fetch_data("/projects/")
    if projects:
        st.dataframe(pd.DataFrame(projects))

elif menu == "Tasks":
    tasks = fetch_data("/tasks/")
    if tasks:
        st.dataframe(pd.DataFrame(tasks))
