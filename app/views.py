from app import app
from flask import request, render_template, redirect, url_for
import bcrypt
from app import models

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Проверка пароля
        if password != confirm_password:
            return render_template('password_mismatch.html', error='Пароли не совпадают')

        # Проверка существования пользователя
        connection = models.get_db_connection('service_database')
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result:
            return render_template('existed_user.html', error='Пользователь с таким именем уже существует')


        # Хеширование пароля
        hashed_password = hash_password(password)

        # Вставка данных в базу данных
        connection = models.get_db_connection('service_database')
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password),
        )
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('login'))  # Перенаправление на страницу входа
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        connection = models.get_db_connection('service_database')
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result == None:
            return render_template('unexisted_user.html')

        # Хеширование пароля
        hashed_password = hash_password(password)

        connection = models.get_db_connection('service_database')
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM users WHERE password = %s", (hashed_password,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            return render_template('index.html')
        else:
            return render_template('invalid_password.html')

'''
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()'''

import hashlib

def hash_password(password):
    # Хешируем пароль с использованием SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password