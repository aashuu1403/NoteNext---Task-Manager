import streamlit as st
import functions
from datetime import date

# Set the page to use a wide layout
st.set_page_config(layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Target the bordered containers to increase border and set height */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 2px solid #333 !important;
        min-height: 65vh; /* Sets a minimum height (65% of the viewport height) */
    }

    /* Style for individual to-do cards */
    .todo-card {
        background-color: #262730;
        border-radius: 7px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-left: 5px solid #444;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Adjust button spacing within the card */
    .todo-card .stButton {
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
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
        st.session_state["new_todo"] = "" # Clear input after adding


def toggle_complete(index):
    todos = get_todos()
    todos[index]["completed"] = not todos[index]["completed"]
    functions.write_todos(todos, "todos.txt")


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
    # Clear form inputs after saving
    st.session_state["new_todo"] = ""
    st.session_state["new_todo_priority"] = "Medium"
    st.session_state["new_todo_date"] = date.today()


def cancel_edit():
    st.session_state["edit_index"] = None
    # Clear the input fields
    st.session_state["new_todo"] = ""
    st.session_state["new_todo_priority"] = "Medium"
    st.session_state["new_todo_date"] = date.today()

def clear_completed_todos():
    todos = get_todos()
    incomplete_todos = [todo for todo in todos if not todo["completed"]]
    functions.write_todos(incomplete_todos, "todos.txt")
    st.success("Completed tasks cleared!")

if "edit_index" not in st.session_state:
    st.session_state["edit_index"] = None

# --- HEADER ---
st.markdown(
    "<h1 style='text-align: center; font-weight: bold; font-size: 3.5rem; margin-bottom: 2rem;'>NoteNext ✅</h1>",
    unsafe_allow_html=True
)


# --- MAIN LAYOUT ---
col_left, col_right = st.columns(2, gap="large")

# --- LEFT COLUMN (TASK LIST) ---
with col_left:
    with st.container(border=True):
        todos = get_todos()
        st.markdown(f"<h3 style='font-size: 1.5rem;'>You have {len(todos)} pending tasks.</h3>", unsafe_allow_html=True)

        if not todos:
            st.info("Your to-do list is empty. Add a new task on the right!")
        else:
            st.button("Clear Completed", on_click=clear_completed_todos, use_container_width=True)

        st.markdown("<p style='font-size: 1.0rem; margin-top: 1rem;'>Search for a task</p>", unsafe_allow_html=True)
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

        PRIORITY_COLORS = {"High": "#FF4B4B", "Medium": "#FFA500", "Low": "#1E90FF"}

        for index, todo in enumerate(filtered_todos):
            with st.container():
                border_color = PRIORITY_COLORS.get(todo.get('priority', 'Medium'))
                st.markdown(f'<div class="todo-card" style="border-left-color: {border_color};">', unsafe_allow_html=True)

                task_col, actions_col = st.columns([0.7, 0.3])

                with task_col:
                    task_text = todo['task']
                    if todo['completed']:
                        task_text = f"~~{task_text}~~"
                    
                    due_date = todo.get('due_date', '')

                    st.markdown(f"""
                        <div style="display: flex; flex-direction: column;">
                            <span style='font-size: 18px;'>{task_text}</span>
                            <span style='font-size: 12px; color: #aaa; margin-top: 5px;'>Due: {due_date}</span>
                        </div>
                    """, unsafe_allow_html=True)

                with actions_col:
                    btn_col1, btn_col2, btn_col3 = st.columns(3)
                    with btn_col1:
                        st.button("✅" if not todo['completed'] else "🟢", key=f"complete_{index}", on_click=toggle_complete, args=(index,), help="Mark as complete", use_container_width=True)
                    with btn_col2:
                        st.button("✏️", key=f"edit_{index}", on_click=set_edit_mode, args=(index,), help="Edit task", use_container_width=True)
                    with btn_col3:
                        st.button("❌", key=f"delete_{index}", on_click=delete_todo, args=(index,), help="Delete task", use_container_width=True)

                st.markdown('</div>', unsafe_allow_html=True)

# --- RIGHT COLUMN (ADD/EDIT FORM) ---
with col_right:
    with st.container(border=True):
        with st.expander("About this app"):
            st.markdown("""
                **NoteNext ✅** is a simple and elegant to-do list application.
                * **Add:** Type your task in the input box and press Enter.
                * **Complete:** Click the checkbox next to a task.
                * **Delete:** Remove a task with the ❌ button.
            """)


        form_title = "Edit Task" if st.session_state.get("edit_index") is not None else "Add a To-Do"
        st.markdown(f"<h2 style='font-size: 1.75rem; margin-top: 1rem;'>{form_title}</h2>", unsafe_allow_html=True)

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

            if st.session_state.get("edit_index") is not None:
                save_col, cancel_col = st.columns(2)
                with save_col:
                    st.form_submit_button("Save Changes", on_click=save_changes, use_container_width=True)
                with cancel_col:
                    st.form_submit_button("Cancel", on_click=cancel_edit, use_container_width=True)
            else:
                st.form_submit_button("Add To-Do", on_click=add_todo, use_container_width=True)