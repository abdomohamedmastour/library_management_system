-- Problem 2: SQL Queries for F2.1 to F2.6
USE library;

-- F2.1: Library Catalogue (Books with Author, Publisher, Category names)
SELECT b.book_id, b.title, b.price, b.publish_year, 
       a.name AS author_name, p.name AS publisher_name, c.name AS category_name
FROM BOOK b
LEFT JOIN AUTHOR a ON b.author_id = a.author_id
LEFT JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
LEFT JOIN CATEGORY c ON b.category_id = c.category_id;

-- F2.2: Search Books (by title or author)
SELECT * FROM BOOK b 
JOIN AUTHOR a ON b.author_id = a.author_id 
WHERE b.title LIKE '%Harry%' OR a.name LIKE '%Rowling%';

-- F2.3: Authors and their Books count / details
SELECT a.name AS author_name, COUNT(b.book_id) AS total_books
FROM AUTHOR a
LEFT JOIN BOOK b ON a.author_id = b.author_id
GROUP BY a.author_id, a.name;

-- F2.4: Loans Management (Active/Returned loans with Book and Member info)
SELECT l.loan_id, m.name AS member_name, b.title AS book_title, l.loan_date, l.return_date
FROM LOAN l
JOIN MEMBER m ON l.member_id = m.member_id
JOIN BOOK b ON l.book_id = b.book_id;

-- F2.5: Most Borrowed Books
SELECT b.title, COUNT(l.book_id) AS borrow_count
FROM BOOK b
JOIN LOAN l ON b.book_id = l.book_id
GROUP BY b.book_id, b.title
ORDER BY borrow_count DESC;

-- F2.6: Authors & Publishers from the same country
SELECT b.book_id, b.title, a.name AS author_name, a.country AS author_country,
       p.name AS publisher_name, p.country AS publisher_country
FROM BOOK b
JOIN AUTHOR a ON b.author_id = a.author_id
JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
WHERE a.country = p.country;