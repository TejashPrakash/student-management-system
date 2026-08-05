from database import connect_database
from student import Student
from mysql.connector import Error
from typing import Optional, List


def _row_to_student(row: dict) -> Student:
    """Map a dictionary-cursor row from the students table to a Student."""
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
    
    connection = None
    cursor = None

    try:
        connection = connect_database()
        if connection is None:
            print("Database connection unavailable.")
            return False

        # use dictionary cursor so we can map columns by name
        cursor = connection.cursor(dictionary=True)

        query = ("""INSERT INTO students (first_name,
            last_name,
            gender,
            dob,
            `class`,
            section,
            roll_no,
            email,
            phone,
            address,
            admission_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")

        values = (
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

        cursor.execute(query, values)
        connection.commit()

        print(f"Success: Student '{student.get_full_name()}' has been added to the database.")
        return True

        
    except Error as e:
        print(f"An error occurred while inserting student: {e}")
        if connection:
            connection.rollback()
        return False

            
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_student_by_roll_no(roll_no: int) -> Optional[Student]:
    connection = None
    cursor = None

    try:
        connection = connect_database()
        if connection is None:
            print("Database connection unavailable.")
            return None

        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM students WHERE roll_no = %s"

        cursor.execute(query, (roll_no,))
        row = cursor.fetchone()

        if row:
            return _row_to_student(row)
        return None

    except Error as e:
        print(f"An error occurred while fetching student by roll number: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_student_by_id(student_id: int) -> Optional[Student]:
    connection = None
    cursor = None

    try:
        connection = connect_database()
        if connection is None:
            print("Database connection unavailable.")
            return None

        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM students WHERE student_id = %s"

        cursor.execute(query, (student_id,))
        row = cursor.fetchone()

        if row:
            return _row_to_student(row)
        return None

    except Error as e:
        print(f"An error occurred while fetching student by id: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def get_all_students() -> List[Student]:
    connection = None
    cursor = None

    try:
        connection = connect_database()
        if connection is None:
            print("Database connection unavailable.")
            return []

        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM students"

        cursor.execute(query)
        rows = cursor.fetchall()

        return [_row_to_student(row) for row in rows]

    except Error as e:
        print(f"An error occurred while fetching all students: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def update_student(student: Student) -> bool:
    connection = None
    cursor = None

    try:
        connection = connect_database()
        if connection is None:
            print("Database connection unavailable.")
            return False

        cursor = connection.cursor()
        query = ("""UPDATE students SET 
            first_name = %s,
            last_name = %s,
            gender = %s,
            dob = %s,
            `class` = %s,
            section = %s,
            roll_no = %s,
            email = %s,
            phone = %s,
            address = %s,
            admission_date = %s
            WHERE student_id = %s""")

        values = (
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
            student.student_id,
        )

        cursor.execute(query, values)
        connection.commit()

        if cursor.rowcount > 0:
            print(f"Student '{student.get_full_name()}' updated successfully.")
            return True
        else:
            print("No student record was updated (ID might not exist).")
            return False

    except Error as e:
        print(f"An error occurred while updating student: {e}")
        if connection:
            connection.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def delete_student(student_id: int) -> bool:
    connection = None
    cursor = None

    try:
        connection = connect_database()
        if connection is None:
            print("Database connection unavailable.")
            return False

        cursor = connection.cursor()
        query = "DELETE FROM students WHERE student_id = %s"

        cursor.execute(query, (student_id,))
        connection.commit()

        if cursor.rowcount > 0:
            print(f"Deleted student with id {student_id}.")
            return True
        else:
            print(f"No student found with ID {student_id} to delete.")
            return False

    except Error as e:
        print(f"An error occurred while deleting student: {e}")
        if connection:
            connection.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
