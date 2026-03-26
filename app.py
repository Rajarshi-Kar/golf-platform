import sqlite3
import os
from datetime import datetime, timedelta
import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

DB_PATH = 'golf_platform.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        conn = get_db()
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            subscription_active BOOLEAN DEFAULT 0,
            charity_percentage INTEGER DEFAULT 10,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            score_value INTEGER NOT NULL,
            score_date DATE NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            UNIQUE(user_id, score_date)
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS draws (
            id INTEGER PRIMARY KEY,
            draw_date DATE UNIQUE,
            winning_numbers TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS winners (
            id INTEGER PRIMARY KEY,
            draw_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            match_type TEXT,
            prize_amount REAL,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY(draw_id) REFERENCES draws(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''')
        
        conn.commit()
        conn.close()
    except Exception as e:
        pass

init_db()

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/')
def index():
    user_id = session.get('user_id')
    if user_id:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')
        
        if not email or not name or not password:
            return jsonify({'error': 'All fields required'}), 400
        
        conn = get_db()
        c = conn.cursor()
        
        try:
            c.execute('INSERT INTO users (email, name, password) VALUES (?, ?, ?)',
                     (email, name, password))
            conn.commit()
            user_id = c.lastrowid
            session['user_id'] = user_id
            session['email'] = email
            conn.close()
            return jsonify({'success': True, 'redirect': '/dashboard'})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'error': 'Email already exists'}), 400
    
    return render_template('auth.html', form='signup')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        conn = get_db()
        c = conn.cursor()
        user = c.execute('SELECT * FROM users WHERE email = ? AND password = ?', 
                        (email, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['email'] = user['email']
            return jsonify({'success': True, 'redirect': '/dashboard'})
        
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return render_template('auth.html', form='signin')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/signin')
    
    user_id = session['user_id']
    conn = get_db()
    c = conn.cursor()
    
    user = c.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    scores = c.execute('SELECT * FROM scores WHERE user_id = ? ORDER BY score_date DESC LIMIT 5', 
                      (user_id,)).fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', user=user, scores=scores)

@app.route('/api/score', methods=['POST'])
def add_score():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    score_value = int(data.get('score', 0))
    score_date = data.get('date')
    
    if not 1 <= score_value <= 45:
        return jsonify({'error': 'Score must be 1-45'}), 400
    
    user_id = session['user_id']
    conn = get_db()
    c = conn.cursor()
    
    try:
        c.execute('INSERT INTO scores (user_id, score_value, score_date) VALUES (?, ?, ?)',
                 (user_id, score_value, score_date))
        conn.commit()
        score_id = c.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': score_id})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Score already exists for this date'}), 400

@app.route('/api/draws', methods=['GET'])
def get_draws():
    conn = get_db()
    c = conn.cursor()
    draws = c.execute('SELECT * FROM draws WHERE status = "completed" ORDER BY draw_date DESC LIMIT 10').fetchall()
    conn.close()
    
    draws_list = []
    for draw in draws:
        draws_list.append({
            'id': draw['id'],
            'date': draw['draw_date'],
            'numbers': draw['winning_numbers'],
            'status': draw['status']
        })
    
    return jsonify(draws_list)

@app.route('/api/user', methods=['GET'])
def get_user():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    conn = get_db()
    c = conn.cursor()
    user = c.execute('SELECT id, email, name, subscription_active, charity_percentage FROM users WHERE id = ?', 
                    (user_id,)).fetchone()
    conn.close()
    
    if user:
        return jsonify(dict(user))
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE users SET subscription_active = 1 WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
