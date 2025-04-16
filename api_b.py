from flask import Flask, jsonify

app_b = Flask(__name__)

# Dados de clima fictícios para algumas cidades
weather_data = {
    "sãopaulo": {"city": "São_Paulo", "temp": 25, "unit": "Celsius"},
    "riodejaneiro": {"city": "Rio_de_Janeiro", "temp": 32, "unit": "Celsius"},
    "portoalegre": {"city": "Porto_Alegre", "temp": 18, "unit": "Celsius"},
    "curitiba": {"city": "Curitiba", "temp": 12, "unit": "Celsius"},
    "belohorizonte": {"city": "Belo_Horizonte", "temp": 28, "unit": "Celsius"}
}

@app_b.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    city_key = city.lower().replace(" ", "")
    if city_key in weather_data:
        return jsonify(weather_data[city_key])
    else:
        return jsonify({"error": "Cidade não encontrada"}), 404

if __name__ == '__main__':
    app_b.run(port=5001)