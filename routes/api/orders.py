from flask import Blueprint, request, jsonify
from models import get_db_connection
from .errors import error_handler

orders_bp = Blueprint('api_orders', __name__)

@orders_bp.route('', methods=['GET'])
def get_all_orders():
    """
    Отримати всі замовлення
    ---
    responses:
      200:
        description: Список всіх замовлень
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders')
        orders = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'data': [dict(o) if hasattr(o, 'keys') else o for o in orders]
        }), 200
    except Exception as e:
        return error_handler(e, 500)

@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """
    Отримати замовлення за ID
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
    responses:
      200:
        description: Інформація про замовлення
      404:
        description: Замовлення не знайдено
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        order = cursor.fetchone()
        conn.close()
        
        if not order:
            return jsonify({'status': 'error', 'message': 'Order not found'}), 404
        
        return jsonify({
            'status': 'success',
            'data': dict(order) if hasattr(order, 'keys') else order
        }), 200
    except Exception as e:
        return error_handler(e, 500)

@orders_bp.route('', methods=['POST'])
def create_order():
    """
    Створити нове замовлення
    ---
    parameters:
      - name: body
        in: body
    responses:
      201:
        description: Замовлення створено
      400:
        description: Невірні дані
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['email', 'address', 'total_price']):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        from datetime import datetime
        cursor.execute(
            'INSERT INTO orders (email, address, total_price, status, date) VALUES (?, ?, ?, ?, ?)',
            (data['email'], data['address'], data['total_price'], 'New', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        order_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Order created',
            'data': {'id': order_id}
        }), 201
    except Exception as e:
        return error_handler(e, 500)
