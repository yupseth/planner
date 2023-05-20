INSERT INTO Calendar (calendar_id, day, month, year, first_letter)
SELECT NULL, day, month, year,
       CASE strftime('%w', year || '-' || month || '-' || day)
           WHEN '0' THEN 'S'
           WHEN '1' THEN 'M'
           WHEN '2' THEN 'T'
           WHEN '3' THEN 'W'
           WHEN '4' THEN 'T'
           WHEN '5' THEN 'F'
           WHEN '6' THEN 'S'
       END AS first_letter
FROM (
    SELECT strftime('%d', date) AS day,
           strftime('%m', date) AS month,
           strftime('%Y', date) AS year
    FROM (
        SELECT date('2023-01-01', '+' || (t4.i*1000 + t3.i*100 + t2.i*10 + t1.i) || ' day') AS date
        FROM (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) AS t1,
             (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) AS t2,
             (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) AS t3,
             (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) AS t4
        WHERE (t4.i*1000 + t3.i*100 + t2.i*10 + t1.i) <= 364
        ORDER BY date
    )
);