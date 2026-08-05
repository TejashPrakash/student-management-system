import logging
import sys

from errors import EduTrackError
from input_validators import (
    get_choice,
    get_date,
    get_email,
    get_phone,
    get_positive_int,
    get_text,
    )
from student import Student
from student_repository import (
    insert_student,
    get_student_by_roll_no,
    get_student_by_id,
    get_all_students,
    update_student,
    delete_student
    )

logger = logging.getLogger(__name__)


def _prompt_student(student_id):
    first_name = get_text("Enter First Name: ", 50)
    last_name = get_text("Enter Last Name: ", 50)
    gender = get_choice("Enter Gender (Male/Female/Other): ")
    dob = get_date("Enter Date of Birth (YYYY-MM-DD): ", allow_future=False)
    class_name = get_text("Enter Class: ", 10)
    section = get_text("Enter Section: ", 1)
    roll_no = get_positive_int("Enter Roll Number: ")
    email = get_email("Enter Email: ")
    phone = get_phone("Enter Phone Number: ")
    address = get_text("Enter Address: ", 500)
    admission_date = get_date("Enter Admission Date (YYYY-MM-DD): ")

    return Student(
        student_id=student_id,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        dob=dob,
        class_name=class_name,
        section=section,
        roll_no=roll_no,
        email=email,
        phone=phone,
        address=address,
        admission_date=admission_date
    )


def handle_choice(choice):
    """Run one menu action. Returns False when the user asked to exit."""
    if choice == "1":
        print("You have selected to add a student...")
        student = _prompt_student(student_id=None)
        insert_student(student)
        print("\nStudent added successfully!\n")

    elif choice == "2":
        print("You have selected to search a student by Roll Number")
        roll_no = get_positive_int("Enter Roll Number: ")

        student = get_student_by_roll_no(roll_no)

        if student:
            student.display_info()
        else:
            print("Student not found.")

    elif choice == "3":
        print("You have selected to search a student by Student ID.")
        student_id = get_positive_int("Enter Student ID: ")

        student = get_student_by_id(student_id)

        if student:
            student.display_info()
        else:
            print("Student not found.")

    elif choice == "4":
        print("You have selected to View All Students.")
        students = get_all_students()
        if not students:
            print("No student found.")
        else:
            for student in students:
                student.display_info()

    elif choice == "5":
        print("You have selected to update a student.")
        student_id = get_positive_int("Enter Student ID: ")

        student = get_student_by_id(student_id)

        if student:
            print("\nCurrent Student Details:")
            student.display_info()
            print("Enter the Updated Details: ")

            if update_student(_prompt_student(student_id)):
                print("Student updated successfully.")
            else:
                print("No student record was updated (ID might not exist).")
        else:
            print("Student not found.")

    elif choice == "6":
        print("You have selected to delete the entry of a student.")
        student_id = get_positive_int("Enter Student ID: ")

        student = get_student_by_id(student_id)

        if student:
            print("\nCurrent Student Details:")
            student.display_info()
            ch = input("Are you sure you want to delete this student? (Y/N): ")
            if ch.strip().upper() == "Y":
                if delete_student(student_id):
                    print("Student deleted successfully.")
                else:
                    print(f"No student found with ID {student_id} to delete.")
            else:
                print("Deletion cancelled.")

        else:
            print("Student not found.")

    elif choice == "7":
        print("\nThank you for using EduTrack!")
        return False
    else:
        print("\nFeature coming soon...")

    return True


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    while True:
        print()
        print("=" * 40)
        print("                EDUTRACK                ")
        print("        Student Management System       ")
        print("=" * 40)
        print("1.  Add Student")
        print("2.  Search Student by Roll Number")
        print("3.  Search Student by Student ID")
        print("4.  View All Students")
        print("5.  Update Student")
        print("6.  Delete Student")
        print("7.  Exit")
        print("=" * 40)

        try:
            choice = input("Enter your choice: ").strip()
            if not handle_choice(choice):
                return 0
        except EduTrackError as exc:
            logger.error("%s", exc)
            logger.debug("Menu option %s failed.", choice, exc_info=True)
        except (EOFError, KeyboardInterrupt):
            print("\nInterrupted. Exiting EduTrack.")
            return 130


if __name__ == "__main__":
    sys.exit(main())
