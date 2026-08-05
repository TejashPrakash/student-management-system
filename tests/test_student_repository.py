import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from mysql.connector import Error

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import student_repository
from errors import StudentRepositoryError
from student import Student


ROW = {
    "student_id": 1,
    "first_name": "Ada",
    "last_name": "Lovelace",
    "gender": "Female",
    "dob": "1815-12-10",
    "class": "10",
    "section": "A",
    "roll_no": 7,
    "email": "ada@example.com",
    "phone": "555",
    "address": "London",
    "admission_date": "2024-01-01",
}


class FakeCursor:
    def __init__(self, row=None, rows=None, error=None, rowcount=1, lastrowid=1):
        self._row = row
        self._rows = rows or []
        self._error = error
        self.rowcount = rowcount
        self.lastrowid = lastrowid
        self.closed = False

    def execute(self, query, values=None):
        if self._error:
            raise self._error

    def fetchone(self):
        return self._row

    def fetchall(self):
        return self._rows

    def close(self):
        self.closed = True


class FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor
        self.closed = False
        self.committed = False
        self.rolled_back = False

    def cursor(self, dictionary=False):
        return self._cursor

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True


def make_student(student_id=1):
    return Student(
        student_id=student_id,
        first_name="Ada",
        last_name="Lovelace",
        gender="Female",
        dob="1815-12-10",
        class_name="10",
        section="A",
        roll_no=7,
        email="ada@example.com",
        phone="555",
        address="London",
        admission_date="2024-01-01",
    )


class RepositoryErrorPropagationTests(unittest.TestCase):
    def _patch_connection(self, cursor):
        connection = FakeConnection(cursor)
        patcher = patch.object(
            student_repository, "connect_database", return_value=connection
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        return connection

    def test_query_failure_is_raised_not_reported_as_empty(self):
        cursor = FakeCursor(error=Error("connection lost"))
        connection = self._patch_connection(cursor)

        with self.assertRaises(StudentRepositoryError):
            student_repository.get_all_students()

        self.assertTrue(cursor.closed)
        self.assertTrue(connection.closed)

    def test_insert_failure_rolls_back_and_raises(self):
        cursor = FakeCursor(error=Error("duplicate roll_no"))
        connection = self._patch_connection(cursor)

        with self.assertRaises(StudentRepositoryError):
            student_repository.insert_student(make_student(student_id=None))

        self.assertTrue(connection.rolled_back)

    def test_delete_failure_raises_instead_of_returning_false(self):
        cursor = FakeCursor(error=Error("foreign key constraint"))
        self._patch_connection(cursor)

        with self.assertRaises(StudentRepositoryError):
            student_repository.delete_student(1)

    def test_delete_returns_false_when_no_row_matched(self):
        self._patch_connection(FakeCursor(rowcount=0))

        self.assertFalse(student_repository.delete_student(99))

    def test_update_returns_true_when_a_row_matched(self):
        self._patch_connection(FakeCursor(rowcount=1))

        self.assertTrue(student_repository.update_student(make_student()))

    def test_missing_student_returns_none(self):
        self._patch_connection(FakeCursor(row=None))

        self.assertIsNone(student_repository.get_student_by_id(42))

    def test_row_is_mapped_to_a_student(self):
        self._patch_connection(FakeCursor(row=ROW))

        student = student_repository.get_student_by_roll_no(7)

        self.assertEqual(student.get_full_name(), "Ada Lovelace")
        self.assertEqual(student.class_name, "10")

    def test_incomplete_row_raises_a_descriptive_error(self):
        incomplete = {key: value for key, value in ROW.items() if key != "class"}
        self._patch_connection(FakeCursor(row=incomplete))

        with self.assertRaisesRegex(StudentRepositoryError, "class"):
            student_repository.get_student_by_id(1)

    def test_insert_returns_the_new_student_id(self):
        self._patch_connection(FakeCursor(lastrowid=17))

        self.assertEqual(student_repository.insert_student(make_student(None)), 17)


if __name__ == "__main__":
    unittest.main()
