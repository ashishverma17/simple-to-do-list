import os
import json
from datetime import datetime

TODO_FILE = "todo_list.json"

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, 'r') as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TODO_FILE, 'w') as file:
        json.dump(tasks, file, indent=2)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    print("\nTo-Do List App")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Remove Task")
    print("4. Mark Task as Complete")
    print("5. View Completed Tasks")
    print("6. Exit")

def view_tasks(tasks, show_completed=False):
    clear_screen()
    filtered_tasks = [task for task in tasks if task['completed'] == show_completed]
    
    if not filtered_tasks:
        status = "completed" if show_completed else "pending"
        print(f"\nNo {status} tasks found.")
        return
    
    print("\n=== Completed Tasks ===" if show_completed else "\n=== Pending Tasks ===")
    for idx, task in enumerate(filtered_tasks, 1):
        status = "✓" if task['completed'] else " "
        created_at = task.get('created_at', 'N/A')
        print(f"{idx}. [{status}] {task['description']} (Created: {created_at})")

def add_task(tasks):
    clear_screen()
    print("\nAdd New Task")
    description = input("Enter task description: ").strip()
    if not description:
        print("Task description cannot be empty!")
        return
    
    new_task = {
        'description': description,
        'completed': False,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task '{description}' added successfully!")

def remove_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    
    try:
        task_num = int(input("\nEnter task number to remove: "))
        if 1 <= task_num <= len(tasks):
            removed = tasks.pop(task_num - 1)
            save_tasks(tasks)
            print(f"Task '{removed['description']}' removed successfully!")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Please enter a valid number!")

def toggle_task_status(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    
    try:
        task_num = int(input("\nEnter task number to mark complete/incomplete: "))
        if 1 <= task_num <= len(tasks):
            task = tasks[task_num - 1]
            task['completed'] = not task['completed']
            if task['completed']:
                task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_tasks(tasks)
            status = "completed" if task['completed'] else "marked incomplete"
            print(f"Task '{task['description']}' {status}!")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Please enter a valid number!")

def main():
    tasks = load_tasks()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            remove_task(tasks)
        elif choice == '4':
            toggle_task_status(tasks)
        elif choice == '5':
            view_tasks(tasks, show_completed=True)
        elif choice == '6':
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1-6.")
        
        if choice != '6':
            input("\nPress Enter to continue...")
            clear_screen()

if __name__ == "__main__":
    main()
