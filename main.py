from functions import get_todos, write_todos
import time

now = time.strftime("%b %d, %Y %H:%M:%S")
print("It is ", now)

while True:
    action = input("Add a new todo (add), show todos(show), edit, complete, exit: ")
    action = action.strip()

    if action.startswith('add '):
        todo = action[4:]
        todos = get_todos("todos.txt")
        todos.append(todo + '\n')
        write_todos(todos, "todos.txt")


    elif action.startswith('show'):
        todos = get_todos("todos.txt")
        for index, item in enumerate(todos):
            item = item.strip('\n')
            row = f"{index + 1}. {item}"
            print(row)


    elif action.startswith('edit '):
        try:
            number = int(action[5:])
            number = number - 1
            todos = get_todos("todos.txt")
            new_todo = input("Enter the new todo: ")
            todos[number] = new_todo + '\n'
            write_todos(todos, "todos.txt")
        except ValueError:
            print("Invalid input. Please enter a valid todo number.")
            continue


    elif action.startswith('complete '):
        try:
            number = int(action[9:])
            todos = get_todos("todos.txt")
            index = number - 1
            todo_to_remove = todos[index].strip('\n')
            todos.pop(index)
            write_todos(todos, "todos.txt")
            message = f"Todo {todo_to_remove} was removed."
            print(message)
        except ValueError:
            print("Invalid input. Please enter a valid todo number.")
            continue


    elif action.startswith('exit'):
        break
    else:
        print("Invalid action. Please try again.")


print("Goodbye!")
print("You have exited the todo list application.")