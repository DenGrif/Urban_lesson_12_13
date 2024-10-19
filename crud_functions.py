import sqlite3

def initiate_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT NOT NULL,
                        price INTEGER NOT NULL
                    )''')
    conn.commit()
    conn.close()


# Получаем все продукты из базы данных
def get_all_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()

    conn.close()
    return products


# Добавление продукта в базу данных
def add_product(title, description, price):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)", (title, description, price))
    conn.commit()
    conn.close()


initiate_db()

# Вливаем в неё данные
add_product("Игра 1", "Небольшая игра", 1000)
add_product("Игра 2", "Средняя игра", 2000)
add_product("Игра 3", "Большая игра", 3000)
add_product("Игра 4", "Очень большая игра", 4000)

print("База данных заполнена.")
