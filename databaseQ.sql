--SQL queries 

--Task 1
-- SELECT country_code, COUNT(country_code) as total_no_stores
-- FROM dim_store_details
-- GROUP BY country_code
-- ORDER BY total_no_stores desc;


--Task 2
-- SELECT locality, count(locality) as total_no_stores
-- FROM dim_store_details
-- GROUP BY locality
-- ORDER BY total_no_stores desc
-- limit 10;


--Task 3
-- SELECT SUM(dim_products.product_price * product_quantity) as total_sales, dim_date_times.month
-- FROM orders_table
-- 	LEFT JOIN dim_date_times on orders_table.date_uuid = dim_date_times.date_uuid
-- 	LEFT JOIN dim_products on orders_table.product_code = dim_products.product_code
-- GROUP BY dim_date_times.month
-- ORDER BY total_sales desc;


--Task 4
-- SELECT store_type
-- FROM dim_store_details
-- WHERE store_type = 'Web Portal';

-- SELECT 
-- 	COUNT(orders_table.product_quantity) as total_sales,
-- 	SUM(orders_table.product_quantity) as product_quantity_count,
-- 	CASE 
-- 		WHEN dim_store_details.store_type = 'Web Portal' then 'Web'
-- 		ELSE 'Offline'
-- 	END AS location
-- FROM orders_table
-- 	LEFT Join dim_store_details on orders_table.store_code = dim_store_details.store_code
-- GROUP BY location
-- ORDER BY product_quantity_count;


--Task 5
-- SELECT 
--     dim_store_details.store_type,
--     SUM(CAST(REPLACE(dim_products.product_price, '£', '') AS NUMERIC) * orders_table.product_quantity) AS total_sales,
--     ROUND(SUM(CAST(REPLACE(dim_products.product_price, '£', '') AS NUMERIC) * orders_table.product_quantity) * 100.0 / total.total_sales, 2) AS percentage_total
-- FROM 
--     orders_table
-- LEFT JOIN 
--     dim_products ON orders_table.product_code = dim_products.product_code
-- LEFT JOIN 
--     dim_store_details ON orders_table.store_id = dim_store_details.store_id
-- LEFT JOIN 
--     (
--         SELECT 
--             dim_store_details.store_type,
--             SUM(CAST(REPLACE(dim_products.product_price, '£', '') AS NUMERIC) * orders_table.product_quantity) AS total_sales
--         FROM 
--             orders_table
--         LEFT JOIN 
--             dim_products ON orders_table.product_code = dim_products.product_code
--         LEFT JOIN 
--             dim_store_details ON orders_table.store_id = dim_store_details.store_id
--         GROUP BY 
--             dim_store_details.store_type
--     ) AS total ON 1=1
-- GROUP BY 
--     dim_store_details.store_type, total.total_sales
-- ORDER BY 
--     total_sales DESC;


--Task 6 query
-- SELECT 
--     total_sales,
--     year,
--     month
-- FROM (
--     SELECT 
--         SUM(CAST(REPLACE(dim_products.product_price, '£', '') AS NUMERIC) * orders_table.product_quantity) AS total_sales,
--         dim_date_times.year,
--         dim_date_times.month
--     FROM orders_table
--     LEFT JOIN dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid
--     LEFT JOIN dim_products ON orders_table.product_code = dim_products.product_code
--     GROUP BY dim_date_times.year, dim_date_times.month
-- ) AS monthly_sales
-- ORDER BY total_sales DESC
-- LIMIT 10;


--Task 7
-- SELECT table_name
-- FROM information_schema.tables
-- WHERE table_schema = 'public'
-- AND table_type = 'BASE TABLE';
-- SELECT SUM(staff_numbers) AS total_staff_numbers,
--     country_code
-- FROM dim_store_details
-- GROUP BY country_code
-- ORDER BY total_staff_numbers DESC;


-- Task 8
--  SELECT 
-- 	COUNT(orders_table.user_uuid) as total_sales,
-- 	dim_store_details.store_type,
-- 	MAX(dim_store_details.country_code) as country_code
-- FROM orders_table
-- 	LEFT JOIN dim_store_details on orders_table.store_code = dim_store_details.store_code
-- 	LEFT JOIN dim_products on orders_table.product_code = dim_products.product_code
-- WHERE dim_store_details.country_code = 'DE'
-- GROUP BY dim_store_details.store_type;


--Task 9 
-- Get average time between sales per year
-- WITH TIME_BETWEEN_SALES AS (
--     SELECT dates.year,
--         LEAD(
--             TO_TIMESTAMP(
--                 dates.year || '-' || dates.month || '-' || dates.day || ' ' || dates.timestamp,
--                 'YYYY-MM-DD HH24:MI:SS.FF'
--             )
--         ) OVER (
--             PARTITION BY dates.year
--             ORDER BY TO_TIMESTAMP(
--                     dates.year || '-' || dates.month || '-' || dates.day || ' ' || dates.timestamp,
--                     'YYYY-MM-DD HH24:MI:SS.FF'
--                 )
--         ) - TO_TIMESTAMP(
--             dates.year || '-' || dates.month || '-' || dates.day || ' ' || dates.timestamp,
--             'YYYY-MM-DD HH24:MI:SS.FF'
--         ) AS time_between_sales
--     FROM orders_table orders
--     JOIN dim_date_times dates ON orders.date_uuid = dates.date_uuid
-- ),
-- AVG_TIME_BETWEEN_SALES AS (
--     SELECT CAST(year AS int),
--         AVG(time_between_sales) AS avg_time_between_sales
--     FROM TIME_BETWEEN_SALES
--     GROUP BY year
-- )

-- SELECT year,
--     avg_time_between_sales
-- FROM AVG_TIME_BETWEEN_SALES
-- ORDER BY EXTRACT(
--         hours
--         FROM avg_time_between_sales
--     ),
--     EXTRACT(
--         minutes
--         FROM avg_time_between_sales
--     ),
--     EXTRACT(
--         seconds
--         FROM avg_time_between_sales
--     ),
--     EXTRACT(
--         milliseconds
--         FROM avg_time_between_sales
--     ) % 1000


	
