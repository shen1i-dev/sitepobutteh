from flask import Blueprint, request, jsonify
from models import get_db_connection
from .errors import error_handler

products_bp = Blueprint('api_products', __name__)

@products_bp.route('', methods=['GET'])
def get_all_products():
    """
    Отримати всі товари
    ---
    responses:
      200:
        description: Список всіх товарів
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        conn.close()
        
        # Конвертуємо Row об'єкти в список словників
        products_list = [dict(p) for p in products]
        
        return jsonify({
            'status': 'success',
            'data': products_list,
            'count': len(products_list)
        }), 200
    except Exception as e:
        return error_handler(e, 500)

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Отримати товар за ID
    ---
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Інформація про товар
      404:
        description: Товар не знайдено
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        conn.close()
        
        if not product:
            return jsonify({'status': 'error', 'message': 'Product not found'}), 404
        
        return jsonify({
            'status': 'success',
            'data': dict(product)
        }), 200
    except Exception as e:
        return error_handler(e, 500)

@products_bp.route('', methods=['POST'])
def create_product():
    """
    Створити новий товар
    ---
    parameters:
      - name: body
        in: body
        schema:
          properties:
            name:
              type: string
            price:
              type: number
            image:
              type: string
    responses:
      201:
        description: Товар створений
      400:
        description: Невірні дані
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['name', 'price']):
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO products (name, price, image) VALUES (?, ?, ?)',
            (data['name'], data['price'], data.get('image', ''))
        )
        conn.commit()
        product_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Product created',
            'data': {'id': product_id}
        }), 201
    except Exception as e:
        return error_handler(e, 500)

@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Оновити товар
    ---
    parameters:
      - name: product_id
        in: path
        type: integer
      - name: body
        in: body
    responses:
      200:
        description: Товар оновлений
      404:
        description: Товар не знайдено
    """
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'status': 'error', 'message': 'Product not found'}), 404
        
        cursor.execute(
            'UPDATE products SET name = ?, price = ?, image = ? WHERE id = ?',
            (data.get('name'), data.get('price'), data.get('image'), product_id)
        )
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Product updated'
        }), 200
    except Exception as e:
        return error_handler(e, 500)

@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    Видалити товар
    ---
    parameters:
      - name: product_id
        in: path
        type: integer
    responses:
      204:
        description: Товар видалений
      404:
        description: Товар не знайдено
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'status': 'error', 'message': 'Product not found'}), 404
        
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()
        
        return '', 204
    except Exception as e:
        return error_handler(e, 500)
