from flask import request, jsonify, render_template
from database import insert_data, fetch_latest_data
from thresholds import check_thresholds
from ai_analysis import get_health_insights
import datetime

def init_routes(app):
    @app.route('/upload', methods=['POST'])
    def upload_data():
        data = request.json
        heart_rate = data.get('heart_rate')
        spo2 = data.get('spo2')
        temperature = data.get('temperature')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alerts = check_thresholds(heart_rate, spo2, temperature)
        insert_data(heart_rate, spo2, temperature, timestamp)
        return jsonify({'message': 'Data saved successfully', 'alerts': alerts}), 201

    @app.route('/latest', methods=['GET'])
    def get_latest_data():
        data = fetch_latest_data()
        if data:
            latest_data = {'id': data[0][0], 'heart_rate': data[0][1], 'spo2': data[0][2], 'temperature': data[0][3], 'timestamp': data[0][4]}
            latest_data['alerts'] = check_thresholds(data[0][1], data[0][2], data[0][3])
            return jsonify(latest_data)
        else:
            return jsonify({'message': 'No data available'}), 404

    @app.route('/graph_data', methods=['GET'])
    def graph_data():
        data = fetch_latest_data(limit=20)
        graph_data = {'timestamps': [row[4] for row in data],
                      'heart_rate': [row[1] for row in data],
                      'spo2': [row[2] for row in data],
                      'temperature': [row[3] for row in data]}
        return jsonify(graph_data)

    @app.route('/health_insights', methods=['GET'])
    def health_insights():
        insights = get_health_insights()
        return jsonify({'insights': insights})

    @app.route('/')
    def dashboard():
        return render_template('dashboard.html')