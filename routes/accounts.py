from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models import get_db_connection

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/accounts', methods=['GET', 'POST'])
def accounts():
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO accounts (password, email) VALUES (?, ?)',
                     (password, email))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success"}), 200
    
    return render_template('accounts.html')