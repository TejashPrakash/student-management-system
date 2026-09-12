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

**Try the app in your browser (no installation needed):**

https://tejashprakash.github.io/student-management-system/

The demo simulates the real application end to end: the same 7-option menu,
the same prompts and validation messages from `input_validators.py`, profile
views like `Student.display_info()`, and the SQL each action runs against the
`students` table. Records are stored in the browser only (`localStorage`);
the full console application continues to use MySQL.

---

## 🛠️ Technologies Used

- Python 3.10 or later
- MySQL
- mysql-connector-python
- python-dotenv
- Spyder IDE
- Git & GitHub

---

## 📂 Project Structure

```
Student-Management-System/
│
├── database/
│   └── schema.sql            # MySQL schema for all tables
│
├── demo/
│   └── index.html            # Interactive browser demo (GitHub Pages)
│
├── docs/
│   └── development-logs.md   # How the project was built, day by day
│
├── src/
│   ├── config.py             # Reads DB credentials from environment/.env
│   ├── database.py           # Connection handling
│   ├── errors.py             # Custom exception types
│   ├── input_validators.py   # Reusable, testable prompt validation
│   ├── student.py            # Student model (OOP)
│   ├── student_repository.py # All SQL CRUD operations (repository layer)
│   └── main.py               # Console menu and workflow
│
├── tests/
│   └── test_*.py             # Unit tests for every module
│
├── .github/workflows/
│   ├── python.yml            # CI: syntax check + unit tests
│   └── deploy-demo.yml       # Deploys demo/ to GitHub Pages
│
├── .env.example              # Template for local database credentials
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

1. Clone the repository

```bash
git clone https://github.com/TejashPrakash/student-management-system.git
```

2. Navigate to the project folder

```bash
cd student-management-system
```

3. Configure the database connection (required)

- Create a `.env` file locally using `.env.example` as a template, or set
  these environment variables in your shell:
  `EDUTRACK_DB_HOST`, `EDUTRACK_DB_USER`, `EDUTRACK_DB_PASSWORD`,
  `EDUTRACK_DB_NAME`, `EDUTRACK_DB_PORT`
- `EDUTRACK_DB_PASSWORD` is mandatory. The app refuses to start without it
  unless you explicitly set `EDUTRACK_ALLOW_EMPTY_PASSWORD=1` for a
  throwaway local database with no password.
- Never commit `.env` or real credentials; prefer a dedicated
  least-privilege MySQL user rather than `root`.

4. Install the required packages

```bash
pip install -r requirements.txt
```

5. Create the database

- Run the SQL statements in `database/schema.sql` to create the `edutrack`
  database and all tables, for example:

```bash
mysql -u root -p < database/schema.sql
```

6. Run the application

```bash
python src/main.py
```

---

## 🧪 Running the Tests

The project ships with unit tests for every module (built with `unittest`,
no extra test dependencies needed):

```bash
python -m unittest discover -s tests -v
```

The same checks run automatically on every push via GitHub Actions
(`.github/workflows/python.yml`).

---

## 📷 Application Menu

```
========================================
                EDUTRACK
        Student Management System
========================================
1.  Add Student
2.  Search Student by Roll Number
3.  Search Student by Student ID
4.  View All Students
5.  Update Student
6.  Delete Student
7.  Exit
========================================
```

---

## 📖 Concepts Demonstrated

- Object-Oriented Programming (OOP)
- Classes and Objects
- Functions and Modules
- MySQL Database Connectivity
- SQL CRUD Operations with Parameterized Queries
- Exception Handling and Custom Exceptions
- Repository Design Pattern
- Dependency Injection for Testable Console Input
- Environment-Based Configuration
- Continuous Integration with GitHub Actions

---

## 🚀 Future Improvements

- Teacher Management
- Attendance Management
- Marks Management
- Login System
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
