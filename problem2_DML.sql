USE library_db;

INSERT INTO AUTHOR (author_id, user_id, name, country) VALUES (1, 1, 'نجيب محفوظ', 'Egypt');
INSERT INTO AUTHOR (author_id, user_id, name, country) VALUES (2, 1, 'Agatha Christie', 'UK');
INSERT INTO AUTHOR (author_id, user_id, name, country) VALUES (3, 1, 'George Orwell', 'UK');

INSERT INTO BOOK (book_id, user_id, title, price, author_id) VALUES (1, 1, 'Palace Walk', 15.50, 1);
INSERT INTO BOOK (book_id, user_id, title, price, author_id) VALUES (2, 1, 'And Then There Were None', 12.00, 2);
INSERT INTO BOOK (book_id, user_id, title, price, author_id) VALUES (3, 1, '1984', 14.25, 3);
INSERT INTO BOOK (book_id, user_id, title, price, author_id) VALUES (4, 1, 'Miramar', 12.50, 1);
INSERT INTO BOOK (book_id, user_id, title, price, author_id) VALUES (5, 1, 'Murder on the Orient Express', 14.00, 2);
INSERT INTO BOOK (book_id, user_id, title, price, author_id) VALUES (6, 1, 'Animal Farm', 10.00, 3);