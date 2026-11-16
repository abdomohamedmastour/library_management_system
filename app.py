from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="20052005",
        database="library"
    )

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.book_id, b.title, b.price, b.publish_year,
               a.name AS author_name, p.name AS publisher_name, c.name AS category_name
        FROM BOOK b
        JOIN AUTHOR a ON b.author_id = a.author_id
        JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
        JOIN CATEGORY c ON b.category_id = c.category_id
    """)
    books = cursor.fetchall()
    cursor.execute("SELECT * FROM AUTHOR")
    authors = cursor.fetchall()
    cursor.execute("SELECT * FROM PUBLISHER")
    publishers = cursor.fetchall()
    cursor.execute("SELECT * FROM CATEGORY")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', books=books, authors=authors, publishers=publishers, categories=categories)

@app.route('/search', methods=['GET', 'POST'])
def search_books():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CATEGORY")
    categories = cursor.fetchall()
    books = None
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        min_price = request.form.get('min_price', 0)
        max_price = request.form.get('max_price', 999999)
        category_id = request.form.get('category_id', '')
        query = """
            SELECT b.*, a.name AS author_name, p.name AS publisher_name, c.name AS category_name
            FROM BOOK b
            JOIN AUTHOR a ON b.author_id = a.author_id
            JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
            JOIN CATEGORY c ON b.category_id = c.category_id
            WHERE b.title LIKE %s AND b.price BETWEEN %s AND %s
        """
        params = [f"%{keyword}%", min_price if min_price else 0, max_price if max_price else 999999]
        if category_id:
            query += " AND b.category_id = %s"
            params.append(category_id)
        query += " ORDER BY b.price ASC"
        cursor.execute(query, tuple(params))
        books = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('search.html', categories=categories, books=books)

@app.route('/catalogue')
def catalogue():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.book_id, b.title, b.publish_year, b.price,
               a.name AS author_name, p.name AS publisher_name, c.name AS category_name
        FROM BOOK b
        JOIN AUTHOR a ON b.author_id = a.author_id
        JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
        JOIN CATEGORY c ON b.category_id = c.category_id
    """)
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('catalogue.html', books=books)

@app.route('/reports')
def reports():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.name AS category_name, COUNT(b.book_id) AS book_count, AVG(b.price) AS avg_price
        FROM CATEGORY c
        LEFT JOIN BOOK b ON c.category_id = b.category_id
        GROUP BY c.category_id, c.name
    """)
    category_stats = cursor.fetchall()
    cursor.execute("""
        SELECT a.name AS author_name, COUNT(b.book_id) AS total_books
        FROM AUTHOR a
        JOIN BOOK b ON a.author_id = b.author_id
        GROUP BY a.author_id, a.name
        HAVING COUNT(b.book_id) >= 2
    """)
    prolific_authors = cursor.fetchall()
    cursor.execute("""
        SELECT SUM(price) AS total_price, MIN(price) AS min_price, MAX(price) AS max_price
        FROM BOOK
    """)
    library_price_stats = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('reports.html', 
                           category_stats=category_stats, 
                           prolific_authors=prolific_authors, 
                           library_price_stats=library_price_stats)

@app.route('/loans', methods=['GET', 'POST'])
def loans_management():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        book_id = request.form['book_id']
        member_id = request.form['member_id']
        loan_date = request.form['loan_date']
        cursor.execute("INSERT INTO LOAN (book_id, member_id, loan_date) VALUES (%s, %s, %s)", (book_id, member_id, loan_date))
        conn.commit()
        return redirect(url_for('loans_management'))
    cursor.execute("""
        SELECT l.loan_id, m.name AS member_name, b.title AS book_title, l.loan_date, l.return_date
        FROM LOAN l
        JOIN MEMBER m ON l.member_id = m.member_id
        JOIN BOOK b ON l.book_id = b.book_id
        WHERE l.return_date IS NULL
    """)
    active_loans = cursor.fetchall()
    cursor.execute("""
        SELECT m.name AS member_name, m.email
        FROM MEMBER m
        LEFT JOIN LOAN l ON m.member_id = l.member_id
        WHERE l.loan_id IS NULL
    """)
    unborrowed_members = cursor.fetchall()
    cursor.execute("""
        SELECT b.title, b.publish_year
        FROM BOOK b
        LEFT JOIN LOAN l ON b.book_id = l.book_id
        WHERE l.loan_id IS NULL
    """)
    unborrowed_books = cursor.fetchall()
    cursor.execute("SELECT * FROM BOOK")
    books = cursor.fetchall()
    cursor.execute("SELECT * FROM MEMBER")
    members = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('loans.html', 
                           active_loans=active_loans, 
                           unborrowed_members=unborrowed_members, 
                           unborrowed_books=unborrowed_books,
                           books=books, members=members)

@app.route('/return_loan/<int:id>')
def return_loan(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE LOAN SET return_date = CURDATE() WHERE loan_id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('loans_management'))

@app.route('/most_borrowed')
def most_borrowed():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.title, a.name AS author_name, COUNT(l.loan_id) AS borrow_count
        FROM BOOK b
        JOIN AUTHOR a ON b.author_id = a.author_id
        JOIN LOAN l ON b.book_id = l.book_id
        GROUP BY b.book_id, b.title, a.name
        ORDER BY borrow_count DESC
        LIMIT 3
    """)
    top_books = cursor.fetchall()
    cursor.execute("""
        SELECT m.name AS member_name, m.email, COUNT(l.loan_id) AS total_loans
        FROM MEMBER m
        JOIN LOAN l ON m.member_id = l.member_id
        GROUP BY m.member_id, m.name, m.email
        ORDER BY total_loans DESC
        LIMIT 1
    """)
    top_member = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('most_borrowed.html', top_books=top_books, top_member=top_member)

@app.route('/authors_books')
def authors_books():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.name AS author_name, a.country, COUNT(b.book_id) AS total_books
        FROM AUTHOR a
        LEFT JOIN BOOK b ON a.author_id = b.author_id
        GROUP BY a.author_id, a.name, a.country
    """)
    authors_count = cursor.fetchall()
    cursor.execute("""
        SELECT b.title, a.name AS author_name, a.country AS author_country,
               p.name AS publisher_name, p.country AS publisher_country
        FROM BOOK b
        JOIN AUTHOR a ON b.author_id = a.author_id
        JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
        WHERE a.country = p.country
    """)
    same_country_books = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('authors_books.html', authors_count=authors_count, same_country_books=same_country_books)

@app.route('/add_author', methods=['POST'])
def add_author():
    name = request.form['name']
    country = request.form['country']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO AUTHOR (name, country) VALUES (%s, %s)", (name, country))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit_author/<int:id>', methods=['GET', 'POST'])
def edit_author(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        cursor.execute("UPDATE AUTHOR SET name = %s, country = %s WHERE author_id = %s", (name, country, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    cursor.execute("SELECT * FROM AUTHOR WHERE author_id = %s", (id,))
    author = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_author.html', author=author)

@app.route('/delete_author/<int:id>')
def delete_author(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM AUTHOR WHERE author_id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    price = request.form['price']
    publish_year = request.form['publish_year']
    author_id = request.form['author_id']
    publisher_id = request.form['publisher_id']
    category_id = request.form['category_id']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO BOOK (title, price, publish_year, author_id, publisher_id, category_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (title, price, publish_year, author_id, publisher_id, category_id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        publish_year = request.form['publish_year']
        author_id = request.form['author_id']
        publisher_id = request.form['publisher_id']
        category_id = request.form['category_id']
        cursor.execute("""
            UPDATE BOOK SET title=%s, price=%s, publish_year=%s, author_id=%s, publisher_id=%s, category_id=%s
            WHERE book_id=%s
        """, (title, price, publish_year, author_id, publisher_id, category_id, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    cursor.execute("SELECT * FROM BOOK WHERE book_id = %s", (id,))
    book = cursor.fetchone()
    cursor.execute("SELECT * FROM AUTHOR")
    authors = cursor.fetchall()
    cursor.execute("SELECT * FROM PUBLISHER")
    publishers = cursor.fetchall()
    cursor.execute("SELECT * FROM CATEGORY")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('edit_book.html', book=book, authors=authors, publishers=publishers, categories=categories)

@app.route('/delete_book/<int:id>')
def delete_book(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM BOOK WHERE book_id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)