import sqlite3

def init_db():
    conn = sqlite3.connect('health_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS health_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        heart_rate REAL,
                        spo2 REAL,
                        temperature REAL,
                        timestamp TEXT)''')
    conn.commit()
    conn.close()

def insert_data(heart_rate, spo2, temperature, timestamp):
    conn = sqlite3.connect('health_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO health_data (heart_rate, spo2, temperature, timestamp) VALUES (?, ?, ?, ?)",
                   (heart_rate, spo2, temperature, timestamp))
    conn.commit()
    conn.close()

def fetch_latest_data(limit=1):
    conn = sqlite3.connect('health_data.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM health_data ORDER BY timestamp DESC LIMIT {limit}")
    data = cursor.fetchall()
    conn.close()
    return data