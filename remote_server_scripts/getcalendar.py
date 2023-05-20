import sys
import sqlite3
import json

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 3:
    print("Usage: python script.py <month> <year>")
    sys.exit(1)

# Extract the command-line arguments
month = int(sys.argv[1])
year = int(sys.argv[2])

# Connect to the database
conn = sqlite3.connect('/opt/planner/calendar')
cursor = conn.cursor()

# Execute the SELECT query
cursor.execute("SELECT * FROM Calendar WHERE month = ? AND year = ?", (month, year))

# Fetch all the matching rows
rows = cursor.fetchall()

# Get the column names
columns = [description[0] for description in cursor.description]

# Prepare the data as a list of dictionaries
data = []
for row in rows:
    data.append(dict(zip(columns, row)))

# Convert the data to JSON
json_data = json.dumps(data, indent=4)

# Print the JSON data
#print(json_data)
print(data)

# Close the database connection
conn.close()

