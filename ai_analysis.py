import json
import requests
from database import fetch_latest_data
import os 
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def get_health_insights():
    data = fetch_latest_data(limit=10)
    health_summary = f"Recent health data: {json.dumps(data)}"
    
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": f"Analyze the following health data and provide insights: {health_summary}"}]}]}
    
    response = requests.post(gemini_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Failed to fetch AI insights'}