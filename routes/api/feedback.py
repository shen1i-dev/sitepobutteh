from flask import Blueprint, request, jsonify
from models import get_db_connection
from .errors import error_handler

feedback_bp = Blueprint('api_feedback', __name__)

@feedback_bp.route('', methods=['GET'])
def get_all_feedback():
    """
    Отримати всі відгуки
    ---
    responses:
      200:
        description: Список всіх відгуків
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM feedback ORDER BY id DESC')
        feedback = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'data': [dict(f) if hasattr(f, 'keys') else f for f in feedback]
        }), 200
    except Exception as e:
        return error_handler(e, 500)

@feedback_bp.route('', methods=['POST'])
def create_feedback():
    """
    Додати новий відгук
    ---
    parameters:
      - name: body
        in: body
    responses:
      201:
        description: Відгук додано
      400:
        description: Невірні дані
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['name', 'email', 'message']):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)',
            (data['name'], data['email'], data['message'])
        )
        conn.commit()
        feedback_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Feedback created',
            'data': {'id': feedback_id}
        }), 201
    except Exception as e:
        return error_handler(e, 500)
