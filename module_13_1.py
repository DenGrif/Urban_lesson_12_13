import asyncio

# Функция для каждого силача
async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')

    # Первая часть задачи, поднятие 5 шаров
    for i in range(1, 6):
        await asyncio.sleep(1 / power)
        print(f'Силач {name} поднял {i} шар')

    print(f'Силач {name} закончил соревнования.')

# Вторая часть задачи функция для запуска соревнований
async def start_tournament():
    tasks = [
        asyncio.create_task(start_strongman('Паша', 3)),
        asyncio.create_task(start_strongman('Денис', 4)),
        asyncio.create_task(start_strongman('Антон', 5)),
    ]

    # Ждёмс завершения всех задач
    await asyncio.gather(*tasks)


# Запуск
asyncio.run(start_tournament())
