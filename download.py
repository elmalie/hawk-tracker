import psycopg2
import csv
from decouple import config


conn = psycopg2.connect(
    dbname=config('DB_USER'),
    user=config('DB_USER'),
    password=config("DB_PASSWORD"),
    host="localhost"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM hawktracker.issue")

with open("hawk_tracker_02.10.23.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
        [desc[0] for desc in cursor.description]
    )  # Write column headers
    csv_writer.writerows(cursor)

cursor.close()
conn.close()
