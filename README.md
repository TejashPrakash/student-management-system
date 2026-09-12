<div align="center">

# 🎓 EduTrack - Student Management System

**A console-based Student Management System in Python + MySQL, with a live in-browser demo.**

[![Python checks](https://github.com/TejashPrakash/student-management-system/actions/workflows/python.yml/badge.svg)](https://github.com/TejashPrakash/student-management-system/actions/workflows/python.yml)
[![Live demo](https://img.shields.io/badge/demo-live-brightgreen)](https://tejashprakash.github.io/student-management-system/demo/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

</div>

---

EduTrack is a menu-driven application for managing student records. It demonstrates
Object-Oriented Programming, real MySQL database connectivity, and CRUD (Create, Read,
Update, Delete) operations through a clean, layered architecture:

```
main.py (menu)  →  student_repository.py (SQL)  →  MySQL (students table)
                        ↑
        input_validators.py guards every prompt
```

## 🌐 Try the Live Demo (no installation)

**👉 [Open the interactive demo](https://tejashprakash.github.io/student-management-system/demo/)**

The demo is a faithful simulation of the real console application, running entirely
in your browser: the same 7-option menu, the same prompts and validation messages
from `input_validators.py`, the same profile output as `Student.display_info()`,
and a trace of the SQL each action runs against the `students` table.

Records are saved in your browser only (`localStorage`); the console application
itself uses MySQL.

## ✨ Features

- ➕ Add Student (11 validated fields)
- 🔍 Search Student by Roll Number
- 🔍 Search Student by Student ID
- 📋 View All Students
- ✏️ Update Student Information
- 🗑️ Delete Student Records (with confirmation)
- 💾 MySQL Database Integration
- 🖥️ Interactive Console Menu
- ⚠️ Error Handling and Database Transaction Support (rollback on failure)

## 🛠️ Technologies Used

| Layer      | Technology                                    |
|------------|-----------------------------------------------|
| Language   | Python 3.10+                                   |
| Database   | MySQL                                          |
| Driver     | mysql-connector-python                         |
| Config     | python-dotenv (environment variables)          |
| Testing    | unittest (standard library)                    |
| CI/CD      | GitHub Actions + GitHub Pages                  |
| IDE        | Spyder                                         |

## 📂 Project Structure

```
Student-Management-System/
│
├── database/
│   └── schema.sql            # MySQL schema: creates database + all tables
│
├── demo/
│   └── index.html            # Interactive browser demo (GitHub Pages)
│
├── docs/
│   └── development-logs.md   # How the project was built, day by day
│
├── src/
│   ├── config.py             # Reads DB credentials from environment / .env
│   ├── database.py           # Connection handling
│   ├── errors.py             # Custom exception types
│   ├── input_validators.py   # Reusable, testable prompt validation
│   ├── student.py            # Student model (OOP)
│   ├── student_repository.py # All SQL CRUD operations (repository layer)
│   └── main.py               # Console menu and workflow
│
├── tests/
│   └── test_*.py             # Unit tests for every module (54 tests)
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

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/TejashPrakash/student-management-system.git
cd student-management-system
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the database connection

Create a `.env` file in the project root (copy `.env.example`) and fill in your
local MySQL credentials:

```env
EDUTRACK_DB_HOST=localhost
EDUTRACK_DB_USER=root
EDUTRACK_DB_PASSWORD=your_password_here
EDUTRACK_DB_NAME=edutrack
EDUTRACK_DB_PORT=3306
```

Notes:

- `EDUTRACK_DB_PASSWORD` is required. The app refuses to start without it unless
  you explicitly set `EDUTRACK_ALLOW_EMPTY_PASSWORD=1` (throwaway local databases only).
- Never commit `.env` or real credentials. In production, prefer a dedicated
  least-privilege MySQL user instead of `root`.

### 4. Create the database

Run the schema script (it creates the `edutrack` database and all tables):

```bash
mysql -u root -p < database/schema.sql
```

### 5. Run the application

```bash
python src/main.py
```

## 🧪 Running the Tests

The project ships with unit tests for every module (`unittest`, no extra test
dependencies needed):

```bash
python -m unittest discover -s tests -v
```

The same checks run automatically on every push via GitHub Actions
(`.github/workflows/python.yml`).

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

## 📖 Concepts Demonstrated

- Object-Oriented Programming (classes, objects, methods)
- Repository Design Pattern (SQL isolated from menu logic)
- Parameterized SQL queries (injection-safe CRUD)
- Exception handling with a custom error hierarchy
- Database transactions with rollback on failure
- Dependency injection for testable console input
- Environment-based configuration (.env, 12-factor style)
- Continuous Integration with GitHub Actions

## 🚀 Future Improvements

- Teacher management
- Attendance management
- Marks management
- Login system with roles
- Export data to CSV/Excel
- Graphical user interface (GUI)
- Web-based version using Flask or Django

## 📚 Documentation

- [Development log](docs/development-logs.md) - how the project was built, decisions made along the way
- [Database schema](database/schema.sql) - all tables with comments

## 👨‍💻 Author

**Tejash Prakash**

GitHub: [@TejashPrakash](https://github.com/TejashPrakash)

## 📄 License

This project is developed for learning purposes and is open for educational use
under the [MIT License](LICENSE).
