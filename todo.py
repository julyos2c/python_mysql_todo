import database


def validate_input(prompt, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if not allow_empty and not value:
            print("[Warning] This field cannot be empty. Please enter a value.")
            continue
        return value


def get_valid_task_id(prompt="Enter Task ID: "):
    raw_input = input(prompt).strip()
    if not raw_input.isdigit() or int(raw_input) <= 0:
        print("[Error] Invalid Task ID. Please enter a positive whole number.")
        return None
    return int(raw_input)


def add_task():
    print("\n--- Add New Task ---")
    title = validate_input("Enter task title: ", allow_empty=False)
    description = validate_input("Enter task description (optional, press Enter to skip): ", allow_empty=True)
    
    desc_to_store = description if description else None

    task_id = database.insert_task(title, desc_to_store)
    if task_id:
        print(f"[Success] Task created successfully with ID #{task_id}.")
    else:
        print("[Error] Failed to create task. Please try again.")


def view_tasks():
    print("\n--- All Tasks ---")
    tasks = database.get_all_tasks()
    
    if not tasks:
        print("No tasks found. Your todo list is currently empty!")
        return

    header = f"{'ID':<6} | {'Status':<12} | {'Created At':<19} | {'Title'}"
    separator = "-" * 75
    print(separator)
    print(header)
    print(separator)

    for task in tasks:
        task_id = str(task["id"])
        status = task["status"]
        created_at = str(task["created_at"]) if task["created_at"] else "N/A"
        title = task["title"]
        title_display = title if len(title) <= 35 else title[:32] + "..."
        print(f"{task_id:<6} | {status:<12} | {created_at:<19} | {title_display}")

    print(separator)
    print(f"Total tasks: {len(tasks)}")


def view_task_by_id():
    print("\n--- View Task by ID ---")
    task_id = get_valid_task_id()
    if task_id is None:
        return

    task = database.get_task_by_id(task_id)
    if not task:
        print(f"[Info] Task with ID #{task_id} does not exist.")
        return

    print("\n" + "=" * 45)
    print(f" Task Details (ID: #{task['id']})")
    print("=" * 45)
    print(f"Title       : {task['title']}")
    print(f"Description : {task['description'] if task['description'] else '(No description provided)'}")
    print(f"Status      : {task['status']}")
    print(f"Created At  : {task['created_at']}")
    print("=" * 45)


def update_task():
    print("\n--- Update Task ---")
    task_id = get_valid_task_id()
    if task_id is None:
        return

    existing_task = database.get_task_by_id(task_id)
    if not existing_task:
        print(f"[Info] Task with ID #{task_id} does not exist.")
        return

    print(f"\nCurrent Title       : {existing_task['title']}")
    print(f"Current Description : {existing_task['description'] if existing_task['description'] else '(None)'}")
    print("(Press Enter without typing to keep the current value)\n")

    new_title = input("Enter new title: ").strip()
    if not new_title:
        new_title = existing_task["title"]

    new_desc = input("Enter new description: ").strip()
    if not new_desc:
        new_desc = existing_task["description"]

    success = database.update_task(task_id, new_title, new_desc)
    if success:
        print(f"[Success] Task #{task_id} was updated successfully.")
    else:
        print(f"[Error] Failed to update task #{task_id}.")


def mark_completed():
    print("\n--- Mark Task as Completed ---")
    task_id = get_valid_task_id()
    if task_id is None:
        return

    existing_task = database.get_task_by_id(task_id)
    if not existing_task:
        print(f"[Info] Task with ID #{task_id} does not exist.")
        return

    if existing_task["status"].lower() == "completed":
        print(f"[Info] Task #{task_id} is already marked as Completed.")
        return

    success = database.mark_task_status(task_id, "Completed")
    if success:
        print(f"[Success] Task #{task_id} marked as Completed.")
    else:
        print(f"[Error] Failed to update task status.")


def delete_task():
    print("\n--- Delete Task ---")
    task_id = get_valid_task_id()
    if task_id is None:
        return

    existing_task = database.get_task_by_id(task_id)
    if not existing_task:
        print(f"[Info] Task with ID #{task_id} does not exist.")
        return

    confirm = input(f"Are you sure you want to delete task #{task_id} ('{existing_task['title']}')? (y/n): ").strip().lower()
    if confirm in ("y", "yes"):
        success = database.delete_task(task_id)
        if success:
            print(f"[Success] Task #{task_id} was deleted successfully.")
        else:
            print(f"[Error] Failed to delete task #{task_id}.")
    else:
        print("[Info] Deletion canceled.")
