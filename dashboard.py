import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'

@app.route('/')
def index():
    conn = get_db_connection()
    conn.close()
    return render_template('index.html')

@app.route('/users')
def users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('users.html', users=users)

@app.route('/createUser', methods=('GET', 'POST'))
def createUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username and not password:
            flash('Username and password is required!')
        elif not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username , password))
            conn.commit()
            conn.close()
            return redirect(url_for('users'))
    return render_template('createUser.html')

def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?',
                        (user_id,)).fetchone()
    conn.close()
    if user is None:
        abort(404)
    return user

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    user = get_user(id)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username and not password:
            flash('Username and password is required!')
        elif not username:
            flash('Username is required!')
        elif not password:
            flash('Password is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE users SET username = ?, password = ?'
                         ' WHERE id = ?',
                         (username, password, id))
            conn.commit()
            conn.close()
            return redirect(url_for('users'))

    return render_template('editUser.html', user=user)

@app.route('/<int:id>/delete', methods=('GET', 'POST',))
def delete(id):
    user = get_user(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(user['username']))
    return redirect(url_for('users'))