[Screenshot 2026-10-21 114147.png…]()






# Python + MySQL Todo List Management System

A beginner-friendly, clean, and robust command-line Todo List Management System built using **Python 3**, **MySQL**, and **mysql-connector-python**.

---

## 📖 Project Overview

This project is designed as an educational application to teach students the fundamentals of:
1. Connecting a Python application to a relational database (MySQL).
2. Implementing **CRUD** operations (Create, Read, Update, Delete).
3. Writing secure, SQL-injection-safe queries using parameterization (`%s`).
4. Structuring code into modular, single-responsibility files (Separation of Concerns).
5. Building user-friendly Command-Line Interfaces (CLI) with clean error handling.

---

## 📂 Project Structure

```text
python_mysql_todo/
├── schema.sql         # Database schema creation script
├── requirements.txt   # Python dependency list
├── database.py        # Database connection, query execution, and transactions
├── todo.py            # Task management business logic and user validation
├── main.py            # CLI menu loop and application entry point
└── README.md          # Project documentation and student guide
```

### Responsibility of Each File

| File | Role & Responsibility |
| :--- | :--- |
| `schema.sql` | Contains the SQL commands to create the `todo_db` database and `tasks` table with appropriate columns and constraints. Safe to run multiple times (`IF NOT EXISTS`). |
| `requirements.txt` | Lists external Python libraries needed for the project (`mysql-connector-python`). |
| `database.py` | Acts as the **Data Access Layer**. Connects to MySQL, executes parameterized queries, commits transactions, rolls back failures, and safely closes connections. |
| `todo.py` | Acts as the **Business Logic Layer**. Validates user input, asks for confirmation on deletions, displays formatted task lists, and coordinates actions with `database.py`. |
| `main.py` | Acts as the **Presentation/Interface Layer**. Runs the command-line menu loop, receives choices (0–6), dispatches requests to `todo.py`, and handles program termination. |

---

## 🏛️ Application Architecture & Program Flow

The application follows a simple **Three-Tier Architecture**:

```text
+------------------------------------+
|             main.py                |  <-- Presentation Layer (CLI Menu)
+------------------------------------+
                 |
                 v
+------------------------------------+
|             todo.py                |  <-- Business Logic Layer (Validation & Rules)
+------------------------------------+
                 |
                 v
+------------------------------------+
|           database.py              |  <-- Data Access Layer (SQL Queries & Transactions)
+------------------------------------+
                 |
                 v
+------------------------------------+
|          MySQL Database            |  <-- Persistence Layer (Tables & Records)
+------------------------------------+
```

### How the Layers Interact:
1. **User interaction (`main.py`)**: The user selects an option from the menu (e.g., option `1` to Add Task).
2. **Business validation (`todo.py`)**: `todo.py` prompts the user for task details, ensures the title is not blank, and formats data.
3. **Database execution (`database.py`)**: `database.py` receives clean parameters, connects to MySQL, executes parameterized SQL (`INSERT INTO tasks ...`), commits the transaction, and returns the result.
4. **User feedback (`main.py` / `todo.py`)**: The user receives a clear confirmation message like `[Success] Task created successfully with ID #1.`

---

## 🧠 Core Concepts Explained

### 1. What is CRUD?
CRUD is an acronym for the four essential operations performed on persistent data:
- **C — Create**: Adding new records to the database (`INSERT INTO tasks ...`). In our app: `add_task()`.
- **R — Read**: Retrieving and viewing stored records (`SELECT * FROM tasks ...`). In our app: `view_tasks()` and `view_task_by_id()`.
- **U — Update**: Modifying existing records (`UPDATE tasks SET ...`). In our app: `update_task()` and `mark_completed()`.
- **D — Delete**: Removing records permanently (`DELETE FROM tasks WHERE id = ...`). In our app: `delete_task()`.

### 2. How Python Connects to MySQL
Python uses the official `mysql-connector-python` driver to open a TCP socket connection to the MySQL server (typically running on `localhost:3306`).
```python
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="todo_db"
)
```
- A **connection** represents the active session with the MySQL server.
- A **cursor** acts as the pointer or handle used to execute SQL statements and retrieve rows.

### 3. Why Parameterized Queries Are Essential
**Never** concatenate raw user input into SQL queries (e.g., `f"SELECT * FROM tasks WHERE id = {user_input}"`). Doing so exposes the system to **SQL Injection**, where malicious users can inject SQL code to alter, steal, or delete data.

**Correct, Parameterized Query:**
```python
# The database driver treats the %s placeholder strictly as data, never as executable SQL code:
query = "SELECT * FROM tasks WHERE id = %s;"
cursor.execute(query, (task_id,))
```

### 4. Transactions: Commit and Rollback
- `connection.commit()`: Saves changes permanently in the database.
- `connection.rollback()`: Cancels changes if an error occurs, keeping the database in a clean state.
- `finally:` ensures connections and cursors are always closed, preventing memory leaks and connection exhaustion.

---

## 🛠️ Step-by-Step Installation and Setup Guide (Windows)

### Prerequisites
1. **Python 3.10+**: Download and install from [python.org](https://www.python.org/). Check "Add Python to PATH" during installation.
2. **MySQL Server**: Ensure MySQL Server is installed (via MySQL Community Server, XAMPP, or WampServer) and running.

---

### Step 1: Open the Project in VS Code
1. Launch **Visual Studio Code**.
2. Go to **File** > **Open Folder...** and select the `python_mysql_todo` folder.
3. Open a terminal by pressing `Ctrl + ` `~` (or go to **Terminal** > **New Terminal**).

---

### Step 2: Set Up Virtual Environment

In the VS Code terminal (PowerShell), run:

```powershell
# Create a virtual environment named .venv
python -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

> **Troubleshooting PowerShell Script Execution:**
> If PowerShell shows an error such as `Activate.ps1 cannot be loaded because running scripts is disabled on this system`, run this once in your PowerShell terminal:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
> .\.venv\Scripts\Activate.ps1
> ```
> Alternatively, you can run all commands directly using the virtual environment's Python executable without activating:
> ```powershell
> .\.venv\Scripts\python.exe -m pip install -r requirements.txt
> .\.venv\Scripts\python.exe main.py
> ```

---

### Step 3: Install Required Packages

With the virtual environment active, install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

---

### Step 4: Configure Database Credentials

By default, `database.py` connects to MySQL using standard local defaults:
- **Host**: `localhost`
- **Port**: `3306`
- **User**: `root`
- **Password**: *(empty)*
- **Database**: `todo_db`

If your MySQL setup uses a custom password or user, you can set environment variables in your terminal before running:

```powershell
$env:DB_USER = "root"
$env:DB_PASSWORD = "your_actual_password"
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
```

---

### Step 5: Execute `schema.sql` to Create Database & Table

You can run `schema.sql` using any of the following methods:

#### Method A: Using MySQL Command-Line Client (PowerShell)
```powershell
# If MySQL client is in your PATH:
mysql -u root -p < schema.sql

# If using XAMPP default installation:
& "C:\xampp\mysql\bin\mysql.exe" -u root < schema.sql
```

#### Method B: Using MySQL Workbench or phpMyAdmin
1. Open **MySQL Workbench** or **phpMyAdmin** (`http://localhost/phpmyadmin`).
2. Open or paste the contents of `schema.sql`.
3. Click **Execute** (or the lightning bolt icon).

---

### Step 6: Run the Application

Launch the CLI application:

```powershell
python main.py
```

---

## 🖥️ Sample Terminal Session

```text
====================================
      PYTHON MYSQL TODO MANAGER     
====================================
1. Add Task
2. View All Tasks
3. View Task by ID
4. Update Task
5. Mark Task as Completed
6. Delete Task
0. Exit
====================================
Enter your choice (0-6): 1

--- Add New Task ---
Enter task title: Buy groceries
Enter task description (optional, press Enter to skip): Milk, eggs, and bread
[Success] Task created successfully with ID #1.

====================================
      PYTHON MYSQL TODO MANAGER     
====================================
1. Add Task
2. View All Tasks
3. View Task by ID
4. Update Task
5. Mark Task as Completed
6. Delete Task
0. Exit
====================================
Enter your choice (0-6): 2

--- All Tasks ---
---------------------------------------------------------------------------
ID     | Status       | Created At          | Title
---------------------------------------------------------------------------
1      | Pending      | 2026-10-14 08:30:15 | Buy groceries
---------------------------------------------------------------------------
Total tasks: 1

====================================
      PYTHON MYSQL TODO MANAGER     
====================================
...
Enter your choice (0-6): 5

--- Mark Task as Completed ---
Enter Task ID: 1
[Success] Task #1 marked as Completed.

====================================
      PYTHON MYSQL TODO MANAGER     
====================================
...
Enter your choice (0-6): 0

Thank you for using Python MySQL Todo Manager. Goodbye!
```

---

## ❓ Common Errors & Solutions

| Error Message | Cause | Solution |
| :--- | :--- | :--- |
| `Can't connect to MySQL server on 'localhost'` | MySQL server is stopped or port is blocked. | Start the MySQL service via Windows Services (`services.msc`), XAMPP Control Panel, or command line. |
| `Access denied for user 'root'@'localhost'` | Password or username is incorrect. | Update `$env:DB_PASSWORD` or change default credentials in `database.py`. |
| `Unknown database 'todo_db'` | The database has not been initialized. | Execute `schema.sql` to create `todo_db` and the `tasks` table. |
| `Activate.ps1 cannot be loaded...` | Windows PowerShell execution policy restricts scripts. | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`. |
| `ModuleNotFoundError: No module named 'mysql'` | The dependency was not installed in the active environment. | Run `python -m pip install -r requirements.txt` inside your virtual environment. |

---

## 🧪 Testing Checklist

- [x] Application connects to MySQL successfully.
- [x] Adding a task inserts record and returns new ID.
- [x] Viewing all tasks displays table with IDs, status, timestamps, and titles.
- [x] Searching task by ID displays full details card.
- [x] Updating a task modifies title and/or description.
- [x] Marking a task completed sets status to `Completed`.
- [x] Deleting a task requires user confirmation (`y/n`).
- [x] Empty titles are caught and rejected.
- [x] Invalid non-numeric or negative task IDs are handled safely.
- [x] Nonexistent task IDs display a polite informative message.
- [x] Database connections and cursors are safely closed in `finally` blocks.
- [x] Transactions are committed on success and rolled back on error.

