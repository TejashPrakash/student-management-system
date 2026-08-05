from database import db_cursor
from student import Student
from mysql.connector import Error
from typing import Optional, List

# Column order shared by inserts, updates and row mapping. The database column
# is `class`; the Student attribute is `class_name`.
STUDENT_COLUMNS = (
    "first_name",
    "last_name",
    "gender",
    "dob",
    "class",
    "section",
    "roll_no",
    "email",
    "phone",
    "address",
    "admission_date",
)

_COLUMNS_SQL = ", ".join(f"`{column}`" for column in STUDENT_COLUMNS)
_PLACEHOLDERS_SQL = ", ".join(["%s"] * len(STUDENT_COLUMNS))
_UPDATE_SET_SQL = ", ".join(f"`{column}` = %s" for column in STUDENT_COLUMNS)

INSERT_QUERY = f"INSERT INTO students ({_COLUMNS_SQL}) VALUES ({_PLACEHOLDERS_SQL})"
UPDATE_QUERY = f"UPDATE students SET {_UPDATE_SET_SQL} WHERE student_id = %s"

# Errors that can surface from the shared cursor helper.
_DB_ERRORS = (Error, ConnectionError)


def _student_values(student: Student) -> tuple:
    """Return the student's field values in STUDENT_COLUMNS order."""
    return (
        student.first_name,
        student.last_name,
        student.gender,
        student.dob,
        student.class_name,
        student.section,
        student.roll_no,
        student.email,
        student.phone,
        student.address,
        student.admission_date,
    )


def _row_to_student(row: dict) -> Student:
    """Build a Student from a dictionary cursor row."""
    return Student(
        student_id=row.get("student_id"),
        first_name=row.get("first_name"),
        last_name=row.get("last_name"),
        gender=row.get("gender"),
        dob=row.get("dob"),
        class_name=row.get("class"),
        section=row.get("section"),
        roll_no=row.get("roll_no"),
        email=row.get("email"),
        phone=row.get("phone"),
        address=row.get("address"),
        admission_date=row.get("admission_date"),
    )


def insert_student(student: Student) -> bool:
    try:
        with db_cursor(dictionary=True, commit=True) as cursor:
            cursor.execute(INSERT_QUERY, _student_values(student))
        print(f"Success: Student '{student.get_full_name()}' has been added to the database.")
        return True
    except _DB_ERRORS as e:
        print(f"An error occurred while inserting student: {e}")
        return False


def get_student_by_roll_no(roll_no: int) -> Optional[Student]:
    try:
        with db_cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM students WHERE roll_no = %s", (roll_no,))
            row = cursor.fetchone()
        return _row_to_student(row) if row else None
    except _DB_ERRORS as e:
        print(f"An error occurred while fetching student by roll number: {e}")
        return None


def get_student_by_id(student_id: int) -> Optional[Student]:
    try:
        with db_cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
            row = cursor.fetchone()
        return _row_to_student(row) if row else None
    except _DB_ERRORS as e:
        print(f"An error occurred while fetching student by id: {e}")
        return None


def get_all_students() -> List[Student]:
    try:
        with db_cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
        return [_row_to_student(row) for row in rows]
    except _DB_ERRORS as e:
        print(f"An error occurred while fetching all students: {e}")
        return []


def update_student(student: Student) -> bool:
    try:
        with db_cursor(commit=True) as cursor:
            cursor.execute(UPDATE_QUERY, _student_values(student) + (student.student_id,))
            updated = cursor.rowcount > 0
        if updated:
            print(f"Student '{student.get_full_name()}' updated successfully.")
        else:
            print("No student record was updated (ID might not exist).")
        return updated
    except _DB_ERRORS as e:
        print(f"An error occurred while updating student: {e}")
        return False


def delete_student(student_id: int) -> bool:
    try:
        with db_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            deleted = cursor.rowcount > 0
        if deleted:
            print(f"Deleted student with id {student_id}.")
        else:
            print(f"No student found with ID {student_id} to delete.")
        return deleted
    except _DB_ERRORS as e:
        print(f"An error occurred while deleting student: {e}")
        return False
