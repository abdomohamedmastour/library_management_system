-- Problem 2: DML (Seed Data for 6 tables)
USE library;

INSERT INTO AUTHOR (author_id, name, country) VALUES
(1, 'J.K. Rowling', 'UK'),
(2, 'George Orwell', 'UK'),
(3, 'Agatha Christie', 'UK'),
(4, 'Stephen King', 'USA');

INSERT INTO PUBLISHER (publisher_id, name, country) VALUES
(1, 'Bloomsbury', 'UK'),
(2, 'Penguin Books', 'UK'),
(3, 'HarperCollins', 'USA');

INSERT INTO CATEGORY (category_id, name) VALUES
(1, 'Fiction'),
(2, 'Mystery'),
(3, 'Science Fiction');

INSERT INTO BOOK (book_id, title, price, publish_year, author_id, publisher_id, category_id) VALUES
(1, 'Harry Potter 1', 18.50, 1997, 1, 1, 1),
(2, 'Harry Potter 2', 19.00, 1998, 1, 1, 1),
(3, '1984', 12.50, 1949, 2, 2, 3),
(4, 'Animal Farm', 10.00, 1945, 2, 2, 1),
(5, 'The Murder of Roger Ackroyd', 14.00, 1926, 3, 2, 2),
(6, 'The Shining', 22.00, 1977, 4, 3, 1),
(7, 'It', 25.00, 1986, 4, 3, 1);

INSERT INTO MEMBER (member_id, name, email, join_date) VALUES
(1, 'Ahmed Ali', 'ahmed@email.com', '2026-01-10'),
(2, 'Mohamed Hassan', 'mohamed@email.com', '2026-02-15'),
(3, 'Sara Khaled', 'sara@email.com', '2026-03-01');

INSERT INTO LOAN (loan_id, book_id, member_id, loan_date, return_date) VALUES
(1, 1, 1, '2026-03-01', '2026-03-10'),
(2, 2, 1, '2026-03-02', NULL),
(3, 3, 2, '2026-03-03', '2026-03-15');