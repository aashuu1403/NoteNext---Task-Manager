from functions import get_todos, write_todos
import time
from datetime import date

now = time.strftime("%b %d, %Y %H:%M:%S")
print("It is ", now)

while True:
    action = input("Add, show, edit, complete, or exit: ")
    action = action.strip().lower()

    if action.startswith('add '):
        todo_text = action[4:]
        todos = get_todos()
        
        # Create a dictionary for the new todo
        new_todo = {
            "task": todo_text,
            "priority": "Medium", # Default priority
            "due_date": str(date.today()), # Default due date
            "completed": False
        }
        todos.append(new_todo)
        write_todos(todos)
        print(f"Added '{todo_text}'.")

    elif action == 'show':
        todos = get_todos()
        if not todos:
            print("Your to-do list is empty.")
        for index, item in enumerate(todos):
            # Access the task using its key
            task = item['task']
            status = " (Completed)" if item['completed'] else ""
            row = f"{index + 1}. {task}{status}"
            print(row)

    elif action.startswith('edit '):
        try:
            number = int(action[5:])
            index = number - 1
            todos = get_todos()
            
            if 0 <= index < len(todos):
                new_text = input(f"Enter the new text for '{todos[index]['task']}': ")
                todos[index]['task'] = new_text
                write_todos(todos)
                print("Todo updated.")
            else:
                print("That number is not on the list.")
        except ValueError:
            print("Invalid input. Please enter a valid todo number.")
        except IndexError:
            print("That number is not on the list.")

    elif action.startswith('complete '):
        try:
            number = int(action[9:])
            index = number - 1
            todos = get_todos()
            
            if 0 <= index < len(todos):
                todos[index]['completed'] = True
                write_todos(todos)
                print(f"Todo '{todos[index]['task']}' marked as complete.")
            else:
                print("That number is not on the list.")
        except ValueError:
            print("Invalid input. Please enter a valid todo number.")
        except IndexError:
            print("That number is not on the list.")

    elif action == 'exit':
        break
    else:
        print("Invalid action. Please try again.")

print("Goodbye!")