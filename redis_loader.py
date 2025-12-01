#!/usr/bin/env python3
"""
Скрипт для импорта данных из PostgreSQL (nanoedu) в Redis
Задание для 22ГМУ-УЦП11.2
"""

print("=" * 60)
print("СКРИПТ ДЛЯ ИМПОРТА ДАННЫХ ИЗ NANOEDU В REDIS")
print("=" * 60)

# ИНСТРУКЦИЯ
print("\n📋 ИНСТРУКЦИЯ:")
print("1. Установите Redis: sudo apt install redis-server")
print("2. Запустите Redis: redis-server")
print("3. Установите библиотеки: pip install redis psycopg2-binary")
print("4. Настройте подключение к БД nanoedu ниже")
print("5. Запустите скрипт: python redis_loader.py")

# КОД ДЛЯ КОПИРОВАНИЯ
print("\n" + "=" * 60)
print("КОД ДЛЯ ВСТАВКИ В ФАЙЛ И ВЫПОЛНЕНИЯ:")
print("=" * 60)

code = '''
import psycopg2
import redis

def connect_to_databases():
    """Подключение к PostgreSQL и Redis"""
    
    # 1. ПОДКЛЮЧЕНИЕ К POSTGRESQL (NANOEDU)
    print("\\n1. Подключаемся к PostgreSQL (nanoedu)...")
    try:
        # ЗАМЕНИТЕ ЭТИ ДАННЫЕ НА СВОИ!
        conn = psycopg2.connect(
            host="localhost",      # или адрес сервера
            database="nanoedu",    # имя базы данных
            user="ваш_логин",      # ваш логин
            password="ваш_пароль", # ваш пароль
            port=5432
        )
        cursor = conn.cursor()
        print("   ✅ PostgreSQL подключен")
    except Exception as e:
        print(f"   ❌ Ошибка PostgreSQL: {e}")
        return None, None
    
    # 2. ПОДКЛЮЧЕНИЕ К REDIS
    print("2. Подключаемся к Redis...")
    try:
        r = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
        # Проверка подключения
        if r.ping():
            print("   ✅ Redis подключен")
        else:
            print("   ❌ Redis не отвечает")
            return None, None
    except Exception as e:
        print(f"   ❌ Ошибка Redis: {e}")
        return None, None
    
    return conn, cursor, r

def execute_sql_query(cursor):
    """Выполнение SQL запроса"""
    print("\\n3. Выполняем SQL запрос...")
    
    sql = """
    SELECT 
        r.region_name,
        SUM(e.quantity) as total_units,
        SUM(e.cost * e.quantity) as total_cost
    FROM table4_equipment e
    JOIN sp_region r ON e.region_id = r.region_id
    GROUP BY r.region_name
    ORDER BY r.region_name;
    """
    
    cursor.execute(sql)
    results = cursor.fetchall()
    print(f"   ✅ Получено {len(results)} записей")
    
    # Вывод результатов
    print("\\n   📊 Результаты:")
    print("   " + "-" * 45)
    print(f"   {"Регион":<20} {"Кол-во":<10} {"Стоимость":<12}")
    print("   " + "-" * 45)
    
    for row in results[:5]:  # Показываем первые 5
        print(f"   {row[0]:<20} {row[1]:<10} {row[2]:<12}")
    
    if len(results) > 5:
        print(f"   ... и ещё {len(results) - 5} регионов")
    
    return results

def save_to_redis(redis_client, data):
    """Сохранение данных в Redis"""
    print("\\n4. Сохраняем данные в Redis...")
    
    for region, units, cost in data:
        # Формируем ключ
        key = f"equipment:region:{region}"
        
        # Данные для сохранения
        redis_data = {
            'total_units': str(units),
            'total_cost': str(cost),
            'region_name': region
        }
        
        # Сохраняем как хэш
        redis_client.hset(key, mapping=redis_data)
        print(f"   💾 {key}")
    
    print(f"\\n   ✅ Сохранено {len(data)} записей в Redis")

def main():
    """Основная функция"""
    conn, cursor, redis_client = connect_to_databases()
    
    if not all([conn, cursor, redis_client]):
        print("\\n❌ Не удалось подключиться к базам данных")
        return
    
    try:
        # Получаем данные из PostgreSQL
        data = execute_sql_query(cursor)
        
        if data:
            # Сохраняем в Redis
            save_to_redis(redis_client, data)
            
            # Проверяем сохранение
            print("\\n5. Проверяем данные в Redis...")
            test_key = f"equipment:region:{data[0][0]}"
            test_data = redis_client.hgetall(test_key)
            
            print(f"\\n   Пример данных (ключ: {test_key}):")
            for key, value in test_data.items():
                print(f"   {key}: {value}")
        
        print("\\n" + "=" * 60)
        print("🎉 ЗАДАНИЕ ВЫПОЛНЕНО!")
        print("=" * 60)
        print("\\n📸 ДЛЯ ОТЧЕТА СДЕЛАЙТЕ СКРИНШОТЫ:")
        print("1. Результат SQL запроса")
        print("2. Вывод этого скрипта")
        print("3. Команды в Redis CLI: KEYS * и HGETALL")
        
    except Exception as e:
        print(f"\\n❌ Ошибка: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("\\n🔌 Соединения закрыты")

if __name__ == "__main__":
    main()
'''

print(code)
print("\n" + "=" * 60)
print("📝 ЗАМЕНИТЕ В КОДЕ:")
print("   host, database, user, password - на свои данные!")
print("=" * 60)

# КОМАНДЫ ДЛЯ ПРОВЕРКИ
print("\n🔍 КОМАНДЫ ДЛЯ ПРОВЕРКИ В REDIS CLI:")
print("""
$ redis-cli
127.0.0.1:6379> KEYS equipment:region:*
127.0.0.1:6379> HGETALL equipment:region:Москва
127.0.0.1:6379> HGET equipment:region:Москва total_units
127.0.0.1:6379> HGET equipment:region:Москва total_cost
""")

print("\n" + "=" * 60)
print("✅ Файл готов! Запустите: python redis_loader.py")
print("=" * 60)
