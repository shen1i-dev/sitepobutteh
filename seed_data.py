from models import get_db_connection, init_db

def seed_products():
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
    
    conn.executemany('INSERT INTO products (name, price, image) VALUES (?, ?, ?)', products)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_products()
    print("Тестові продукти додано до бази даних.")