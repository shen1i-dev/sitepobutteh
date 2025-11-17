import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'db.sqlite')

def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _conn()
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        message TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        price REAL DEFAULT 0,
        stock INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        status TEXT DEFAULT 'pending',
        total REAL DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price REAL
    )
    ''')

    # services and service_orders
    cur.execute('''
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS service_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        price_at_order REAL NOT NULL,
        total REAL NOT NULL,
        client_id INTEGER,
        name TEXT,
        email TEXT,
        status TEXT NOT NULL DEFAULT 'new',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

# Feedback helpers
def get_feedbacks():
    conn = _conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, email, message, created_at FROM feedback ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_feedback(fid):
    conn = _conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM feedback WHERE id = ?', (fid,))
    conn.commit()
    conn.close()

# create a feedback record
def create_feedback(name, email, message):
    conn = _conn()
    cur = conn.cursor()
    # Use parameterized query to prevent injection; created_at has a default so we can omit it
    cur.execute('INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)', (name, email, message))
    conn.commit()
    fid = cur.lastrowid
    conn.close()
    return fid

# Products
def create_product(name, description, price, stock=0):
    conn = _conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)', (name, description, float(price), int(stock)))
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return pid

def get_products():
    conn = _conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, description, price, stock FROM products ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_product(pid):
    conn = _conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM products WHERE id = ?', (pid,))
    conn.commit()
    conn.close()

# Orders (basic)
def get_orders():
    conn = _conn()
    cur = conn.cursor()
    cur.execute('SELECT id, client_id, status, total, created_at FROM orders ORDER BY created_at DESC')
    rows = cur.fetchall()
    conn.close()
    return rows

def get_order_items(order_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute('SELECT id, order_id, product_id, quantity, price FROM order_items WHERE order_id = ?', (order_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def update_order_status(order_id, status):
    conn = _conn()
    cur = conn.cursor()
    cur.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    conn.commit()
    conn.close()

# Clients
def create_client(name, email, phone):
    conn = _conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO clients (name, email, phone) VALUES (?, ?, ?)', (name, email, phone))
    conn.commit()
    cid = cur.lastrowid
    conn.close()
    return cid

def get_clients():
    conn = _conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, email, phone FROM clients ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    return rows

# Services
def create_service(name, description, price):
    conn = _conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO services (name, description, price) VALUES (?, ?, ?)', (name, description, float(price)))
    conn.commit()
    sid = cur.lastrowid
    conn.close()
    return sid

def get_services():
    conn = _conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, description, price FROM services ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    return rows

def get_service(service_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute('SELECT id, name, description, price FROM services WHERE id = ?', (service_id,))
    row = cur.fetchone()
    conn.close()
    return row

def delete_service(service_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM services WHERE id = ?', (service_id,))
    conn.commit()
    conn.close()

# Service orders
def create_service_order(service_id, quantity=1, client_id=None, name=None, email=None):
    conn = _conn()
    cur = conn.cursor()
    cur.execute('SELECT price FROM services WHERE id = ?', (service_id,))
    r = cur.fetchone()
    if not r:
        conn.close()
        raise ValueError('Послуга не знайдена')
    price = float(r['price'])
    q = int(quantity)
    total = price * q
    cur.execute('''
        INSERT INTO service_orders (service_id, quantity, price_at_order, total, client_id, name, email, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (service_id, q, price, total, client_id, name, email, 'new'))
    conn.commit()
    oid = cur.lastrowid
    conn.close()
    return oid

def get_service_orders():
    conn = _conn()
    cur = conn.cursor()
    cur.execute('''
      SELECT so.id, so.service_id, s.name AS service_name, so.quantity, so.price_at_order, so.total, so.name, so.email, so.status, so.created_at
      FROM service_orders so
      LEFT JOIN services s ON s.id = so.service_id
      ORDER BY so.created_at DESC
    ''')
    rows = cur.fetchall()
    conn.close()
    return rows

def update_service_order_status(order_id, status):
    conn = _conn()
    cur = conn.cursor()
    cur.execute('UPDATE service_orders SET status = ? WHERE id = ?', (status, order_id))
    conn.commit()
    conn.close()