from flask import Flask, render_template, session
from models import init_db
from routes.feedback import feedback_bp
from routes.admin import admin_bp
from routes.shop import shop_bp
from routes.accounts import accounts_bp
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Flasgger
from datetime import timedelta
import os

app = Flask(__name__)

# Отримуємо змінні середовища
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
DATABASE_PATH = os.environ.get('DATABASE_PATH', 'sqlite:///db.sqlite')
FLASK_ENV = os.environ.get('FLASK_ENV', 'development')

# Налаштування Flask
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}' if DATABASE_PATH.endswith('.db') else DATABASE_PATH
app.config['JSON_SORT_KEYS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

# CORS конфігурація для дозволу запитів з браузера
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Ініціалізація бази даних
init_db()
db = SQLAlchemy(app)
swagger = Flasgger(app)

# Реєстрація блюпрінтів
app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(accounts_bp)

# Реєстрація API blueprints
from routes.api.products import products_bp as products_api_bp
from routes.api.orders import orders_bp as orders_api_bp
from routes.api.feedback import feedback_bp as feedback_api_bp
from routes.api.users import users_bp as users_api_bp

app.register_blueprint(products_api_bp, url_prefix='/api/v1/products')
app.register_blueprint(orders_api_bp, url_prefix='/api/v1/orders')
app.register_blueprint(feedback_api_bp, url_prefix='/api/v1/feedback')
app.register_blueprint(users_api_bp, url_prefix='/api/v1/users')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api-products')
def api_products():
    return render_template('api_products.html')

# Health check endpoint
@app.route('/health')
def health():
    try:
        # Перевіряємо доступність застосунку
        return {'status': 'healthy', 'environment': FLASK_ENV}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500

if __name__ == '__main__':
    # Створюємо директорію для бази даних, якщо її немає
    os.makedirs(os.path.dirname(DATABASE_PATH) if DATABASE_PATH != 'sqlite:///db.sqlite' else 'data', exist_ok=True)
    
    # Ініціалізуємо базу даних
    with app.app_context():
        db.create_all()
    
    # Запускаємо сервер на всіх інтерфейсах (необхідно для контейнера)
    debug_mode = FLASK_ENV == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)