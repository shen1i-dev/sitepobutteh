from flask import Blueprint, request, jsonify
from models import get_db_connection
from .errors import error_handler

users_bp = Blueprint('api_users', __name__)

@users_bp.route('', methods=['GET'])
def get_all_users():
    """
    Отримати всі користувачів
    ---
    responses:
      200:
        description: Список користувачів
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, email FROM accounts')
        users = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'data': [dict(u) if hasattr(u, 'keys') else u for u in users]
        }), 200
    except Exception as e:
        return error_handler(e, 500)

@users_bp.route('', methods=['POST'])
def create_user():
    """
    Створити нового користувача
    ---
    parameters:
      - name: body
        in: body
    responses:
      201:
        description: Користувач створений
      400:
        description: Невірні дані
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['email', 'password']):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO accounts (email, password) VALUES (?, ?)',
            (data['email'], data['password'])
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'User created',
            'data': {'id': user_id}
        }), 201
    except Exception as e:
        return error_handler(e, 500)
