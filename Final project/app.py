from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

def create_table():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT,
                series_name TEXT,
                isbn TEXT,
                read_status BOOLEAN NOT NULL DEFAULT 0,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()

create_table()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form.get('username')
    password = request.form.get('password')

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')

    return redirect(url_for('login'))

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    hashed_password = generate_password_hash(password)

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()

    flash('Registration successful! Please log in.')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    books = get_books(session['user_id'])
    return render_template('dashboard.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    genre = request.form.get('genre')
    series_name = request.form.get('series_name')
    isbn = request.form.get('isbn')

    user_id = session.get('user_id')
    if user_id is None:
        flash('User not logged in.')
        return redirect(url_for('login'))

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO books (title, author, genre, series_name, isbn, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, author, genre, series_name, isbn, user_id))
        conn.commit()

    return redirect(url_for('dashboard'))

@app.route('/mark_as_read/<int:book_id>')
def mark_as_read(book_id):
    if 'user_id' not in session:
        flash('User not logged in.')
        return redirect(url_for('login'))

    user_id = session['user_id']

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT read_status FROM books WHERE id = ? AND user_id = ?', (book_id, user_id))
        result = cursor.fetchone()

        if result:
            read_status = result[0]
            if read_status:
                # If the book is already marked as read, undo the action
                cursor.execute('UPDATE books SET read_status = 0 WHERE id = ? AND user_id = ?', (book_id, user_id))
                flash('Marked as Unread!')
            else:
                # If the book is not read, mark it as read
                cursor.execute('UPDATE books SET read_status = 1 WHERE id = ? AND user_id = ?', (book_id, user_id))
                flash('Marked as Read!')
            conn.commit()
        else:
            flash('Book not found or does not belong to the user.')

    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        flash('User not logged in.')
        return redirect(url_for('login'))

    user_id = session['user_id']

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()

        # Delete books associated with the user
        cursor.execute('DELETE FROM books WHERE user_id = ?', (user_id,))

        # Delete the user
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))

        conn.commit()

    # Logout the user after deleting the account
    session.pop('user_id', None)
    flash('Your account has been deleted.')
    return redirect(url_for('login'))

def get_books(user_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE user_id = ?', (user_id,))
        books = cursor.fetchall()
        return books

if __name__ == '__main__':
    app.run(debug=True)
