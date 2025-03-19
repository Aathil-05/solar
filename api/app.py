from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# File to store data
excel_file = '../data/energy_data.xlsx'

# Log data to Excel
def log_to_excel(data):
    df = pd.DataFrame(data, index=[0])
    df.to_excel(excel_file, index=False, mode='a', header=False)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    log_data = {
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Temperature (°C)': data['temperature'],
        'Humidity (%)': data['humidity'],
        'Voltage (V)': data['voltage'],
        'Energy Produced (Wh)': data['energyProduced'],
        'Relay State': 'ON' if data['relayState'] == 1 else 'OFF'
    }
    log_to_excel(log_data)
    return jsonify({"status": "success"})

@app.route('/data', methods=['GET'])
def fetch_data():
    try:
        df = pd.read_excel(excel_file)
        data = df.tail(10).to_dict(orient='records')
        return jsonify(data)
    except:
        return jsonify({"error": "No data found"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
