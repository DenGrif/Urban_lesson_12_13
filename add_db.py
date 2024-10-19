from crud_functions import add_product, initiate_db

# Запускаем функцию
initiate_db()

# И добавляем в неё данные
add_product("Игра 1", "Небольшая игра", 1000)
add_product("Игра 2", "Средняя игра", 2000)
add_product("Игра 3", "Большая игра", 3000)
add_product("Игра 4", "Очень большая игра", 4000)

print("База данных заполнена.")
