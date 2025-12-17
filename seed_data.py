from models import get_db_connection, init_db

def seed_products():
    """Legacy seeding (non-idempotent). Prefer ensure_seed_products()."""
    init_db()
    conn = get_db_connection()
    products = [
        ('Пральна машинка', 6999.99, 'https://cdn.27.ua/original/35/73/6632819_1.jpeg'),
        ('Телевізор', 2999.99, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1UYZhs0mhNAEk0pW617O1Bcj75q2nKVC_tQ&s'),
        ('Холодильник', 12499.99, 'https://bs-partner.com.ua/upload/iblock/c61/akpyh96q9psj4sz3s4b43qthwq74loyu/KGN86AI32U.jpg'),
        ('Колонки', 15599.99, 'https://uastore.com.ua/files/resized/products/99Afiudg.1800x1800w.jpg'),
        ('Мікрохвильова піч', 1999.99, '/api/placeholder/200/200'),
        ('Ноутбук', 4999.99, '/api/placeholder/200/200'),
        ('Кондиціонер', 6599.99, '/api/placeholder/200/200'),
        ('Принтер', 2499.99, '/api/placeholder/200/200'),
    ]
    conn.executemany('INSERT INTO products (name, price, image) VALUES (?, ?, ?)')
    conn.commit()
    conn.close()

def ensure_seed_products():
    """Insert demo products only if the products table is empty (idempotent)."""
    init_db()
    conn = get_db_connection()
    try:
        row = conn.execute('SELECT COUNT(*) AS cnt FROM products').fetchone()
        count = row['cnt'] if row and 'cnt' in row.keys() else 0
    except Exception:
        count = 0

    if count and int(count) > 0:
        conn.close()
        return False

    products = [
        ('Пральна машинка', 6999.99, 'https://cdn.27.ua/original/35/73/6632819_1.jpeg'),
        ('Телевізор', 2999.99, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1UYZhs0mhNAEk0pW617O1Bcj75q2nKVC_tQ&s'),
        ('Холодильник', 12499.99, 'https://bs-partner.com.ua/upload/iblock/c61/akpyh96q9psj4sz3s4b43qthwq74loyu/KGN86AI32U.jpg'),
        ('Колонки', 15599.99, 'https://uastore.com.ua/files/resized/products/99Afiudg.1800x1800w.jpg'),
        ('Мікрохвильова піч', 1999.99, '/api/placeholder/200/200'),
        ('Ноутбук', 4999.99, '/api/placeholder/200/200'),
        ('Кондиціонер', 6599.99, '/api/placeholder/200/200'),
        ('Принтер', 2499.99, '/api/placeholder/200/200'),
    ]
    conn.executemany('INSERT INTO products (name, price, image) VALUES (?, ?, ?)', products)
    conn.commit()
    conn.close()
    return True

if __name__ == '__main__':
    inserted = ensure_seed_products()
    if inserted:
        print("Тестові продукти додано до бази даних.")
    else:
        print("Сидінг пропущено: продукти вже існують.")