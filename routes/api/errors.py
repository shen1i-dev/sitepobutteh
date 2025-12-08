from flask import jsonify

def error_handler(exception, status_code):
    """Універсальна обробка помилок"""
    return jsonify({
        'status': 'error',
        'message': str(exception),
        'code': status_code
    }), status_code
