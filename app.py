from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# --- Database Helpers ---
def get_db_connection():
    conn = sqlite3.connect('festival.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# --- Routes ---

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/<page_name>')
def render_page(page_name):
    # Automatically finds the right HTML file 
    if not page_name.endswith('.html'):
        page_name += '.html'
    try:
        return render_template(page_name)
    except:
        return redirect(url_for('home'))

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if name and email and password:
        conn = get_db_connection()
        conn.execute('INSERT INTO registrations (name, email, password) VALUES (?, ?, ?)',
                     (name, email, password))
        conn.commit()
        conn.close()
        return render_template('sucess.html') # Fixed spelling to match your file
    return "Please fill in all fields.", 400

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)