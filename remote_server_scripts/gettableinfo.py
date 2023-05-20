import sys
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('/opt/planner/calendar')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Get the table name from the command-line argument
if len(sys.argv) > 1:
    table_name = sys.argv[1]
else:
    print("Please provide the table name as a command-line argument.")
    sys.exit(1)

# Execute the PRAGMA statement to get table information
cursor.execute('PRAGMA table_info({})'.format(table_name))

# Fetch all rows from the cursor
rows = cursor.fetchall()

# Print the details of the table
for row in rows:
    print(row)

# Close the cursor and database connection
cursor.close()
conn.close()
