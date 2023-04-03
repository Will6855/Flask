import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

# Créer la connexion à la BDD
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

# Fonction à executer sur la racine
@app.route('/')
def index():
    conn = get_db_connection()
    nbUsers = conn.execute('SELECT COUNT(*) FROM users').fetchone()
    conn.close()
    return render_template('index.html', nbUsers=nbUsers)

# Fonction à executer sur /users
@app.route('/users')
def users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall() # Récupére tous les utilisateurs de la BDD
    conn.close()
    return render_template('users.html', users=users) # Affiche les utilisateurs

# Fonction à executer sur /CreateUser
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
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', # Insere un nouvel utilisateur dans la BDD
                         (username , password))
            conn.commit()
            conn.close()
            return redirect(url_for('users')) # Retourne sur la page affichant tous les utilisateurs
    return render_template('createUser.html')

# Fonction servant à récupérer toutes les informations d'un utilisateur à partir de son ID
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?',
                        (user_id,)).fetchone()
    conn.close()
    if user is None:
        abort(404)
    return user

# Fonction permettant de modifier les informations d'un utilisateur à partir de son ID
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
                         (username, password, id)) # Modifie les informations de l'utilisateurs
            conn.commit()
            conn.close()
            return redirect(url_for('users'))

    return render_template('editUser.html', user=user)

# Fonction permettant de supprimer un utilisateur à partir de son ID
@app.route('/<int:id>/delete', methods=('GET', 'POST',))
def delete(id):
    user = get_user(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,)) # Supprime l'utilisateur
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(user['username']))
    return redirect(url_for('users'))


# Fonction qui récupérent un ensemble d'informations pour l'afficher sur la page WEB
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    nbUsers = conn.execute('SELECT COUNT(*) FROM users').fetchone()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('dashboard.html', nbUsers=nbUsers, users=users)