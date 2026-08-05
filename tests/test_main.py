import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import main
from student import Student


def run_main(inputs):
    """Run main.main() feeding the given console inputs, returning stdout.

    Both plain ``input`` calls and ``get_positive_int`` (which otherwise binds
    the real builtin ``input``) are driven from one shared iterator so the
    scripted answers are consumed in order.
    """
    buffer = io.StringIO()
    stream = iter(inputs)

    def fake_input(prompt=""):
        return next(stream)

    def fake_positive_int(prompt, *args, **kwargs):
        return int(next(stream))

    with mock.patch.object(main, "input", side_effect=fake_input), \
            mock.patch.object(main, "get_positive_int", side_effect=fake_positive_int):
        with redirect_stdout(buffer):
            main.main()
    return buffer.getvalue()


ADD_INPUTS = [
    "1",
    "Ada",            # first name
    "Lovelace",       # last name
    "Female",         # gender
    "1815-12-10",     # dob
    "10",             # class
    "A",              # section
    "7",              # roll no (positive int)
    "ada@example.com",
    "123",            # phone
    "London",         # address
    "2024-01-01",     # admission date
    "7",              # exit
]


class ExitTests(unittest.TestCase):
    def test_exit_prints_goodbye(self):
        output = run_main(["7"])
        self.assertIn("Thank you for using EduTrack!", output)

    def test_invalid_choice_shows_coming_soon(self):
        output = run_main(["99", "7"])
        self.assertIn("Feature coming soon...", output)


class AddStudentTests(unittest.TestCase):
    def test_add_student_success(self):
        with mock.patch.object(main, "insert_student", return_value=True) as insert:
            output = run_main(ADD_INPUTS)

        insert.assert_called_once()
        student = insert.call_args.args[0]
        self.assertIsInstance(student, Student)
        self.assertEqual(student.first_name, "Ada")
        self.assertEqual(student.roll_no, 7)
        self.assertIsNone(student.student_id)
        self.assertIn("Student added successfully!", output)

    def test_add_student_failure(self):
        with mock.patch.object(main, "insert_student", return_value=False):
            output = run_main(ADD_INPUTS)
        self.assertIn("could not be added", output)


class SearchByRollNoTests(unittest.TestCase):
    def test_found_displays_student(self):
        found = mock.Mock()
        with mock.patch.object(main, "get_student_by_roll_no", return_value=found) as getter:
            run_main(["2", "7", "7"])
        getter.assert_called_once_with(7)
        found.display_info.assert_called_once()

    def test_not_found(self):
        with mock.patch.object(main, "get_student_by_roll_no", return_value=None):
            output = run_main(["2", "7", "7"])
        self.assertIn("Student not found.", output)


class SearchByIdTests(unittest.TestCase):
    def test_found_displays_student(self):
        found = mock.Mock()
        with mock.patch.object(main, "get_student_by_id", return_value=found) as getter:
            run_main(["3", "5", "7"])
        getter.assert_called_once_with(5)
        found.display_info.assert_called_once()

    def test_not_found(self):
        with mock.patch.object(main, "get_student_by_id", return_value=None):
            output = run_main(["3", "5", "7"])
        self.assertIn("Student not found.", output)


class ViewAllTests(unittest.TestCase):
    def test_lists_all_students(self):
        s1, s2 = mock.Mock(), mock.Mock()
        with mock.patch.object(main, "get_all_students", return_value=[s1, s2]):
            run_main(["4", "7"])
        s1.display_info.assert_called_once()
        s2.display_info.assert_called_once()

    def test_no_students(self):
        with mock.patch.object(main, "get_all_students", return_value=[]):
            output = run_main(["4", "7"])
        self.assertIn("No student found.", output)


UPDATE_INPUTS = [
    "5",              # menu: update
    "5",              # student id
    "Grace",          # first name
    "Hopper",         # last name
    "Female",
    "1906-12-09",
    "12",
    "B",
    "9",              # roll no
    "grace@example.com",
    "456",
    "New York",
    "2024-02-02",
    "7",              # exit
]


class UpdateStudentTests(unittest.TestCase):
    def test_update_success(self):
        existing = mock.Mock()
        with mock.patch.object(main, "get_student_by_id", return_value=existing), \
                mock.patch.object(main, "update_student", return_value=True) as upd:
            output = run_main(UPDATE_INPUTS)

        upd.assert_called_once()
        updated = upd.call_args.args[0]
        self.assertEqual(updated.student_id, 5)
        self.assertEqual(updated.first_name, "Grace")
        self.assertIn("Student updated successfully.", output)

    def test_update_failure(self):
        existing = mock.Mock()
        with mock.patch.object(main, "get_student_by_id", return_value=existing), \
                mock.patch.object(main, "update_student", return_value=False):
            output = run_main(UPDATE_INPUTS)
        self.assertIn("Failed to update student.", output)

    def test_update_student_not_found(self):
        with mock.patch.object(main, "get_student_by_id", return_value=None):
            output = run_main(["5", "5", "7"])
        self.assertIn("Student not found.", output)


class DeleteStudentTests(unittest.TestCase):
    def test_delete_confirmed_success(self):
        existing = mock.Mock()
        with mock.patch.object(main, "get_student_by_id", return_value=existing), \
                mock.patch.object(main, "delete_student", return_value=True) as delete:
            output = run_main(["6", "5", "Y", "7"])
        delete.assert_called_once_with(5)
        self.assertIn("Student deleted successfully.", output)

    def test_delete_confirmed_failure(self):
        existing = mock.Mock()
        with mock.patch.object(main, "get_student_by_id", return_value=existing), \
                mock.patch.object(main, "delete_student", return_value=False):
            output = run_main(["6", "5", "y", "7"])
        self.assertIn("Failed to delete student.", output)

    def test_delete_cancelled(self):
        existing = mock.Mock()
        with mock.patch.object(main, "get_student_by_id", return_value=existing), \
                mock.patch.object(main, "delete_student") as delete:
            output = run_main(["6", "5", "N", "7"])
        delete.assert_not_called()
        self.assertIn("Deletion cancelled.", output)

    def test_delete_student_not_found(self):
        with mock.patch.object(main, "get_student_by_id", return_value=None):
            output = run_main(["6", "5", "7"])
        self.assertIn("Student not found.", output)


if __name__ == "__main__":
    unittest.main()
