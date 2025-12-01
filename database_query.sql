-- SQL запрос для выполнения задания
-- Расчет количества оборудования и стоимости по регионам

SELECT 
    r.region_name AS "Регион",
    SUM(e.quantity) AS "Количество_оборудования",
    SUM(e.cost * e.quantity) AS "Суммарная_стоимость"
FROM table4_equipment e
JOIN sp_region r ON e.region_id = r.region_id
GROUP BY r.region_name
ORDER BY r.region_name;
