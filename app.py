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

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
# Can be a full SQLAlchemy URI (e.g., sqlite:///db.sqlite) or a filesystem path (e.g., /data/db.sqlite)
DATABASE_PATH = os.environ.get('DATABASE_PATH', 'db.sqlite')
FLASK_ENV = os.environ.get('FLASK_ENV', 'development')

app.secret_key = SECRET_KEY
# Normalize DATABASE_PATH into a valid SQLAlchemy URI
if DATABASE_PATH.startswith('sqlite:'):
    db_uri = DATABASE_PATH
else:
    # Prepend sqlite:/// to relative or absolute filesystem path
    # For absolute paths, this results in sqlite:////<abs-path>, which SQLAlchemy expects
    db_uri = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['JSON_SORT_KEYS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

CORS(app, resources={r"/api/*": {"origins": "*"}})

init_db()
db = SQLAlchemy(app)
swagger = Flasgger(app)

# Ensure SQLite directory exists even when running under gunicorn (no __main__)
try:
    uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if uri.startswith('sqlite:///'):
        db_file = uri.replace('sqlite:///', '', 1)
        db_dir = os.path.dirname(db_file) or '.'
        os.makedirs(db_dir, exist_ok=True)
    # Initialize tables if not present
    with app.app_context():
        db.create_all()
except Exception as e:
    # Avoid import-time crashes in production; table init can also be run later
    pass

app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(accounts_bp)

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

@app.route('/health')
def health():
    try:
        return {'status': 'healthy', 'environment': FLASK_ENV}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500

if __name__ == '__main__':
    # Ensure local development creates DB directory
    try:
        uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if uri.startswith('sqlite:///'):
            db_file = uri.replace('sqlite:///', '', 1)
            db_dir = os.path.dirname(db_file) or '.'
            os.makedirs(db_dir, exist_ok=True)
        with app.app_context():
            db.create_all()
    except Exception:
        pass

    debug_mode = FLASK_ENV == 'development'
    # Respect PORT env for platforms like Render; default 5000 locally
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)