from student import Student
from student_repository import insert_student
    
if __name__ == "__main__":
    student = Student(
        student_id = None,
        first_name="Rahul",
        last_name="Sharma",
        gender="Male",
        dob="2007-05-14",
        class_name="12",
        section="A",
        roll_no=1,
        email="rahul@example.com",
        phone="8859556561",
        address="Ranchi",
        admission_date="2024-04-01"
        )
        
    student.display_info()
    insert_student(student)    # insert_student(student)

from student_repository import get_student_by_roll_no

student = get_student_by_roll_no(1)

if student:
    student.display_info()
    
from student_repository import get_all_students

students = get_all_students()

if students:
    for student in students:
        student.display_info()