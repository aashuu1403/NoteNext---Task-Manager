import streamlit as st
import functions
from datetime import date

# Set the page to use a wide layout
st.set_page_config(layout="wide")

# CSS for the expander header and header alignment
st.markdown("""
<style>
    /* Style for the entire top header section */
    .header-section {
        padding-bottom: 1rem; /* Add some space below the header content */
        margin-bottom: 1rem; /* Space between header and content below */
        border-bottom: 1px solid #333; /* This creates the horizontal line */
    }

    /* This rule aligns the header items vertically */
    .header-container [data-testid="stHorizontalBlock"] {
        align-items: center;
    }

    /* Target the expander inside our custom container */
    .about-container [data-testid="stExpander"] {
        width: 350px !important;
        border: 1px solid #333 !important; /* Adjusted for dark theme */
        border-radius: 5px !important;
        box-shadow: none !important;
    }

    /* Style the header part of the expander */
    .about-container [data-testid="stExpander"] summary {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        padding: 0.75rem 1rem !important;
        display: flex;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

def get_todos():
    return functions.get_todos("todos.txt")

def add_todo():
    new_todo_text = st.session_state["new_todo"]
    new_todo_priority = st.session_state["new_todo_priority"]
    new_todo_date = st.session_state["new_todo_date"]

    if new_todo_text.strip():
        todos = get_todos()
        todos.append({
            "task": new_todo_text.strip(),
            "priority": new_todo_priority,
            "due_date": str(new_todo_date),
            "completed": False
        })
        functions.write_todos(todos, "todos.txt")
        st.success("Task added successfully!")

def toggle_complete(index):
    todos = get_todos()
    todos[index]["completed"] = not todos[index]["completed"]
    functions.write_todos(todos, "todos.txt")
    st.success("Task updated!")

def delete_todo(index):
    todos = get_todos()
    todos.pop(index)
    functions.write_todos(todos, "todos.txt")
    st.success("Task deleted successfully!")

def set_edit_mode(index):
    todos = get_todos()
    st.session_state["edit_index"] = index
    st.session_state["new_todo"] = todos[index]["task"]
    st.session_state["new_todo_priority"] = todos[index]["priority"]
    st.session_state["new_todo_date"] = date.fromisoformat(todos[index]["due_date"])

def save_changes():
    index = st.session_state["edit_index"]
    todos = get_todos()
    todos[index]["task"] = st.session_state["new_todo"]
    todos[index]["priority"] = st.session_state["new_todo_priority"]
    todos[index]["due_date"] = str(st.session_state["new_todo_date"])
    functions.write_todos(todos, "todos.txt")
    st.session_state["edit_index"] = None # Clear edit mode
    st.success("Task updated successfully!")

def clear_completed_todos():
    todos = get_todos()
    incomplete_todos = [todo for todo in todos if not todo["completed"]]
    functions.write_todos(incomplete_todos, "todos.txt")
    st.success("Completed tasks cleared!")

if "edit_index" not in st.session_state:
    st.session_state["edit_index"] = None

# Simplified header layout - NOW WRAPPED IN .header-section
st.markdown('<div class="header-section">', unsafe_allow_html=True)
st.markdown('<div class="header-container">', unsafe_allow_html=True)
title_col, about_col = st.columns([0.85, 0.15])

with title_col:
    st.markdown("<h1 style='text-align: center; font-size: 2.5rem; margin-top: 0; margin-bottom: 0;'>NoteNext ✅</h1>", unsafe_allow_html=True)

with about_col:
    with st.container():
        st.markdown('<div class="about-container">', unsafe_allow_html=True)
        with st.expander("About this app"):
            st.markdown("""
                **NoteNext ✅** is a simple and elegant to-do list application.
                * **Add:** Type your task in the input box and press Enter.
                * **Complete:** Click the checkbox next to a task.
                * **Delete:** Remove a task with the ❌ button.
            """)
        st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True) # CLOSE NEW WRAPPER

# Main two-column layout
col_left, col_divider, col_right = st.columns([0.475, 0.05, 0.475])

with col_left:
    todos = get_todos()
    st.markdown(f"<h3 style='font-size: 1.5rem;'>You have {len(todos)} pending tasks.</h3>", unsafe_allow_html=True)

    if not todos:
        st.markdown(f"<p style='font-size: 1.0rem;'>Your to-do list is empty. Add a new task on the right!</p>", unsafe_allow_html=True)
    else:
        st.button("Clear Completed", on_click=clear_completed_todos)

    st.markdown("<p style='font-size: 1.0rem;'>Search for a task</p>", unsafe_allow_html=True)
    search_query = st.text_input(
        "Search tasks",
        placeholder="Search...",
        key="search_query",
        label_visibility="hidden"
    )

    filtered_todos = [
        todo for todo in todos
        if search_query.lower() in todo['task'].lower()
    ]

    for index, todo in enumerate(filtered_todos):
        col1, col2, col3, col4 = st.columns([0.7, 0.1, 0.1, 0.1])

        task_text = todo['task']
        if todo['completed']:
            task_text = f"~~{task_text}~~"

        with col1:
            st.markdown(f"<span style='font-size: 18px;'>{task_text}</span>", unsafe_allow_html=True)
        with col2:
            complete_button_label = "✅" if not todo['completed'] else "🟢"
            st.button(complete_button_label, key=f"complete_{index}", on_click=toggle_complete, args=(index,))
        with col3:
            st.button("✏️", key=f"edit_{index}", on_click=set_edit_mode, args=(index,))
        with col4:
            st.button("❌", key=f"delete_{index}", on_click=delete_todo, args=(index,))

with col_divider:
    st.markdown("""
        <div style="border-left: 1px solid #444; height: 100vh; position: absolute; left: 50%;"></div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-size: 1.75rem;'>Add or Edit a To-Do</h2>", unsafe_allow_html=True)

    with st.form(key="todo_form", clear_on_submit=True):
        st.text_input(
            "Task",
            placeholder="Add new to-do...",
            key="new_todo"
        )
        st.selectbox(
            "Priority",
            options=["High", "Medium", "Low"],
            key="new_todo_priority"
        )
        st.date_input(
            "Due Date",
            key="new_todo_date"
        )

        # Use on_click callbacks for robust form handling
        if st.session_state.get("edit_index") is not None:
            st.form_submit_button("Save Changes", on_click=save_changes)
        else:
            st.form_submit_button("Add To-Do", on_click=add_todo)