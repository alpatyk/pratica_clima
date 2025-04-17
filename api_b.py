from flask import Flask, jsonify

app = Flask(__name__)

weather_data = {
    "sãopaulo": {"city": "São Paulo", "temp": 25, "unit": "Celsius"},
    "riodejaneiro": {"city": "Rio de Janeiro", "temp": 32, "unit": "Celsius"},
    "portoalegre": {"city": "Porto Alegre", "temp": 18, "unit": "Celsius"},
    "curitiba": {"city": "Curitiba", "temp": 12, "unit": "Celsius"},
    "belohorizonte": {"city": "Belo Horizonte", "temp": 28, "unit": "Celsius"}
}

@app.route('/weather/<city>')
def get_weather(city):
    city_key = city.lower().replace(" ", "")
    if city_key in weather_data:
        return jsonify(weather_data[city_key])
    return jsonify({"error": "Cidade não encontrada"}), 404

if __name__ == '__main__':
    app.run(port=5001)