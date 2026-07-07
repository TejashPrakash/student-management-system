from database import connect_database
from student import Student
from mysql.connector import Error

def insert_student(student: Student) -> None:
    
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
        
    except Error as e:
        print(f"An error occured: {e}")
        if connection:
            connection.rollback()
            
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()