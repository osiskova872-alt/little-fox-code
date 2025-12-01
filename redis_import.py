"""
СКРИПТ ДЛЯ ИМПОРТА ДАННЫХ ИЗ NANOEDU В REDIS
Задание: рассчитать количество оборудования и стоимость по регионам
"""

def print_instructions():
    print("=" * 70)
    print("ИНСТРУКЦИЯ ПО ВЫПОЛНЕНИЮ ЗАДАНИЯ")
    print("=" * 70)
    print()
    print("1. SQL ЗАПРОС (выполнить в PostgreSQL nanoedu):")
    print("-" * 40)
    print("""
    SELECT 
        r.region_name,
        SUM(e.quantity) as total_units,
        SUM(e.cost * e.quantity) as total_cost
    FROM table4_equipment e
    JOIN sp_region r ON e.region_id = r.region_id
    GROUP BY r.region_name
    ORDER BY r.region_name;
    """)
    print()
    
    print("2. ПРИМЕР РЕЗУЛЬТАТА SQL ЗАПРОСА:")
    print("-" * 40)
    example_data = [
        ("Москва", 150, 7500000),
        ("Санкт-Петербург", 90, 4500000),
        ("Новосибирск", 60, 3000000),
        ("Екатеринбург", 45, 2250000)
    ]
    
    print(f"{'Регион':<20} {'Количество':<12} {'Стоимость':<15}")
    print("-" * 40)
    for region, units, cost in example_data:
        print(f"{region:<20} {units:<12} {cost:<15}")
    print()
    
    print("3. КОД ДЛЯ ЗАГРУЗКИ В REDIS:")
    print("-" * 40)
    print("""
    import redis
    
    # Подключение к Redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    # Пример данных (заменить на реальные результаты)
    regions_data = [
        ("Москва", 150, 7500000),
        ("Санкт-Петербург", 90, 4500000),
        ("Новосибирск", 60, 3000000),
    ]
    
    # Загрузка данных в Redis
    for region, units, cost in regions_data:
        key = f"equipment:region:{region}"
        data = {
            'total_units': str(units),
            'total_cost': str(cost),
            'region': region
        }
        r.hset(key, mapping=data)
        print(f"Сохранено: {key}")
    
    print("✅ Данные загружены в Redis!")
    """)
    print()
    
    print("4. КОМАНДЫ ДЛЯ ПРОВЕРКИ В REDIS:")
    print("-" * 40)
    print("""
    $ redis-cli
    127.0.0.1:6379> KEYS equipment:region:*
    1) "equipment:region:Москва"
    2) "equipment:region:Санкт-Петербург"
    
    127.0.0.1:6379> HGETALL equipment:region:Москва
    1) "total_units"
    2) "150"
    3) "total_cost"
    4) "7500000"
    5) "region"
    6) "Москва"
    """)
    
    print("=" * 70)
    print("СКРИНШОТЫ ДЛЯ ОТЧЕТА:")
    print("1. Результат SQL запроса в pgAdmin/HeidiSQL")
    print("2. Запуск Python скрипта в терминале")
    print("3. Результат в Redis CLI")
    print("=" * 70)

if __name__ == "__main__":
    print_instructions()
