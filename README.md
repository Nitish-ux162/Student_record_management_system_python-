# Student Record Management System (Python + SQLite)

This project is a **console-based Student Record Management System** built using **Python 3** and **SQLite3**.

It allows performing CRUD (Create, Read, Update, Delete) operations on student records.

---

## Features

* Add a new student
* List all students
* Find student by **ID** or **Roll Number**
* Update student details
* Delete a student record

---

## Requirements

* Python **3.8+** (tested on Python 3.10)
* No external libraries required (uses built-in `sqlite3`)

---

## Project Structure

```
student_record_system/
├── student_system.py   # Main script
├── students.db         # SQLite database (auto-created on first run)
```

---

## Run Instructions

1. Clone or download the project folder.
2. Open a terminal in the folder.
3. Run:

   ```bash
   python student_system.py
   ```
4. On first run, `students.db` will be created automatically.

---

## Example Usage

```
=== Student Record Management ===
1. Add student
2. List students
3. Find student by ID or Roll no
4. Update student
5. Delete student
0. Exit
Enter choice: 1
Roll no: 101
First name: Alice
Last name: Johnson
Email (optional): alice@example.com
Course (optional): CS
Year (int, optional): 2
Student added with ID: 1
```

---

## Database Schema

The program automatically creates the following table in **students.db**:

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    course TEXT,
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Future Enhancements

* Export student records to CSV/Excel
* Add user authentication
* GUI (Tkinter/PyQt)
* REST API version (Flask/FastAPI)

---

## Author

Developed by **Nitish Prajapati**.
