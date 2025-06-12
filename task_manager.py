import json
import os
import getpass

USERS_FILE = "users.json"
TASKS_FOLDER = "tasks"  # Directory to store user task files

# Load user data
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

# Save user data
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# Register a new user
def register(users):
    username = input("Enter new username: ")
    if username in users:
        print("❌ Username already exists.\n")
        return None
    password = getpass.getpass("Enter new password: ")
    users[username] = password
    save_users(users)
    print("✅ Registration successful!\n")
    return username

# Login an existing user
def login(users):
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    if users.get(username) == password:
        print("✅ Login successful!\n")
        return username
    else:
        print("❌ Invalid credentials.\n")
        return None

# Load tasks from file
def load_tasks(username):
    filepath = os.path.join(TASKS_FOLDER, f"{username}_tasks.json")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return []

# Save tasks to file
def save_tasks(username, tasks):
    os.makedirs(TASKS_FOLDER, exist_ok=True)
    filepath = os.path.join(TASKS_FOLDER, f"{username}_tasks.json")
    with open(filepath, "w") as f:
        json.dump(tasks, f, indent=4)

# Display all tasks
def view_tasks(tasks):
    if not tasks:
        print("📋 No tasks found.\n")
        return
    print("\nYour Tasks:")
    for i, task in enumerate(tasks, 1):
        status = "✅" if task["completed"] else "❌"
        print(f"{i}. [{status}] {task['task']}")
    print()

# Add new task
def add_task(tasks):
    task_desc = input("Enter task description: ")
    tasks.append({"task": task_desc, "completed": False})
    print("✅ Task added.\n")

# Mark task as complete
def complete_task(tasks):
    view_tasks(tasks)
    try:
        task_no = int(input("Enter task number to mark as complete: "))
        if 1 <= task_no <= len(tasks):
            tasks[task_no - 1]["completed"] = True
            print("✅ Task marked as complete.\n")
        else:
            print("❌ Invalid task number.\n")
    except ValueError:
        print("❌ Please enter a valid number.\n")

# Delete task
def delete_task(tasks):
    view_tasks(tasks)
    try:
        task_no = int(input("Enter task number to delete: "))
        if 1 <= task_no <= len(tasks):
            removed = tasks.pop(task_no - 1)
            print(f"🗑️ Task '{removed['task']}' deleted.\n")
        else:
            print("❌ Invalid task number.\n")
    except ValueError:
        print("❌ Please enter a valid number.\n")

# Task menu
def task_menu(username):
    tasks = load_tasks(username)
    while True:
        print("=== Task Manager Menu ===")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Logout")
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            save_tasks(username, tasks)
            print("👋 Logged out.\n")
            break
        else:
            print("❌ Invalid option. Try again.\n")

# Main loop
def main():
    users = load_users()
    while True:
        print("=== Welcome to Task Manager ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")

        if choice == "1":
            user = register(users)
            if user:
                task_menu(user)
        elif choice == "2":
            user = login(users)
            if user:
                task_menu(user)
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Try again.\n")

if __name__ == "__main__":
    main()
