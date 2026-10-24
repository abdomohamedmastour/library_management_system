DROP DATABASE IF EXISTS library_db;
CREATE DATABASE library_db;
USE library_db;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE AUTHOR (
    author_id INT,
    user_id INT,
    name VARCHAR(150) NOT NULL,
    country VARCHAR(100) NOT NULL,
    PRIMARY KEY (author_id, user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE BOOK (
    book_id INT,
    user_id INT,
    title VARCHAR(150) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (book_id, user_id),
    FOREIGN KEY (author_id, user_id) REFERENCES AUTHOR(author_id, user_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);