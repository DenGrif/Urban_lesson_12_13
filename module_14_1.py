import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

# Таблица Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL
)
''')

# Заполняем её 10ю записями
users_data = [
    ('User1', 'example1@gmail.com', 10, 1000),
    ('User2', 'example2@gmail.com', 20, 1000),
    ('User3', 'example3@gmail.com', 30, 1000),
    ('User4', 'example4@gmail.com', 40, 1000),
    ('User5', 'example5@gmail.com', 50, 1000),
    ('User6', 'example6@gmail.com', 60, 1000),
    ('User7', 'example7@gmail.com', 70, 1000),
    ('User8', 'example8@gmail.com', 80, 1000),
    ('User9', 'example9@gmail.com', 90, 1000),
    ('User10', 'example10@gmail.com', 100, 1000)
]

cursor.executemany("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)", users_data)

# Обновляем balance
cursor.execute("UPDATE Users SET balance = 500 WHERE id % 2 = 1")

# Получаем все записи из таблицы,
# чтоб потом из этого списка удалить каждую 3ю
cursor.execute("SELECT id FROM Users ORDER BY id")
all_ids = cursor.fetchall()

# Удаляем каждую 3-ю запись, начиная с первой
for i in range(0, len(all_ids), 3):
    cursor.execute("DELETE FROM Users WHERE id = ?", (all_ids[i][0],))

# Записи, где возраст не равен 60
cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != 60")
users = cursor.fetchall()

for user in users:
    print(f"Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}")

connection.commit()
connection.close()
