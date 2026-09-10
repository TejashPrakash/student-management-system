import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import main
from errors import StudentRepositoryError
from student import Student


def capture(func, *args, **kwargs):
    """Run func, returning (result, stdout)."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        result = func(*args, **kwargs)
    return result, buffer.getvalue()


class PromptStudentTests(unittest.TestCase):
    def test_collects_fields_into_a_student(self):
        with mock.patch.object(main, "get_text", side_effect=[
                    "Ada", "Lovelace", "10", "A", "London"]), \
                mock.patch.object(main, "get_choice", return_value="Female"), \
                mock.patch.object(main, "get_date", side_effect=[
                    "1815-12-10", "2024-01-01"]), \
                mock.patch.object(main, "get_positive_int", return_value=7), \
                mock.patch.object(main, "get_email", return_value="ada@example.com"), \
                mock.patch.object(main, "get_phone", return_value="1234567890"):
            student = main._prompt_student(student_id=None)

        self.assertIsInstance(student, Student)
        self.assertIsNone(student.student_id)
        self.assertEqual(student.first_name, "Ada")
        self.assertEqual(student.last_name, "Lovelace")
        self.assertEqual(student.gender, "Female")
        self.assertEqual(student.dob, "1815-12-10")
        self.assertEqual(student.class_name, "10")
        self.assertEqual(student.section, "A")
        self.assertEqual(student.roll_no, 7)
        self.assertEqual(student.email, "ada@example.com")
        self.assertEqual(student.phone, "1234567890")
        self.assertEqual(student.address, "London")
        self.assertEqual(student.admission_date, "2024-01-01")

    def test_keeps_supplied_student_id(self):
        with mock.patch.object(main, "get_text", return_value="x"), \
                mock.patch.object(main, "get_choice", return_value="Male"), \
                mock.patch.object(main, "get_date", return_value="2024-01-01"), \
                mock.patch.object(main, "get_positive_int", return_value=1), \
                mock.patch.object(main, "get_email", return_value="a@b.co"), \
                mock.patch.object(main, "get_phone", return_value="123456"):
            student = main._prompt_student(student_id=42)
        self.assertEqual(student.student_id, 42)


class HandleChoiceAddTests(unittest.TestCase):
    def test_add_student(self):
        student = mock.Mock()
        with mock.patch.object(main, "_prompt_student", return_value=student), \
                mock.patch.object(main, "insert_student") as insert:
            result, output = capture(main.handle_choice, "1")

        insert.assert_called_once_with(student)
        self.assertTrue(result)
        self.assertIn("Student added successfully!", output)

    def test_add_student_propagates_repository_error(self):
        with mock.patch.object(main, "_prompt_student", return_value=mock.Mock()), \
                mock.patch.object(
                    main, "insert_student", side_effect=StudentRepositoryError("db down")
                ):
            with self.assertRaises(StudentRepositoryError):
                main.handle_choice("1")


class HandleChoiceSearchTests(unittest.TestCase):
    def test_search_by_roll_no_found(self):
        found = mock.Mock()
        with mock.patch.object(main, "get_positive_int", return_value=7), \
                mock.patch.object(main, "get_student_by_roll_no", return_value=found) as getter:
            result, _ = capture(main.handle_choice, "2")
        getter.assert_called_once_with(7)
        found.display_info.assert_called_once()
        self.assertTrue(result)

    def test_search_by_roll_no_not_found(self):
        with mock.patch.object(main, "get_positive_int", return_value=7), \
                mock.patch.object(main, "get_student_by_roll_no", return_value=None):
            _, output = capture(main.handle_choice, "2")
        self.assertIn("Student not found.", output)

    def test_search_by_id_found(self):
        found = mock.Mock()
        with mock.patch.object(main, "get_positive_int", return_value=5), \
                mock.patch.object(main, "get_student_by_id", return_value=found) as getter:
            capture(main.handle_choice, "3")
        getter.assert_called_once_with(5)
        found.display_info.assert_called_once()

    def test_search_by_id_not_found(self):
        with mock.patch.object(main, "get_positive_int", return_value=5), \
                mock.patch.object(main, "get_student_by_id", return_value=None):
            _, output = capture(main.handle_choice, "3")
        self.assertIn("Student not found.", output)


class HandleChoiceViewAllTests(unittest.TestCase):
    def test_lists_all_students(self):
        s1, s2 = mock.Mock(), mock.Mock()
        with mock.patch.object(main, "get_all_students", return_value=[s1, s2]):
            capture(main.handle_choice, "4")
        s1.display_info.assert_called_once()
        s2.display_info.assert_called_once()

    def test_no_students(self):
        with mock.patch.object(main, "get_all_students", return_value=[]):
            _, output = capture(main.handle_choice, "4")
        self.assertIn("No student found.", output)


class HandleChoiceUpdateTests(unittest.TestCase):
    def test_update_success(self):
        prompted = mock.Mock()
        with mock.patch.object(main, "get_positive_int", return_value=5), \
                mock.patch.object(main, "get_student_by_id", return_value=mock.Mock()), \
                mock.patch.object(main, "_prompt_student", return_value=prompted), \
                mock.patch.object(main, "update_student", return_value=True) as upd:
            _, output = capture(main.handle_choice, "5")
        upd.assert_called_once_with(prompted)
        self.assertIn("Student updated successfully.", output)

    def test_update_no_row_matched(self):
        with mock.patch.object(main, "get_positive_int", return_value=5), \
                mock.patch.object(main, "get_student_by_id", return_value=mock.Mock()), \
                mock.patch.object(main, "_prompt_student", return_value=mock.Mock()), \
                mock.patch.object(main, "update_student", return_value=False):
            _, output = capture(main.handle_choice, "5")
        self.assertIn("No student record was updated", output)

    def test_update_student_not_found(self):
        with mock.patch.object(main, "get_positive_int", return_value=5), \
                mock.patch.object(main, "get_student_by_id", return_value=None):
            _, output = capture(main.handle_choice, "5")
        self.assertIn("Student not found.", output)


class HandleChoiceDeleteTests(unittest.TestCase):
    def test_delete_confirmed_success(self):
        with mock.patch.object(main, "get_positive_int", return_value=5), \
                mock.patch.object(main, "get_student_by_id", return_value=mock.Mock()), \
                mock.patch.object(main, "input", return_value="Y"), \
                mock.patch.object(main, "delete_student", return_value=True) as delete:
            _, output = capture(main.handle_choice, "6")
        delete.assert_called_once_with(5)
        self.assertIn("Student deleted successfully.", output)

    def test_delete_confirmed_no_row(self):
        with mock.patch.object(main, "get_positive_int", return_value=5), \
                mock.patch.object(main, "get_student_by_id", return_value=mock.Mock()), \
                mock.patch.object(main, "input", return_value="y"), \
                mock.patch.object(main, "delete_student", return_value=False):
            _, output = capture(main.handle_choice, "6")
        self.assertIn("No student found with ID 5 to delete.", output)

    def test_delete_cancelled(self):
        with mock.patch.object(main, "get_positive_int", return_value=5), \
                mock.patch.object(main, "get_student_by_id", return_value=mock.Mock()), \
                mock.patch.object(main, "input", return_value="N"), \
                mock.patch.object(main, "delete_student") as delete:
            _, output = capture(main.handle_choice, "6")
        delete.assert_not_called()
        self.assertIn("Deletion cancelled.", output)

    def test_delete_student_not_found(self):
        with mock.patch.object(main, "get_positive_int", return_value=5), \
                mock.patch.object(main, "get_student_by_id", return_value=None):
            _, output = capture(main.handle_choice, "6")
        self.assertIn("Student not found.", output)


class HandleChoiceControlTests(unittest.TestCase):
    def test_exit_returns_false(self):
        result, output = capture(main.handle_choice, "7")
        self.assertFalse(result)
        self.assertIn("Thank you for using EduTrack!", output)

    def test_unknown_choice_continues(self):
        result, output = capture(main.handle_choice, "99")
        self.assertTrue(result)
        self.assertIn("Feature coming soon...", output)


class MainLoopTests(unittest.TestCase):
    def test_exits_cleanly_on_quit(self):
        with mock.patch.object(main, "input", return_value="7"):
            result, _ = capture(main.main)
        self.assertEqual(result, 0)

    def test_recovers_from_edutrack_error_then_exits(self):
        with mock.patch.object(main, "input", side_effect=["1", "7"]), \
                mock.patch.object(
                    main, "handle_choice",
                    side_effect=[StudentRepositoryError("boom"), False],
                ):
            result, _ = capture(main.main)
        self.assertEqual(result, 0)

    def test_handles_eof(self):
        with mock.patch.object(main, "input", side_effect=EOFError):
            result, output = capture(main.main)
        self.assertEqual(result, 130)
        self.assertIn("Interrupted", output)


if __name__ == "__main__":
    unittest.main()
