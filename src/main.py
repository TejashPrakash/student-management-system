from student import Student
from student_repository import (
    insert_student,
    get_student_by_roll_no,
    get_student_by_id,
    get_all_students,
    update_student,
    delete_student
    )
def main():
    
    while True:
        print()
        print("=" * 40)
        print("                EDUTRACK                ")
        print("        Student Management System       ")
        print("=" * 40)
        print("1.  Add Student")
        print("2.  Search Student by Roll Number")
        print("3.  Search Student by Student ID")
        print("4.  View All Students")
        print("5.  Update Student")
        print("6.  Delete Student")
        print("7.  Exit")
        print("=" * 40)
        
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            print("You have selected to add a student...")
            first_name = input("Enter First Name: ").strip()
            last_name = input("Enter Last Name: ").strip()
            gender = input("Enter Gender (Male/Female/Other): ").strip()
            dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
            class_name = input("Enter Class: ").strip()
            section = input("Enter Section: ").strip()
            roll_no = int(input("Enter Roll Number: "))
            email = input("Enter Email: ").strip()
            phone = input("Enter Phone Number: ").strip()
            address = input("Enter Address: ")
            admission_date = input("Enter Admission Date (YYYY-MM-DD): ")
            
            student = Student(
                student_id=None,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                dob=dob,
                class_name=class_name,
                section=section,
                roll_no=roll_no,
                email=email,
                phone=phone,
                address=address,
                admission_date=admission_date
            )
            insert_student(student)
            print("\nStudent added successfully!\n")
            
        elif choice == "2":
            print("You have selected to search a student by Roll Number")
            roll_no = int(input("Enter Roll Number: "))
        
            student = get_student_by_roll_no(roll_no)
        
            if student:
                student.display_info()
            else:
                print("Student not found.")
        
        elif choice == "3":
            print("You have selected to search a student by Student ID.")
            student_id = int(input("Enter Student ID: "))
            
            student = get_student_by_id(student_id)
            
            if student:
                student.display_info()
            else:
                print("Student not found.")
        
        elif choice == "4":
            print("You have selected to View All Students.")
            students = get_all_students()
            if not students:
                print("No student found.")
            else:
                for student in students:
                    student.display_info()
        
        elif choice == "5":
            print("You have selected to update a student.")
            student_id = int(input("Enter Student ID: "))
            
            student = get_student_by_id(student_id)
            
            if student:
                print("\nCurrent Student Details:")
                student.display_info()
                print("Enter the Updated Details: ")
                first_name = input("Enter First Name: ").strip()
                last_name = input("Enter Last Name: ").strip()
                gender = input("Enter Gender (Male/Female/Other): ").strip()
                dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
                class_name = input("Enter Class: ").strip()
                section = input("Enter Section: ").strip()
                roll_no = int(input("Enter Roll Number: "))
                email = input("Enter Email: ").strip()
                phone = input("Enter Phone Number: ").strip()
                address = input("Enter Address: ")
                admission_date = input("Enter Admission Date (YYYY-MM-DD): ")
                
                student = Student(
                    student_id=student_id,
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    dob=dob,
                    class_name=class_name,
                    section=section,
                    roll_no=roll_no,
                    email=email,
                    phone=phone,
                    address=address,
                    admission_date=admission_date
                )
                
                success = update_student(student)
                
                if success:
                    print("Student updated successfully.")
                else:
                    print("Failed to update student.")
            else:
                print("Student not found.")
                
        elif choice == "6":
            print("You have selected to delete the entry of a student.")
            student_id = int(input("Enter Student ID: "))
            
            student = get_student_by_id(student_id)
            
            if student:
                print("\nCurrent Student Details:")
                student.display_info()
                ch = input("Are you sure you want to delete this student? (Y/N): ")
                if ch.strip().upper() == "Y":
                    success = delete_student(student_id)

                    if success:
                        print("Student deleted successfully.")
                    else:
                        print("Failed to delete student.")
                else:
                    print("Deletion cancelled.")
                
            else:
                print("Student not found.")
            
        elif choice == "7":
            print("\nThank you for using EduTrack!")
            break
        else:
            print("\nFeature coming soon...")
        
if __name__ == "__main__":
    main()