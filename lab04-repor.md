# Звіт з лабораторної роботи 4

## Реалізація бази даних для вебпроєкту

### Інформація про команду
- Назва команди: Немає команди

- Учасники:
  - Кравчук Владислав Вікторович

## Завдання

### Обрана предметна область

Опишіть предметну область вашого вебзастосунку та які дані потрібно зберігати (наприклад: інтернет-магазин, система бронювання, блог з коментарями тощо).:
Побутова техніка, можна купувати техніку

### Реалізовані вимоги

Вкажіть, які рівні завдань було виконано:

- [Виконано] Рівень 1: Створено базу даних SQLite з таблицею для відгуків, реалізовано базові CRUD операції, створено адмін-панель для перегляду та видалення відгуків, додано функціональність магазину з таблицями для товарів та замовлень
- [Виконано] Рівень 2: Створено додаткову таблицю, релевантну предметній області, реалізовано роботу з новою таблицею через адмін-панель, інтегровано функціональність у застосунок
- [ ] Рівень 3: Розширено функціональність двома додатковими функціями, що суттєво покращують користувацький досвід

## Хід виконання роботи

### Підготовка середовища розробки

Опишіть процес налаштування:

- Версія Python:
Python 3.12+
- Встановлені бібліотеки (Flask, SQLite3 тощо):
Flask==2.3.0+
Flask-SQLAlchemy==3.0.0+
SQLite3 (вбудована в Python)
Werkzeug==2.3.0+
Jinja2==3.1.0+
- Інші використані інструменти та розширення:
Git
Visual Studio Code

### Структура проєкту

Наведіть структуру файлів та директорій вашого проєкту:

```
site/
├── app.py
├── models.py
├── requirements.txt
├── db.sqlite
├── routes/
│   ├── __init__.py
│   ├── accounts.py
│   ├── admin.py
│   ├── feedback.py
│   ├── shop.py
│   └── __pycache__/
├── templates/
│   ├── base.html
│   ├── about.html
│   ├── accounts.html
│   ├── admin.html
│   ├── cart.html
│   ├── feedback.html
│   ├── home.html
│   ├── order_details.html
│   └── shop.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
├── __pycache__/
├── lab-reports/
│   └── lab04-report.md
└── .gitignore
```

### Проектування бази даних

#### Схема бази даних

Опишіть структуру вашої бази даних:

```
Таблиця "feedback":
- id (INTEGER, PRIMARY KEY)
- name (TEXT, NOT NULL)
- email (TEXT, NOT NULL)
- message (TEXT, NOT NULL)
- rating (INTEGER, DEFAULT 5)
- created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

Таблиця "products":
- id (INTEGER, PRIMARY KEY)
- name (TEXT, NOT NULL)
- description (TEXT)
- category (TEXT)
- price (REAL, NOT NULL)
- stock (INTEGER, DEFAULT 0)
- image_url (TEXT)
- created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

Таблиця "orders":
- id (INTEGER, PRIMARY KEY)
- customer_name (TEXT, NOT NULL)
- customer_email (TEXT, NOT NULL)
- total_amount (REAL, NOT NULL)
- status (TEXT, DEFAULT 'pending')
- shipping_address (TEXT)
- created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

Таблиця "order_items":
- id (INTEGER, PRIMARY KEY)
- order_id (INTEGER, FOREIGN KEY)
- product_id (INTEGER, FOREIGN KEY)
- quantity (INTEGER, NOT NULL)
- price (REAL, NOT NULL)

Таблиця "users":
- id (INTEGER, PRIMARY KEY)
- username (TEXT, UNIQUE, NOT NULL)
- email (TEXT, UNIQUE, NOT NULL)
- password (TEXT, NOT NULL)
- role (TEXT, DEFAULT 'user')
- created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
```



### Опис реалізованої функціональності

#### Система відгуків

Опишіть реалізацію системи збору та відображення відгуків користувачів.:
- Форма для збору відгуків з полями: ім'я, email, повідомлення, рейтинг
- Збереження відгуків у таблиці "feedback"
- Адмін-панель для перегляду та видалення відгуків

#### Магазин

Опишіть функціональність магазину:

- Відображення каталогу товарів
- Додавання товарів до кошика
- Оформлення замовлення
- Управління товарами через адмін-панель

#### Адміністративна панель

Опишіть можливості адмін-панелі:

- Перегляд відгуків
- Управління товарами
- Управління замовленнями
- Перегляд зареєстрованих користувачів

#### Додаткова функціональність (якщо реалізовано)

Опишіть додаткові таблиці та функції, які було реалізовано для рівнів 2 та 3.:
- Таблиця "users" для зберігання інформації про користувачів
- Реєстрація користувачів

## Ключові фрагменти коду
```python
# filepath: models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    shipping_address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

### Ініціалізація бази даних

Наведіть код створення таблиць у файлі `models.py`:

```python
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    # Створення таблиці feedback
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            rating INTEGER DEFAULT 5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Створення таблиці products
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Створення таблиці orders
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            shipping_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Створення таблиці order_items
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    # Створення таблиці users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Викликати при запуску додатку
if __name__ == '__main__':
    init_db()

### CRUD операції

Наведіть приклади реалізації CRUD операцій:

#### Створення (Create)

```python
def add_feedback(name, email, message):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)',
        (name, email, message)
    )
    conn.commit()
    conn.close()
```

#### Читання (Read)

```python
def get_all_feedback():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM feedback ORDER BY created_at DESC')
    feedback = cursor.fetchall()
    conn.close()
    return feedback
```

#### Оновлення (Update)

```python
def update_order_status(order_id, status):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE orders SET status = ? WHERE id = ?',
        (status, order_id)
    )
    conn.commit()
    conn.close()
```

#### Видалення (Delete)

```python
def delete_feedback(feedback_id):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
    conn.commit()
    conn.close()
```

### Маршрутизація

Наведіть приклади маршрутів для роботи з базою даних:

```python
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        add_feedback(name, email, message)
        flash('Дякуємо за ваш відгук!', 'success')
        return redirect(url_for('feedback'))
    return render_template('feedback.html')
```

### Робота зі зв'язками між таблицями

Наведіть приклад запиту з використанням JOIN для отримання пов'язаних даних:

```python
def get_order_details(order_id):
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT o.*, oi.quantity, p.name, p.price
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        WHERE o.id = ?
    ''', (order_id,))
    details = cursor.fetchall()
    conn.close()
    return details
```

## Розподіл обов'язків у команді

Опишіть внесок кожного учасника команди:

- Кравчук Владислав Вікторович: Всю роботу виконано самостійно

## Тестування

### Сценарії тестування

Опишіть, які сценарії ви тестували:

1. Додавання нового відгуку та перевірка його відображення в адмін-панелі
2. Створення товару, додавання його до кошика та оформлення замовлення
3. Зміна статусу замовлення через адмін-панель
4. Видалення записів з бази даних
5. Перевірка валідації даних
6. Тестування реєстрації користувачів
7. Чи працює пошта зворотнього зв'язку


## Висновки

Опишіть:

- Що вдалося реалізувати успішно:
Додати нову базу даних, покращити сторінку зворотній зв'язок
- Які навички роботи з базами даних отримали:
Навчився створювати базу даних, таблиці та працювати з ними
- Які труднощі виникли при проектуванні схеми БД:
Труднощі були з базою даних, але я все вирішив
- Як організували командну роботу:
Роботу організував самостійно
- Які покращення можна внести в майбутньому:
Додати до авторизації більше функціонала

Очікувана оцінка: [8 балів]

Обґрунтування: Виконав всі вимоги рівнів 1 та 2
