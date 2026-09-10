import logging
from contextlib import contextmanager
from typing import List, Optional

from mysql.connector import Error

from database import close_quietly, connect_database
from errors import StudentRepositoryError
from student import Student

logger = logging.getLogger(__name__)


@contextmanager
def _cursor(dictionary: bool = True):
    """Yield a cursor, always closing the cursor and connection afterwards."""
    connection = connect_database()
    cursor = None
    try:
        cursor = connection.cursor(dictionary=dictionary)
        yield connection, cursor
    finally:
        close_quietly(cursor)
        close_quietly(connection)


def _rollback(connection) -> None:
    try:
        connection.rollback()
    except Error:
        logger.warning("Rollback failed after a database error.", exc_info=True)


def _row_to_student(row: dict) -> Student:
    try:
        return Student(
            student_id=row["student_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            gender=row["gender"],
            dob=row["dob"],
            class_name=row["class"],
            section=row["section"],
            roll_no=row["roll_no"],
            email=row["email"],
            phone=row["phone"],
            address=row["address"],
            admission_date=row["admission_date"],
        )
    except KeyError as exc:
        raise StudentRepositoryError(
            f"Student row is missing the column {exc.args[0]!r}; "
            "the database schema may be out of date."
        ) from exc


# Column order shared by INSERT and UPDATE. The database column is `class`;
# the matching Student attribute is `class_name`.
_STUDENT_COLUMNS = (
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

_INSERT_QUERY = (
    "INSERT INTO students ("
    + ", ".join(f"`{column}`" for column in _STUDENT_COLUMNS)
    + ") VALUES ("
    + ", ".join(["%s"] * len(_STUDENT_COLUMNS))
    + ")"
)

_UPDATE_QUERY = (
    "UPDATE students SET "
    + ", ".join(f"`{column}` = %s" for column in _STUDENT_COLUMNS)
    + " WHERE student_id = %s"
)


def _student_values(student: Student) -> tuple:
    """Return the student's field values in _STUDENT_COLUMNS order."""
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


def insert_student(student: Student) -> int:
    """Insert a student and return the generated student id.

    Raises:
        DatabaseConnectionError: the database is unreachable.
        StudentRepositoryError: the insert failed.
    """
    with _cursor() as (connection, cursor):
        try:
            cursor.execute(_INSERT_QUERY, _student_values(student))
            connection.commit()
        except Error as exc:
            _rollback(connection)
            raise StudentRepositoryError(
                f"Could not add student '{student.get_full_name()}': {exc}"
            ) from exc

        student.student_id = cursor.lastrowid
        logger.info(
            "Added student '%s' with id %s.", student.get_full_name(), student.student_id
        )
        return student.student_id


def get_student_by_roll_no(roll_no: int) -> Optional[Student]:
    """Return the student with this roll number, or None when there is none."""
    with _cursor() as (_, cursor):
        try:
            cursor.execute("SELECT * FROM students WHERE roll_no = %s", (roll_no,))
            row = cursor.fetchone()
        except Error as exc:
            raise StudentRepositoryError(
                f"Could not fetch the student with roll number {roll_no}: {exc}"
            ) from exc

        return _row_to_student(row) if row else None


def get_student_by_id(student_id: int) -> Optional[Student]:
    """Return the student with this id, or None when there is none."""
    with _cursor() as (_, cursor):
        try:
            cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
            row = cursor.fetchone()
        except Error as exc:
            raise StudentRepositoryError(
                f"Could not fetch the student with id {student_id}: {exc}"
            ) from exc

        return _row_to_student(row) if row else None


def get_all_students() -> List[Student]:
    """Return every student; an empty list means the table is empty."""
    with _cursor() as (_, cursor):
        try:
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
        except Error as exc:
            raise StudentRepositoryError(f"Could not fetch the students: {exc}") from exc

        return [_row_to_student(row) for row in rows]


def update_student(student: Student) -> bool:
    """Update a student; return False when no record matched the student id."""
    with _cursor(dictionary=False) as (connection, cursor):
        try:
            cursor.execute(_UPDATE_QUERY, _student_values(student) + (student.student_id,))
            connection.commit()
        except Error as exc:
            _rollback(connection)
            raise StudentRepositoryError(
                f"Could not update the student with id {student.student_id}: {exc}"
            ) from exc

        return cursor.rowcount > 0


def delete_student(student_id: int) -> bool:
    """Delete a student; return False when no record matched the student id."""
    with _cursor(dictionary=False) as (connection, cursor):
        try:
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            connection.commit()
        except Error as exc:
            _rollback(connection)
            raise StudentRepositoryError(
                f"Could not delete the student with id {student_id}: {exc}"
            ) from exc

        return cursor.rowcount > 0
