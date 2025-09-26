class Student:
    def __init__(self, roll_number, name, class_name):
        self.roll_number = roll_number
        self.name = name
        self.class_name = class_name
        self.marks = {}

    def add_marks(self, subject, mark):
        self.marks[subject] = mark

    def display_details(self):
        print(f"Roll Number: {self.roll_number}")
        print(f"Name: {self.name}")
        print(f"Class: {self.class_name}")
        print("Marks:")
        for subject, mark in self.marks.items():
            print(f"{subject}: {mark}")

class StudentRecordSystem:
    def __init__(self):
        self.students = {}

    def add_student(self, roll_number, name, class_name):
        self.students[roll_number] = Student(roll_number, name, class_name)
        print(f"Student {name} added successfully!")

    def delete_student(self, roll_number):
        if roll_number in self.students:
            del self.students[roll_number]
            print(f"Student with roll number {roll_number} deleted successfully!")
        else:
            print(f"Student with roll number {roll_number} not found!")

    def display_student_details(self, roll_number):
        if roll_number in self.students:
            self.students[roll_number].display_details()
        else:
            print(f"Student with roll number {roll_number} not found!")

    def add_marks(self, roll_number, subject, mark):
        if roll_number in self.students:
            self.students[roll_number].add_marks(subject, mark)
            print(f"Marks added successfully for student {self.students[roll_number].name}!")
        else:
            print(f"Student with roll number {roll_number} not found!")

def main():
    system = StudentRecordSystem()

    while True:
        print("\nStudent Record Management System")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Display Student Details")
        print("4. Add Marks")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            roll_number = input("Enter roll number: ")
            name = input("Enter name: ")
            class_name = input("Enter class: ")
            system.add_student(roll_number, name, class_name)
        elif choice == "2":
            roll_number = input("Enter roll number: ")
            system.delete_student(roll_number)
        elif choice == "3":
            roll_number = input("Enter roll number: ")
            system.display_student_details(roll_number)
        elif choice == "4":
            roll_number = input("Enter roll number: ")
            subject = input("Enter subject: ")
            mark = float(input("Enter mark: "))
            system.add_marks(roll_number, subject, mark)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()