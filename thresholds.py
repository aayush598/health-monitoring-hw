def check_thresholds(heart_rate, spo2, temperature):
    alerts = []
    if heart_rate < 50 or heart_rate > 120:
        alerts.append(f'Abnormal heart rate detected: {heart_rate} BPM')
    if spo2 < 90:
        alerts.append(f'Low SpO₂ level detected: {spo2}%')
    if temperature < 35.0 or temperature > 38.0:
        alerts.append(f'Abnormal body temperature detected: {temperature}°C')
    return alerts