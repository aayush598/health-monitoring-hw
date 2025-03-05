from flask import Flask, request, jsonify, render_template
import sqlite3
import datetime

app = Flask(__name__)

# Initialize SQLite Database
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

init_db()

# Function to check thresholds
def check_thresholds(heart_rate, spo2, temperature):
    alerts = []
    if heart_rate < 50 or heart_rate > 120:
        alerts.append(f'Abnormal heart rate detected: {heart_rate} BPM')
    if spo2 < 90:
        alerts.append(f'Low SpO₂ level detected: {spo2}%')
    if temperature < 35.0 or temperature > 38.0:
        alerts.append(f'Abnormal body temperature detected: {temperature}°C')
    return alerts

# API Endpoint to Receive Sensor Data
@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.json
    heart_rate = data.get('heart_rate')
    spo2 = data.get('spo2')
    temperature = data.get('temperature')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    alerts = check_thresholds(heart_rate, spo2, temperature)

    conn = sqlite3.connect('health_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO health_data (heart_rate, spo2, temperature, timestamp) VALUES (?, ?, ?, ?)",
                   (heart_rate, spo2, temperature, timestamp))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Data saved successfully', 'alerts': alerts}), 201

# API Endpoint to Fetch Latest Data
@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('health_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM health_data ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()
    conn.close()
    
    data_list = [{'id': row[0], 'heart_rate': row[1], 'spo2': row[2], 'temperature': row[3], 'timestamp': row[4]} for row in data]
    return jsonify(data_list)

# Dashboard for Real-time Monitoring
@app.route('/')
def dashboard():
    conn = sqlite3.connect('health_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM health_data ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', data=data)

# API Endpoint to Fetch Latest Data for Real-Time Monitoring
@app.route('/latest', methods=['GET'])
def get_latest_data():
    conn = sqlite3.connect('health_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM health_data ORDER BY timestamp DESC LIMIT 1")
    data = cursor.fetchone()
    conn.close()
    
    if data:
        latest_data = {'id': data[0], 'heart_rate': data[1], 'spo2': data[2], 'temperature': data[3], 'timestamp': data[4]}
        latest_data['alerts'] = check_thresholds(data[1], data[2], data[3])
        return jsonify(latest_data)
    else:
        return jsonify({'message': 'No data available'}), 404
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
