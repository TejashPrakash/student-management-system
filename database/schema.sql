-- ====================================================
-- EduTrack - Student Management System Database Schema
-- Author    : Tejash Prakash
-- Description:
--   Creates the tables required for Version 1.
--   Run the statements below in MySQL Workbench or:
--     mysql -u root -p < database/schema.sql
-- ====================================================

CREATE DATABASE IF NOT EXISTS edutrack;
USE edutrack;

-- ----------------------------------------------------
-- students : the core table used by the console app.
-- The Python model in src/student.py maps 1:1 onto
-- these columns (class_name -> `class`).
-- ----------------------------------------------------
CREATE TABLE students (
    student_id     INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    first_name     VARCHAR(50) NOT NULL,
    last_name      VARCHAR(50) NOT NULL,
    gender         ENUM('Male', 'Female', 'Other') NOT NULL,
    dob            DATE NOT NULL,
    class          VARCHAR(10) NOT NULL,
    section        CHAR(1) NOT NULL,
    roll_no        INT NOT NULL UNIQUE,
    email          VARCHAR(255) UNIQUE,
    phone          VARCHAR(20) UNIQUE,
    address        TEXT,
    admission_date DATE NOT NULL,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ----------------------------------------------------
-- Reserved for Version 2 (see "Future Improvements"
-- in the README): teacher, attendance and marks
-- management.
-- ----------------------------------------------------
CREATE TABLE teachers (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name  VARCHAR(50) NOT NULL,
    subject    VARCHAR(50) NOT NULL,
    email      VARCHAR(255) UNIQUE,
    phone      VARCHAR(20) UNIQUE,
    is_active  BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE attendance (
    attendance_id   INT AUTO_INCREMENT PRIMARY KEY,
    student_id      INT UNSIGNED,
    attendance_date DATE NOT NULL,
    status          ENUM('Present', 'Absent', 'Late') NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE marks (
    marks_id   INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNSIGNED,
    subject    VARCHAR(50) NOT NULL,
    exam       VARCHAR(50),
    marks      DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
