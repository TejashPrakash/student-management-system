# 🎓 EduTrack - Student Management System

A console-based Student Management System built in Python using MySQL. This project demonstrates Object-Oriented Programming (OOP), database connectivity, and CRUD (Create, Read, Update, Delete) operations.

## 📌 Features

- ➕ Add Student
- 🔍 Search Student by Roll Number
- 🔍 Search Student by Student ID
- 📋 View All Students
- ✏️ Update Student Information
- 🗑️ Delete Student Records
- 💾 MySQL Database Integration
- 🖥️ Interactive Console Menu
- ⚠️ Error Handling and Database Transaction Support

## 🌐 Live Demo

An interactive browser demo is included in the `demo/` folder and deployed to
GitHub Pages at:

https://tejashprakash.github.io/student-management-system/

The demo stores sample records in the browser only; the full console application
continues to use MySQL.

---

## 🛠️ Technologies Used

- Python 3.10 or later
- MySQL
- mysql-connector-python
- Spyder IDE
- Git & GitHub

---

## 📂 Project Structure

```
Student-Management-System/
│
├── database/
│   └── schema.sql
│
├── demo/
│   └── index.html
│
├── src/
│   ├── config.py
│   ├── database.py
│   ├── errors.py
│   ├── input_validators.py
│   ├── student.py
│   ├── student_repository.py
│   └── main.py
│
├── tests/
│   └── test_*.py
│
├── .github/workflows/
│   ├── python.yml
│   └── deploy-demo.yml
│
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚙️ Installation

1. Clone the repository

```bash
git clone https://github.com/TejashPrakash/student-management-system.git
```

2. Navigate to the project folder

```bash
cd student-management-system
```

3. Create a `.env` file locally using `.env.example` as a template with your MySQL credentials.

4. Install the required packages

```bash
pip install -r requirements.txt
```

5. Create the database

- Run the SQL statements in `database/schema.sql` to create the required tables.

6. Run the application

```bash
python src/main.py
```

---

## 📷 Application Menu

```
========================================
                EDUTRACK
        Student Management System
========================================
1. Add Student
2. Search Student by Roll Number
3. Search Student by Student ID
4. View All Students
5. Update Student
6. Delete Student
7. Exit
========================================
```

---

## 📖 Concepts Demonstrated

- Object-Oriented Programming (OOP)
- Classes and Objects
- Functions and Modules
- MySQL Database Connectivity
- SQL CRUD Operations
- Exception Handling
- Repository Design Pattern
- Modular Programming

---

## 🚀 Future Improvements

- Teacher Management
- Attendance Management
- Marks Management
- Login System
- Data Validation
- Export Data to CSV/Excel
- Graphical User Interface (GUI)
- Web-based Version using Flask or Django

---

## 👨‍💻 Author

**Tejash Prakash**

GitHub: https://github.com/TejashPrakash

---

## 📄 License

This project is developed for learning purposes and is open for educational use.
