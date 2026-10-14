import sys
import database
import todo


def display_menu():
    print()
    print("====================================")
    print("      PYTHON MYSQL TODO MANAGER     ")
    print("====================================")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Task by ID")
    print("4. Update Task")
    print("5. Mark Task as Completed")
    print("6. Delete Task")
    print("0. Exit")
    print("====================================")


def check_database_readiness():
    is_connected, message = database.test_connection()
    if not is_connected:
        print("\n[Database Connection Alert]")
        print(f"Could not connect to MySQL database: {message}")
        print("\nPlease ensure:")
        print("1. Your MySQL server service is actively running.")
        print("2. The 'todo_db' database exists (run 'schema.sql' first).")
        print("3. Connection settings (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME) match your environment.")
        return False
    return True


def main():
    print("Starting Python MySQL Todo List Management System...")
    
    if not check_database_readiness():
        retry = input("\nWould you like to continue anyway? (y/n): ").strip().lower()
        if retry not in ("y", "yes"):
            print("Exiting application. Please start MySQL and run schema.sql first.")
            sys.exit(1)

    while True:
        try:
            display_menu()
            choice = input("Enter your choice (0-6): ").strip()

            if choice == "1":
                todo.add_task()
            elif choice == "2":
                todo.view_tasks()
            elif choice == "3":
                todo.view_task_by_id()
            elif choice == "4":
                todo.update_task()
            elif choice == "5":
                todo.mark_completed()
            elif choice == "6":
                todo.delete_task()
            elif choice == "0":
                print("\nThank you for using Python MySQL Todo Manager. Goodbye!")
                break
            else:
                print("\n[Error] Invalid choice! Please select an option between 0 and 6.")
                
        except KeyboardInterrupt:
            print("\n\n[Info] Keyboard interrupt received. Exiting application. Goodbye!")
            sys.exit(0)
        except Exception as err:
            print(f"\n[Unexpected Error] An unexpected error occurred: {err}")
            print("Returning to the main menu...")


if __name__ == "__main__":
    main()
