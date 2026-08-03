from database import connect_database
from student import Student
from mysql.connector import Error

def insert_student(student: Student) -> bool:
    
    connection = None
    cursor = None
    
    try:
        connection = connect_database()
        
        if connection is None:
            return
        
        cursor = connection.cursor()
        
        query = """INSERT INTO students (first_name,
        last_name,
        gender,
        dob,
        class,
        section,
        roll_no,
        email,
        phone,
        address,
        admission_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (student.first_name,
                  student.last_name,
                  student.gender,
                  student.dob,
                  student.class_name,
                  student.section,
                  student.roll_no,
                  student.email,
                  student.phone,
                  student.address,
                  student.admission_date
                )
        
        cursor.execute(query, values)
        
        connection.commit()
        
        print(f"Success: Student '{student.get_full_name()}' has been added to the database.")
        return True
        
    except Error as e:
        print(f"An error occured: {e}")
        if connection:
            connection.rollback()
        return False
            
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_student_by_roll_no(roll_no: int) -> Student | None:
    
    connection = None
    cursor = None
    
    try:
        connection = connect_database()
        
        if connection is None:
            return
        
        cursor = connection.cursor()
    
        query = """SELECT * FROM students WHERE roll_no = %s"""
        
        cursor.execute(query, (roll_no,))
        row = cursor.fetchone()
        
        if row:
            student = Student(
                student_id=row[0],
                first_name=row[1],
                last_name=row[2],
                gender=row[3],
                dob=row[4],
                class_name=row[5],
                section=row[6],
                roll_no=row[7],
                email=row[8],
                phone=row[9],
                address=row[10],
                admission_date=row[11]
                )
            return student
        else:
            print("Student not found.")
            return None
            
    except Error as e:
        print(f"An error occured: {e}")
        if connection:
            connection.rollback()
            
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
def get_student_by_id(student_id: int) -> Student | None:
    
    connection = None
    cursor = None
    
    try:
        connection = connect_database()
        
        if connection is None:
            return
        
        cursor = connection.cursor()
    
        query = """SELECT * FROM students WHERE student_id = %s"""
        
        cursor.execute(query, (student_id,))
        row = cursor.fetchone()
        
        if row:
            student = Student(
                student_id=row[0],
                first_name=row[1],
                last_name=row[2],
                gender=row[3],
                dob=row[4],
                class_name=row[5],
                section=row[6],
                roll_no=row[7],
                email=row[8],
                phone=row[9],
                address=row[10],
                admission_date=row[11]
                )
            return student
        else:
            print("Student not found.")
            return None
            
    except Error as e:
        print(f"An error occured: {e}")
        if connection:
            connection.rollback()
            
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
def get_all_students() -> list[Student]:
    
    connection = None
    cursor = None
    
    try:
        connection = connect_database()
        
        if connection is None:
            return
        
        cursor = connection.cursor()
    
        query = """SELECT * FROM students;"""
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        student_list=[]
        
        for row in rows:
            student = Student(
                student_id=row[0],
                first_name=row[1],
                last_name=row[2],
                gender=row[3],
                dob=row[4],
                class_name=row[5],
                section=row[6],
                roll_no=row[7],
                email=row[8],
                phone=row[9],
                address=row[10],
                admission_date=row[11]
                )
            student_list.append(student)
        
        return student_list
    
    except Error as e:
        print(f"An error occured: {e}")
        if connection:
            connection.rollback()
            
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
def update_student(student: Student) -> bool:
    
    connection = None
    cursor = None
    
    try:
        connection = connect_database()
        
        if connection is None:
            return False
        
        cursor = connection.cursor()
        
        query ="""UPDATE students SET 
            first_name = %s,
            last_name = %s,
            gender = %s,
            dob = %s,
            class = %s,
            section = %s,
            roll_no = %s,
            email = %s,
            phone = %s,
            address = %s,
            admission_date = %s
            WHERE student_id = %s;"""
        
        values = (student.first_name,
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
                  student.student_id
                )
        
        cursor.execute(query, values)
        
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Student '{student.get_full_name()}' updated successfully.")
            return True
        else:
            print("No student record was Updated(ID might not exist).")
            return False
    
    except Error as e:
        print(f"An error occured: {e}")
        if connection:
            connection.rollback()
            
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
def delete_student(student_id: int) -> bool:
    
    connection = None
    cursor = None
    
    try:
        connection = connect_database()
        
        if connection is None:
            return False
        
        cursor = connection.cursor()
        
        query = """DELETE FROM students WHERE student_id = %s;"""
        
        cursor.execute(query, (student_id,))
        
        connection.commit()
        
        if cursor.rowcount > 0:
            return True
        else:
            print(f"No student found with ID {student_id} to delete.")
            return False
    
    except Error as e:
        print(f"An error occured: {e}")
        if connection:
            connection.rollback()
            
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
