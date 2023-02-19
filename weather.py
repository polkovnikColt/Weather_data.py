import requests
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

API_TOKEN=""
WEATHER_API_TOKEN = ""
WEATHER_API_URL = "http://api.weatherapi.com/v1/forecast.json"

@app.route("/api/weather/v1/helloTest", methods=["GET"])
def hello_world():
  return "Hello,World"

@app.route('/api/weather/v1/getWeather', methods=['POST'])
def get_weather_by_params():
    try:
        data = request.json
        if not data or 'token' not in data or data['token'] != API_TOKEN:
            return jsonify({"Unathorized": "invalid token"}), 401

        location = data.get('location')
        date = data.get('date')
        requester_name = data.get("requester_name")

        if not location: 
            return jsonify({"Error": "missing location param"}), 400
        if not date:
            return jsonify({"Error": "missing date param"}), 400

        weather_api_response = requests.get(WEATHER_API_URL, params={'key': WEATHER_API_TOKEN, 'q': location, 'dt': date })

        if weather_api_response.status_code == 200:
            weather_data = weather_api_response.json()
            weather_current = weather_data['current']
            return jsonify({
                "requester_name": data.get('requester_name'),
                "timestamp": datetime.utcnow().isoformat() + 'Z',
                "location": location,
                "date": date,
                "weather": {
                	"temp_c": weather_current['temp_c'],
                	"wind_kph": weather_current['wind_kph'],
                	"pressure_mb": weather_current['pressure_mb'],
                	"humidity": weather_current['humidity']
            	}
            })
        else:
            return jsonify({"error": "unable to get weather data"}), 500
    
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
