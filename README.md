# Library Management System (Lab 3)

A full-stack web application for managing a library database, built with Python (Flask), MySQL, and Bootstrap 5.

## Project Features

* **CRUD Operations:** Create, read, update, and delete **Authors** and **Books**[cite: 19].
* **F2.1 Search Books:** Filter books by title keyword (`LIKE`), price range (`BETWEEN`), and category, ordered by cheapest price first[cite: 19].
* **F2.2 Library Catalogue:** Display all books with full author, publisher, and category details using SQL `JOIN`[cite: 19].
* **F2.3 Reports & Statistics:** View book counts and average prices per category (`GROUP BY`), prolific authors with 2+ books (`HAVING`), and overall library price statistics (`SUM`, `MIN`, `MAX`)[cite: 19].
* **F2.4 Loans Management:** Issue new loans, mark books as returned, view active unreturned loans, and identify members and books with zero loans (`LEFT JOIN`)[cite: 19].
* **F2.5 Most Borrowed:** Display the top 3 most borrowed books (`LIMIT 3`) and the top borrowing member[cite: 19].
* **F2.6 Authors & Publishers:** List all authors with their total book counts (including 0) and books whose author and publisher share the same country[cite: 19].

## Tech Stack

* **Backend:** Python (Flask, `mysql-connector-python`)[cite: 19]
* **Database:** MySQL[cite: 19]
* **Frontend:** HTML5, Jinja2, Bootstrap 5[cite: 19]

## Database & Application Setup

1. Open MySQL Workbench or your MySQL client[cite: 19].
2. Create the database `library` and run `problem2_DDL.sql` to initialize the tables (`AUTHOR`, `PUBLISHER`, `CATEGORY`, `BOOK`, `MEMBER`, `LOAN`)[cite: 19].
3. Run `problem2_DML.sql` to insert the initial seed data[cite: 19].
4. Install required Python packages:
   ```bash
   pip install flask mysql-connector-python