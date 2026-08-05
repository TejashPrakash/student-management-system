import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import student_repository as repo
from student import Student
from mysql.connector import Error


SAMPLE_ROW = {
    "student_id": 5,
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
    "phone": "1234567890",
    "phone": "555",
    "address": "London",
    "admission_date": "2024-01-01",
}


def make_student(**overrides):
    defaults = dict(
        student_id=5,
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
        last_name="Hella",
        gender="Female",
        dob="2012-12-10",
        class_name="10",
        section="A",
        roll_no=7,
        email="ada@example.com",
        phone="1234567890",
        address="London",
        admission_date="2024-01-01",
    )
    defaults.update(overrides)
    return Student(**defaults)


def make_connection(cursor):
    """Build a fake DB connection whose .cursor(...) returns the given cursor."""
    connection = mock.Mock()
    connection.cursor.return_value = cursor
    return connection


class RowToStudentTests(unittest.TestCase):
    def test_maps_columns_including_class_alias(self):
        student = repo._row_to_student(SAMPLE_ROW)
        self.assertIsInstance(student, Student)
        self.assertEqual(student.student_id, 5)
        self.assertEqual(student.class_name, "10")
        self.assertEqual(student.get_full_name(), "Ada Lovelace")

    def test_missing_keys_default_to_none(self):
        student = repo._row_to_student({})
        self.assertIsNone(student.student_id)
        self.assertIsNone(student.class_name)


class InsertStudentTests(unittest.TestCase):
    def test_inserts_and_commits(self):
        cursor = mock.Mock()
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            result = repo.insert_student(make_student())

        self.assertTrue(result)
        cursor.execute.assert_called_once()
        connection.commit.assert_called_once()
        cursor.close.assert_called_once()
        connection.close.assert_called_once()

    def test_returns_false_when_no_connection(self):
        with mock.patch.object(repo, "connect_database", return_value=None):
            self.assertFalse(repo.insert_student(make_student()))

    def test_rolls_back_on_error(self):
        cursor = mock.Mock()
        cursor.execute.side_effect = Error("insert failed")
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            result = repo.insert_student(make_student())

        self.assertFalse(result)
        connection.rollback.assert_called_once()
        connection.close.assert_called_once()


class GetStudentByRollNoTests(unittest.TestCase):
    def test_returns_student_when_found(self):
        cursor = mock.Mock()
        cursor.fetchone.return_value = SAMPLE_ROW
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            student = repo.get_student_by_roll_no(7)

        self.assertIsInstance(student, Student)
        self.assertEqual(student.roll_no, 7)
        cursor.execute.assert_called_once_with(
            "SELECT * FROM students WHERE roll_no = %s", (7,)
        )

    def test_returns_none_when_not_found(self):
        cursor = mock.Mock()
        cursor.fetchone.return_value = None
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            self.assertIsNone(repo.get_student_by_roll_no(999))

    def test_returns_none_when_no_connection(self):
        with mock.patch.object(repo, "connect_database", return_value=None):
            self.assertIsNone(repo.get_student_by_roll_no(7))

    def test_returns_none_on_error(self):
        cursor = mock.Mock()
        cursor.execute.side_effect = Error("boom")
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            self.assertIsNone(repo.get_student_by_roll_no(7))


class GetStudentByIdTests(unittest.TestCase):
    def test_returns_student_when_found(self):
        cursor = mock.Mock()
        cursor.fetchone.return_value = SAMPLE_ROW
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            student = repo.get_student_by_id(5)

        self.assertEqual(student.student_id, 5)
        cursor.execute.assert_called_once_with(
            "SELECT * FROM students WHERE student_id = %s", (5,)
        )

    def test_returns_none_when_not_found(self):
        cursor = mock.Mock()
        cursor.fetchone.return_value = None
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            self.assertIsNone(repo.get_student_by_id(5))

    def test_returns_none_when_no_connection(self):
        with mock.patch.object(repo, "connect_database", return_value=None):
            self.assertIsNone(repo.get_student_by_id(5))

    def test_returns_none_on_error(self):
        cursor = mock.Mock()
        cursor.execute.side_effect = Error("boom")
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            self.assertIsNone(repo.get_student_by_id(5))


class GetAllStudentsTests(unittest.TestCase):
    def test_returns_list_of_students(self):
        cursor = mock.Mock()
        cursor.fetchall.return_value = [SAMPLE_ROW, {**SAMPLE_ROW, "student_id": 6}]
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            students = repo.get_all_students()

        self.assertEqual(len(students), 2)
        self.assertTrue(all(isinstance(s, Student) for s in students))
        self.assertEqual(students[1].student_id, 6)

    def test_returns_empty_list_when_no_connection(self):
        with mock.patch.object(repo, "connect_database", return_value=None):
            self.assertEqual(repo.get_all_students(), [])

    def test_returns_empty_list_on_error(self):
        cursor = mock.Mock()
        cursor.execute.side_effect = Error("boom")
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            self.assertEqual(repo.get_all_students(), [])


class UpdateStudentTests(unittest.TestCase):
    def test_returns_true_when_row_updated(self):
        cursor = mock.Mock()
        cursor.rowcount = 1
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            result = repo.update_student(make_student())

        self.assertTrue(result)
        connection.commit.assert_called_once()

    def test_returns_false_when_no_row_updated(self):
        cursor = mock.Mock()
        cursor.rowcount = 0
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            self.assertFalse(repo.update_student(make_student()))

    def test_returns_false_when_no_connection(self):
        with mock.patch.object(repo, "connect_database", return_value=None):
            self.assertFalse(repo.update_student(make_student()))

    def test_rolls_back_on_error(self):
        cursor = mock.Mock()
        cursor.execute.side_effect = Error("boom")
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            self.assertFalse(repo.update_student(make_student()))
        connection.rollback.assert_called_once()


class DeleteStudentTests(unittest.TestCase):
    def test_returns_true_when_row_deleted(self):
        cursor = mock.Mock()
        cursor.rowcount = 1
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            result = repo.delete_student(5)

        self.assertTrue(result)
        cursor.execute.assert_called_once_with(
            "DELETE FROM students WHERE student_id = %s", (5,)
        )
        connection.commit.assert_called_once()

    def test_returns_false_when_no_row_deleted(self):
        cursor = mock.Mock()
        cursor.rowcount = 0
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            self.assertFalse(repo.delete_student(5))

    def test_returns_false_when_no_connection(self):
        with mock.patch.object(repo, "connect_database", return_value=None):
            self.assertFalse(repo.delete_student(5))

    def test_rolls_back_on_error(self):
        cursor = mock.Mock()
        cursor.execute.side_effect = Error("boom")
        connection = make_connection(cursor)
        with mock.patch.object(repo, "connect_database", return_value=connection):
            self.assertFalse(repo.delete_student(5))
        connection.rollback.assert_called_once()
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
