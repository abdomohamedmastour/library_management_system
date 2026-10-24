# Personal Library System

A full-stack web application for managing authors and books, built using Flask and MySQL.

## Project Features

- **User Authentication:** Secure user registration and login functionality.
- **Author & Book Management:** Create, view, update, and delete authors and books (CRUD operations).
- **Data Security:** Multi-user schema design ensuring proper data isolation between accounts.

## Tech Stack

- **Backend:** Python (Flask, PyMySQL)
- **Database:** MySQL
- **Frontend:** HTML

## Database Setup

1. Open MySQL Workbench or your MySQL client.
2. Run the DDL script (`problem2_DDL.sql`) to initialize the database structure.
3. Run the DML script (`problem2_DML.sql`) to insert the application seed data.

## How to Run Locally

1. Clone the repository: `git clone https://github.com/abdomohamedmastour/library_management_system.git`
2. Install dependencies: `pip install flask pymysql`
3. Start the application: `python app.py`
4. Access the app in your browser at `http://127.0.0.1:5000`.

## Project Team

- Abdelrahman Mastour
- Mohamed Ibrahim