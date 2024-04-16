import psycopg2
from dotenv import load_dotenv
import json
import os

load_dotenv()

# Connect to our database
conn = psycopg2.connect(user=os.getenv("USERNAME"), password=os.getenv("PASSWORD"), host=os.getenv("HOSTNAME"), port=5432, database="postgres")
cur = conn.cursor()


cur.execute(
    """
    CREATE TABLE IF NOT EXISTS prompts (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        prompt TEXT NOT NULL,
        is_favorite BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
)
conn.commit()


with open('prompt.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

cursor = conn.cursor()
insert_sql = """
INSERT INTO prompts (title, prompt, is_favorite)
VALUES (%s, %s, %s)
"""

try:
    for prompt in data:
        cursor.execute(insert_sql, (prompt['act'], prompt['prompt'], False))
    conn.commit()
    print("Prompts inserted successfully.")
except Exception as e:
    print("Error during inserting the data:", e)
    conn.rollback()
finally:
    cursor.close()
    conn.close()

print("SUCCESS: Inserted prompts into database.")