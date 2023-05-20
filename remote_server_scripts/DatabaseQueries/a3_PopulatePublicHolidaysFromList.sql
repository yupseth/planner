CREATE TEMP TABLE holidays(day INTEGER, month INTEGER, year INTEGER, name TEXT);
INSERT INTO holidays(day, month, year, name)
VALUES
    (1, 1, 2023, 'Anul Nou'),
    (2, 1, 2023, 'Anul Nou'),
    (24, 1, 2023, 'Ziua Unirii Principatelor Romane'),
    (14, 4, 2023, 'Paste ortodox'),
    (17, 4, 2023, 'Paste ortodox'),
    (1, 5, 2023, 'Ziua Muncii'),
    (1, 6, 2023, 'Ziua Copilului'),
    (4, 6, 2023, 'Rusalii'),
    (5 ,6 ,2023 ,'A doua zi de Rusalii'),
    (15 ,8 ,2023 ,'Adormirea Maicii Domnului'),
    (30 ,11 ,2023 ,'Sfantul Andrei'),
    (1 ,12 ,2023 ,'Ziua Nationala a Romaniei'),
    (25 ,12 ,2023 ,'Craciunul'),
    (26 ,12 ,2023 ,'Craciunul');

UPDATE Calendar
SET is_public_holiday = 1,
    day_comment = (SELECT name FROM holidays WHERE Calendar.day = holidays.day AND Calendar.month = holidays.month AND Calendar.year = holidays.year)
WHERE EXISTS (SELECT 1 FROM holidays WHERE Calendar.day = holidays.day AND Calendar.month = holidays.month AND Calendar.year = holidays.year);

DROP TABLE holidays;