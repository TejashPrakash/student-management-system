import sys
import unittest
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import database
import student_repository as repo
from student import Student


def make_student(student_id=1):
    return Student(
        student_id=student_id,
        first_name="Ann",
        last_name="Lee",
        gender="Female",
        dob="2000-01-01",
        class_name="10",
        section="A",
        roll_no=5,
        email="ann@example.com",
        phone="123456",
        address="1 Main St",
        admission_date="2020-01-01",
    )


ROW = {
    "student_id": 1,
    "first_name": "Ann",
    "last_name": "Lee",
    "gender": "Female",
    "dob": "2000-01-01",
    "class": "10",
    "section": "A",
    "roll_no": 5,
    "email": "ann@example.com",
    "phone": "123456",
    "address": "1 Main St",
    "admission_date": "2020-01-01",
}


class FakeCursor:
    def __init__(self, row=None, rows=None, rowcount=1):
        self._row = row
        self._rows = rows or []
        self.rowcount = rowcount
        self.executed = []
        self.closed = False

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchone(self):
        return self._row

    def fetchall(self):
        return self._rows

    def close(self):
        self.closed = True


class FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def cursor(self, dictionary=False):
        return self._cursor

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True


class RepositoryTests(unittest.TestCase):
    def _patch_connection(self, connection):
        return mock.patch.object(database, "connect_database", return_value=connection)

    def test_insert_student_commits_and_closes(self):
        cursor = FakeCursor()
        conn = FakeConnection(cursor)
        with self._patch_connection(conn):
            self.assertTrue(repo.insert_student(make_student()))
        self.assertTrue(conn.committed)
        self.assertTrue(cursor.closed)
        self.assertTrue(conn.closed)

    def test_get_student_by_id_maps_class_column(self):
        cursor = FakeCursor(row=ROW)
        conn = FakeConnection(cursor)
        with self._patch_connection(conn):
            student = repo.get_student_by_id(1)
        self.assertEqual(student.class_name, "10")
        self.assertEqual(student.get_full_name(), "Ann Lee")

    def test_get_all_students_returns_list(self):
        cursor = FakeCursor(rows=[ROW, ROW])
        conn = FakeConnection(cursor)
        with self._patch_connection(conn):
            students = repo.get_all_students()
        self.assertEqual(len(students), 2)

    def test_update_reports_missing_row(self):
        cursor = FakeCursor(rowcount=0)
        conn = FakeConnection(cursor)
        with self._patch_connection(conn):
            self.assertFalse(repo.update_student(make_student()))

    def test_delete_student_success(self):
        cursor = FakeCursor(rowcount=1)
        conn = FakeConnection(cursor)
        with self._patch_connection(conn):
            self.assertTrue(repo.delete_student(1))

    def test_error_triggers_rollback(self):
        cursor = FakeCursor()
        cursor.execute = mock.Mock(side_effect=database.Error("boom"))
        conn = FakeConnection(cursor)
        with self._patch_connection(conn):
            self.assertFalse(repo.insert_student(make_student()))
        self.assertTrue(conn.rolled_back)
        self.assertTrue(conn.closed)

    def test_connection_unavailable_is_handled(self):
        with self._patch_connection(None):
            self.assertFalse(repo.insert_student(make_student()))
            self.assertIsNone(repo.get_student_by_id(1))
            self.assertEqual(repo.get_all_students(), [])


if __name__ == "__main__":
    unittest.main()
