import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

connection = psycopg.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT
            'threat_intel' AS table_name,
            COUNT(*) AS records
        FROM threat_intel

        UNION ALL

        SELECT
            'siem_alerts',
            COUNT(*)
        FROM siem_alerts

        UNION ALL

        SELECT
            'edr_events',
            COUNT(*)
        FROM edr_events;
    """)

    results = cursor.fetchall()

for table_name, records in results:
    print(f"{table_name}: {records} records")

connection.close()