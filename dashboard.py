import streamlit as st
import requests
import pandas as pd

API_URL = "https://task-project-management-rest-api.onrender.com"

st.set_page_config(page_title="Task Manager", layout="wide")


# ── Auth helpers ──────────────────────────────────────────────────────────────

def login(email: str, password: str) -> str | None:
    try:
        resp = requests.post(
            f"{API_URL}/auth/login",
            data={"username": email, "password": password},
            timeout=10,
        )
        if resp.status_code == 200:
            return resp.json()["access_token"]
        st.error(resp.json().get("detail", "Login failed"))
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
    return None


def auth_headers() -> dict:
    return {"Authorization": f"Bearer {st.session_state.token}"}


def fetch(endpoint: str) -> list:
    try:
        resp = requests.get(f"{API_URL}{endpoint}", headers=auth_headers(), timeout=10)
        if resp.status_code == 401:
            st.warning("Session expired. Please log in again.")
            st.session_state.token = None
            st.rerun()
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else [data]
    except requests.exceptions.RequestException as e:
        st.error(f"API error: {e}")
        return []


def post(endpoint: str, payload: dict) -> dict | None:
    try:
        resp = requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            headers=auth_headers(),
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        detail = e.response.json().get("detail", str(e))
        st.error(f"Error: {detail}")
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
    return None


def delete(endpoint: str) -> bool:
    try:
        resp = requests.delete(f"{API_URL}{endpoint}", headers=auth_headers(), timeout=10)
        return resp.status_code == 204
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return False


# ── Login screen ─────────────────────────────────────────────────────────────

if "token" not in st.session_state:
    st.session_state.token = None

if not st.session_state.token:
    st.title("Task Manager — Login")
    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            token = login(email, password)
            if token:
                st.session_state.token = token
                st.rerun()

    with tab_register:
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Register"):
            try:
                resp = requests.post(f"{API_URL}/auth/register", json={
                    "email": reg_email, "password": reg_password
                }, timeout=10)
                if resp.status_code == 201:
                    st.success("Registered! You can now log in.")
                else:
                    st.error(resp.json().get("detail", "Registration failed"))
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")
    st.stop()


# ── Authenticated app ─────────────────────────────────────────────────────────

with st.sidebar:
    st.title("Task Manager")
    menu = st.selectbox("Navigate", ["Dashboard", "Users", "Projects", "Tasks"])
    if st.button("Logout"):
        st.session_state.token = None
        st.rerun()

# Dashboard
if menu == "Dashboard":
    st.header("Overview")
    col1, col2, col3 = st.columns(3)

    users = fetch("/users/")
    projects = fetch("/projects/")
    tasks = fetch("/tasks/")

    col1.metric("Users", len(users))
    col2.metric("Projects", len(projects))
    col3.metric("Tasks", len(tasks))

    if tasks:
        df = pd.DataFrame(tasks)
        if "status" in df.columns:
            st.subheader("Tasks by Status")
            st.bar_chart(df["status"].value_counts())

# Users
elif menu == "Users":
    st.header("Users")
    users = fetch("/users/")
    if users:
        st.dataframe(pd.DataFrame(users), use_container_width=True)
    else:
        st.info("No users found or insufficient permissions.")

# Projects
elif menu == "Projects":
    st.header("Projects")

    with st.expander("Create Project"):
        name = st.text_input("Project Name")
        description = st.text_area("Description")
        if st.button("Create Project"):
            if not name.strip():
                st.warning("Project name is required.")
            else:
                result = post("/projects/", {"name": name, "description": description})
                if result:
                    st.success(f"Project '{result['name']}' created.")
                    st.rerun()

    projects = fetch("/projects/")
    if projects:
        df = pd.DataFrame(projects)
        st.dataframe(df, use_container_width=True)

        st.subheader("Delete Project")
        project_options = {p["name"]: p["id"] for p in projects}
        selected = st.selectbox("Select project to delete", list(project_options.keys()))
        if st.button("Delete Selected Project"):
            if delete(f"/projects/{project_options[selected]}"):
                st.success(f"Deleted '{selected}'")
                st.rerun()
    else:
        st.info("No projects found.")

# Tasks
elif menu == "Tasks":
    st.header("Tasks")

    projects = fetch("/projects/")
    project_map = {p["name"]: p["id"] for p in projects}

    with st.expander("Create Task"):
        title = st.text_input("Title")
        description = st.text_area("Description", key="task_desc")
        status = st.selectbox("Status", ["todo", "in_progress", "done"])
        priority = st.selectbox("Priority", ["low", "medium", "high"])
        project_name = st.selectbox("Project", list(project_map.keys()) or ["No projects"])
        if st.button("Create Task"):
            if not title.strip():
                st.warning("Title is required.")
            elif not project_map:
                st.warning("Create a project first.")
            else:
                result = post("/tasks/", {
                    "title": title,
                    "description": description,
                    "status": status,
                    "priority": priority,
                    "project_id": project_map[project_name],
                })
                if result:
                    st.success(f"Task '{result['title']}' created.")
                    st.rerun()

    tasks = fetch("/tasks/")
    if tasks:
        df = pd.DataFrame(tasks)
        col_filter, col_sort = st.columns(2)
        with col_filter:
            status_filter = st.multiselect("Filter by status", ["todo", "in_progress", "done"])
        with col_sort:
            sort_col = st.selectbox("Sort by", ["created_at", "priority", "status", "title"])

        if status_filter:
            df = df[df["status"].isin(status_filter)]
        df = df.sort_values(sort_col, ascending=True)

        st.dataframe(df, use_container_width=True)
    else:
        st.info("No tasks found.")
