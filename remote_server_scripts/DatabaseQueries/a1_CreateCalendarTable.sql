CREATE TABLE Calendar (
  calendar_id INTEGER PRIMARY KEY,
  day INTEGER,
  month INTEGER,
  year INTEGER,
  first_letter TEXT,
  is_public_holiday INTEGER,
  day_comment TEXT
);