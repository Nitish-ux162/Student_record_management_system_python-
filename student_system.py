import sqlite3
from dataclasses import dataclass, asdict
from typing import Optional, List
import sys

DB_FILE = "students.db"


@dataclass
class Student:
    id: Optional[int] = None
    roll_no: str = ""
    first_name: str = ""
    last_name: str = ""
    email: Optional[str] = None
    course: Optional[str] = None
    year: Optional[int] = None

    def __str__(self):
        return f"{self.id} | {self.roll_no} | {self.first_name} {self.last_name} | {self.email} | {self.course} | Year: {self.year}"


class DB:
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row
        self._ensure_schema()

    def _ensure_schema(self):
        sql = """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT NOT NULL UNIQUE,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            course TEXT,
            year INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.conn.execute(sql)
        self.conn.commit()

    def execute(self, sql: str, params: tuple = ()):
        cur = self.conn.execute(sql, params)
        self.conn.commit()
        return cur

    def query_one(self, sql: str, params: tuple = ()):
        cur = self.conn.execute(sql, params)
        return cur.fetchone()

    def query_all(self, sql: str, params: tuple = ()):
        cur = self.conn.execute(sql, params)
        return cur.fetchall()

    def close(self):
        self.conn.close()


class StudentDAO:
    def __init__(self, db: DB):
        self.db = db

    def add_student(self, s: Student) -> Optional[int]:
        sql = """
        INSERT INTO students (roll_no, first_name, last_name, email, course, year)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            cur = self.db.execute(sql, (s.roll_no, s.first_name, s.last_name, s.email, s.course, s.year))
            return cur.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
            return None

    def get_student_by_id(self, id: int) -> Optional[Student]:
        row = self.db.query_one("SELECT * FROM students WHERE id = ?", (id,))
        return self._row_to_student(row) if row else None

    def get_student_by_roll(self, roll_no: str) -> Optional[Student]:
        row = self.db.query_one("SELECT * FROM students WHERE roll_no = ?", (roll_no,))
        return self._row_to_student(row) if row else None

    def get_all_students(self) -> List[Student]:
        rows = self.db.query_all("SELECT * FROM students ORDER BY id")
        return [self._row_to_student(r) for r in rows]

    def update_student(self, s: Student) -> bool:
        sql = """
        UPDATE students
        SET roll_no = ?, first_name = ?, last_name = ?, email = ?, course = ?, year = ?
        WHERE id = ?
        """
        cur = self.db.execute(sql, (s.roll_no, s.first_name, s.last_name, s.email, s.course, s.year, s.id))
        return cur.rowcount > 0

    def delete_student(self, id: int) -> bool:
        cur = self.db.execute("DELETE FROM students WHERE id = ?", (id,))
        return cur.rowcount > 0

    @staticmethod
    def _row_to_student(row: sqlite3.Row) -> Student:
        return Student(
            id=row["id"],
            roll_no=row["roll_no"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            email=row["email"],
            course=row["course"],
            year=row["year"],
        )


def input_int(prompt: str) -> int:
    while True:
        val = input(prompt).strip()
        try:
            return int(val)
        except ValueError:
            print("Please enter a valid integer.")


def main_menu():
    db = DB()
    dao = StudentDAO(db)

    try:
        while True:
            print("\n=== Student Record Management ===")
            print("1. Add student")
            print("2. List students")
            print("3. Find student by ID or Roll no")
            print("4. Update student")
            print("5. Delete student")
            print("0. Exit")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                roll = input("Roll no: ").strip()
                fn = input("First name: ").strip()
                ln = input("Last name: ").strip()
                email = input("Email (optional): ").strip() or None
                course = input("Course (optional): ").strip() or None
                year_str = input("Year (int, optional): ").strip()
                year = int(year_str) if year_str else None

                s = Student(roll_no=roll, first_name=fn, last_name=ln, email=email, course=course, year=year)
                new_id = dao.add_student(s)
                if new_id:
                    print(f"Student added with ID: {new_id}")
                else:
                    print("Failed to add student (roll_no might be duplicate).")

            elif choice == "2":
                all_students = dao.get_all_students()
                if not all_students:
                    print("No students found.")
                else:
                    for st in all_students:
                        print(st)

            elif choice == "3":
                sub = input("Search by (1) ID or (2) Roll no? ").strip()
                if sub == "1":
                    id = input_int("Enter ID: ")
                    s = dao.get_student_by_id(id)
                    print(s if s else "Not found.")
                else:
                    roll = input("Enter roll no: ").strip()
                    s = dao.get_student_by_roll(roll)
                    print(s if s else "Not found.")

            elif choice == "4":
                id = input_int("Enter student ID to update: ")
                s = dao.get_student_by_id(id)
                if not s:
                    print("No student with given ID.")
                    continue
                print("Leave blank to keep current value.")
                roll = input(f"Roll ({s.roll_no}): ").strip()
                if roll:
                    s.roll_no = roll
                fn = input(f"First name ({s.first_name}): ").strip()
                if fn:
                    s.first_name = fn
                ln = input(f"Last name ({s.last_name}): ").strip()
                if ln:
                    s.last_name = ln
                email = input(f"Email ({s.email}): ").strip()
                if email:
                    s.email = email
                course = input(f"Course ({s.course}): ").strip()
                if course:
                    s.course = course
                year_str = input(f"Year ({s.year}): ").strip()
                if year_str:
                    try:
                        s.year = int(year_str)
                    except ValueError:
                        print("Invalid year entered; keeping old value.")
                ok = dao.update_student(s)
                print("Updated." if ok else "Update failed.")

            elif choice == "5":
                id = input_int("Enter student ID to delete: ")
                ok = dao.delete_student(id)
                print("Deleted." if ok else "Delete failed (ID may not exist).")

            elif choice == "0":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Try again.")

    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")
    finally:
        db.close()


if __name__ == "__main__":
    main_menu()
