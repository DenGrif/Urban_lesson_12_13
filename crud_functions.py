import sqlite3
def initiate_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT NOT NULL,
                        price INTEGER NOT NULL,
                        image_path TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()


# Добавление игр с картинками
def add_product(title, description, price, image_path):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Products (title, description, price, image_path) VALUES (?, ?, ?, ?)",
                   (title, description, price, image_path))
    conn.commit()
    conn.close()


# Возвращает все записи из таблицы
def get_all_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()

    conn.close()
    return products
