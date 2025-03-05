from notifications import send_notification

def check_thresholds(heart_rate, spo2, temperature):
    alerts = []
    if heart_rate < 50 or heart_rate > 120:
        alert = f'Abnormal heart rate detected: {heart_rate} BPM'
        alerts.append(alert)
        send_notification(alert)
    if spo2 < 90:
        alert = f'Low SpO₂ level detected: {spo2}%'
        alerts.append(alert)
        send_notification(alert)
    if temperature < 35.0 or temperature > 38.0:
        alert = f'Abnormal body temperature detected: {temperature}°C'
        alerts.append(alert)
        send_notification(alert)
    return alerts