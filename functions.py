import json

FILEPATH = "todos.txt"

def get_todos(filepath=FILEPATH):
    """ Read a text file and return the list of
    to-do items.
    """
    try:
        with open(filepath, 'r') as file_local:
            todos_local = json.load(file_local)
    except (FileNotFoundError, json.JSONDecodeError):
        todos_local = []
    return todos_local

def write_todos(todos_arg, filepath=FILEPATH):
    """ Write the to-do items list in the text file."""
    with open(filepath, 'w') as file:
        json.dump(todos_arg, file, indent=4)