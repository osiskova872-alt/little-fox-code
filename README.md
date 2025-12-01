# 🦊 little-fox-code

## 📋 Задание: Импорт данных из nanoedu в Redis

**Выполнил:** Шишкова Олеся  
**Группа:** [22ГМУ-УЦП11.2]  
**Дата:** $(date +%d.%m.%Y)

---

## 🎯 Цель задания
На основе базы данных `nanoedu`:
1. Использовать поля `full_name` таблицы `table4_equipment`
2. Рассчитать **количество единиц оборудования** (2 вариант)
3. Рассчитать **суммарную стоимость** (1 вариант)
4. В разрезе регионов (таблица `sp_region`)
5. Залить соответствующую таблицу в Redis в виде пар **ключ-значение**

---

## 📁 Файлы в репозитории

| Файл | Назначение |
|------|------------|
| [`database_query.sql`](database_query.sql) | SQL запрос для выполнения |
| [`redis_loader.py`](redis_loader.py) | Python скрипт для загрузки в Redis |
| [`instructions.md`](instructions.md) | Подробная инструкция |
| [`screenshots/`](screenshots/) | Папка со скриншотами |

---

## 🔧 Технологии
- **PostgreSQL** (база nanoedu)
- **Redis** (хранилище ключ-значение)
- **Python 3** (скрипт для импорта)

---

## 📊 SQL запрос (основной)

```sql
-- Файл: database_query.sql
SELECT 
    r.region_name AS "Регион",
    SUM(e.quantity) AS "Количество_оборудования",
    SUM(e.cost * e.quantity) AS "Суммарная_стоимость"
FROM table4_equipment e
JOIN sp_region r ON e.region_id = r.region_id
GROUP BY r.region_name
ORDER BY r.region_name;# little-fox-code
