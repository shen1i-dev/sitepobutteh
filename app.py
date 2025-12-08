from flask import Flask, render_template, session
from models import init_db
from routes.feedback import feedback_bp
from routes.admin import admin_bp
from routes.shop import shop_bp
from routes.accounts import accounts_bp
from flask_sqlalchemy import SQLAlchemy
from flasgger import Flasgger
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Необхідно для роботи з сесіями
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['JSON_SORT_KEYS'] = False

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)