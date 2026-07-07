class Student:
    """
    Represents a student in the EduTrack system.
    """
    def __init__(self, student_id, first_name, last_name, gender, 
                 dob, class_name, section, roll_no, email, phone,
                 address, admission_date):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.dob = dob
        self.class_name = class_name
        self.section = section
        self.roll_no = roll_no
        self.email = email
        self.phone = phone
        self.address = address
        self.admission_date = admission_date
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
        
    def display_info(self):
        print("=" * 40)
        print(f"STUDENT PROFILE : {self.get_full_name()}")
        print("=" * 40)
        print(f"Student ID      : {self.student_id}")
        print(f"Roll No         : {self.roll_no}")
        print(f"Gender          : {self.gender}")
        print(f"Date of Birth   : {self.dob}")
        print(f"Class & Section : {self.class_name} - {self.section}")
        print(f"Email           : {self.email}")
        print(f"Phone           : {self.phone}")
        print(f"Address         : {self.address}")
        print(f"Admission Date  : {self.admission_date}")
        print("=" * 40)        