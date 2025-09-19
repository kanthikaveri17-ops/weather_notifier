from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace with your OpenWeather API key
API_KEY = "a2e7286c2062b7ee6faf1a4f70b094ad"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def get_weather():
    data = request.json
    lat = data.get("lat")
    lon = data.get("lon")
    city = data.get("city")

    # Fetch by coordinates or city name
    if lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    elif city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    else:
        return jsonify({"error": "No location provided"}), 400

    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch weather"}), 500

    data = response.json()
    return jsonify({
        "city": data["name"],
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"]
    })

if __name__ == "__main__":
    app.run(debug=True)
  
