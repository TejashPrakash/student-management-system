import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from student import Student


def make_student(**overrides):
    defaults = dict(
        student_id=1,
        first_name="Ada",
        last_name="Lovelace",
        gender="Female",
        dob="1815-12-10",
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


class StudentInitTests(unittest.TestCase):
    def test_stores_all_attributes(self):
        student = make_student()
        self.assertEqual(student.student_id, 1)
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


class GetFullNameTests(unittest.TestCase):
    def test_joins_first_and_last_name(self):
        self.assertEqual(make_student().get_full_name(), "Ada Lovelace")

    def test_handles_empty_names(self):
        student = make_student(first_name="", last_name="")
        self.assertEqual(student.get_full_name(), " ")


class DisplayInfoTests(unittest.TestCase):
    def test_prints_all_fields(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            make_student().display_info()
        output = buffer.getvalue()

        self.assertIn("STUDENT PROFILE : Ada Lovelace", output)
        self.assertIn("Student ID      : 1", output)
        self.assertIn("Roll No         : 7", output)
        self.assertIn("Gender          : Female", output)
        self.assertIn("Date of Birth   : 1815-12-10", output)
        self.assertIn("Class & Section : 10 - A", output)
        self.assertIn("Email           : ada@example.com", output)
        self.assertIn("Phone           : 1234567890", output)
        self.assertIn("Address         : London", output)
        self.assertIn("Admission Date  : 2024-01-01", output)


if __name__ == "__main__":
    unittest.main()
