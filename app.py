from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='20052005',
        database='library_db'
    )
    return connection

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM AUTHOR WHERE user_id = %s", (user_id,))
    authors = cursor.fetchall()
    
    cursor.execute("SELECT * FROM BOOK WHERE user_id = %s", (user_id,))
    books = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return render_template('index.html', authors=authors, books=books)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if '@' not in email:
            flash('Email must contain "@"', 'danger')
            return redirect(url_for('signup'))
            
        hashed_password = generate_password_hash(password)
        
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                           (username, email, hashed_password))
            connection.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error:
            flash('Email already exists or error occurred.', 'danger')
            return redirect(url_for('signup'))
        finally:
            cursor.close()
            connection.close()
            
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        
        # حساب الـ author_id الجديد الخاص بهذا المستخدم فقط ليبدأ من 1
        cursor.execute("SELECT MAX(author_id) AS max_id FROM AUTHOR WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        next_id = 1 if result['max_id'] is None else result['max_id'] + 1
        
        cursor.execute("INSERT INTO AUTHOR (author_id, user_id, name, country) VALUES (%s, %s, %s, %s)", 
                       (next_id, user_id, name, country))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
        
    cursor.close()
    connection.close()
    return render_template('add_author.html')

@app.route('/edit_author/<int:id>', methods=['GET', 'POST'])
def edit_author(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        cursor.execute("UPDATE AUTHOR SET name = %s, country = %s WHERE author_id = %s AND user_id = %s", 
                       (name, country, id, user_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
        
    cursor.execute("SELECT * FROM AUTHOR WHERE author_id = %s AND user_id = %s", (id, user_id))
    author = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit_author.html', author=author)

@app.route('/delete_author/<int:id>')
def delete_author(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM AUTHOR WHERE author_id = %s AND user_id = %s", (id, user_id))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        author_id = request.form['author_id']
        
        # حساب الـ book_id الجديد الخاص بهذا المستخدم فقط ليبدأ من 1
        cursor.execute("SELECT MAX(book_id) AS max_id FROM BOOK WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        next_id = 1 if result['max_id'] is None else result['max_id'] + 1
        
        cursor.execute("INSERT INTO BOOK (book_id, user_id, title, price, author_id) VALUES (%s, %s, %s, %s, %s)", 
                       (next_id, user_id, title, price, author_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
        
    cursor.execute("SELECT * FROM AUTHOR WHERE user_id = %s", (user_id,))
    authors = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('add_book.html', authors=authors)

@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        author_id = request.form['author_id']
        cursor.execute("UPDATE BOOK SET title = %s, price = %s, author_id = %s WHERE book_id = %s AND user_id = %s", 
                       (title, price, author_id, id, user_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
        
    cursor.execute("SELECT * FROM BOOK WHERE book_id = %s AND user_id = %s", (id, user_id))
    book = cursor.fetchone()
    
    cursor.execute("SELECT * FROM AUTHOR WHERE user_id = %s", (user_id,))
    authors = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return render_template('edit_book.html', book=book, authors=authors)

@app.route('/delete_book/<int:id>')
def delete_book(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM BOOK WHERE book_id = %s AND user_id = %s", (id, user_id))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)