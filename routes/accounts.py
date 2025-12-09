from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from models import get_db_connection

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/accounts', methods=['GET', 'POST'])
def accounts():
    if request.method == 'POST':
        password = request.form.get('password')
        email = request.form.get('email')
        action = request.form.get('action', 'register')  # Дія: register або login
        
        conn = get_db_connection()
        
        if action == 'login':
            # Перевіряємо дані при логіні
            user = conn.execute('SELECT * FROM accounts WHERE email = ? AND password = ?',
                              (email, password)).fetchone()
            conn.close()
            
            if user:
                session['user_email'] = email
                session.permanent = True
                return jsonify({"status": "success", "message": "Успішно залогіновані!"}), 200
            else:
                return jsonify({"status": "error", "message": "Невірний email або пароль"}), 401
        else:
            # Реєстрація нового акаунту
            existing = conn.execute('SELECT * FROM accounts WHERE email = ?',
                                  (email,)).fetchone()
            if existing:
                conn.close()
                return jsonify({"status": "error", "message": "Цей email вже зареєстрований"}), 400
            
            conn.execute('INSERT INTO accounts (password, email) VALUES (?, ?)',
                        (password, email))
            conn.commit()
            conn.close()
            
            # Зберігаємо email користувача в сесії
            session['user_email'] = email
            session.permanent = True
            
            return jsonify({"status": "success", "message": "Аккаунт успішно створено!"}), 201
    
    return render_template('accounts.html')

@accounts_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('accounts.accounts'))