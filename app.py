from flask import Flask, render_template, request, redirect, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB_NAME = 'users.db'

# Create database table if not exists
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          email TEXT NOT NULL,
                          userid TEXT UNIQUE NOT NULL,
                          password TEXT NOT NULL
                        )''')

@app.route('/')
def home():
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    userid = request.form['userid']
    password = request.form['password']

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, userid, password) VALUES (?, ?, ?, ?)",
                           (name, email, userid, password))
            conn.commit()
            flash("Registration successful!", "success")
    except sqlite3.IntegrityError:
        flash("User ID already exists. Try another one.", "error")

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
