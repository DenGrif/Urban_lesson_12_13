from crud_functions import add_product, initiate_db

# Запускаем функцию
initiate_db()

# И добавляем в неё данные
add_product("Игра 1", "Небольшая игра", 1000, "Lgame.jpg")
add_product("Игра 2", "Средняя игра", 2000, "Mgame.jpg")
add_product("Игра 3", "Большая игра", 3000, "XLgame.jpg")
add_product("Игра 4", "Очень большая игра", 4000, "XXLgame.jpg")

print("База данных заполнена.")
