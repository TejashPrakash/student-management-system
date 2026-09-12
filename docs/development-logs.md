# Development Log

Notes on how EduTrack was built and why things are the way they are.

## Day 1

- Sketched the idea: a console-based Student Management System in Python.
- Chose MySQL for storage to practice real database connectivity.
- Listed the core features: add, search, view, update and delete students.

## Day 2

- Created the project folder structure.
- Designed the database schema.
- Reviewed and improved the schema.
- Created the `edutrack` database.
- Executed the schema successfully.

## Day 3

### Completed
- Connected Python to MySQL.
- Created Student class.
- Implemented insert_student().
- Successfully inserted first student into the database.
- Verified data using MySQL Workbench.

### Learned
- OOP basics
- SQL INSERT
- Exception handling
- Parameterized queries

## Day 4

### Completed
- Added the remaining repository functions: search by roll number,
  search by student ID, list all, update and delete.
- Wrapped every query in parameterized statements so user input never
  becomes part of the SQL text.
- Used a context manager for the cursor/connection so resources are
  always released, and added rollback on failed writes.
- Split the menu logic in `main.py` into small handler functions so each
  menu option is testable on its own.

### Learned
- Repository design pattern: the menu talks to functions, never directly
  to MySQL.
- Transactions: a failed INSERT/UPDATE should leave the table unchanged.
- UNIQUE constraints catch duplicate roll numbers at the database level.

## Day 5

### Completed
- Wrote unit tests for every module with `unittest`, using fake
  input/output functions so prompts are tested without a keyboard.
- Moved database credentials out of the code and into environment
  variables loaded from a local `.env` file.
- Added a GitHub Actions workflow that compiles `src/` and runs the test
  suite on every push.

### Learned
- Dependency injection makes console code testable: validators receive
  `input_fn`/`output_fn` instead of calling `input()` directly.
- CI turns "it works on my machine" into an automatic check.

## Day 6

### Completed
- Built an interactive browser demo of the full console workflow
  (menu, prompts, validation and the SQL each action runs) in
  `demo/index.html`.
- Deployed the demo to GitHub Pages so reviewers can try the app
  without installing Python or MySQL.
- Wrote this development log.
