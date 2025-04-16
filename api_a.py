from flask import Flask, jsonify
import requests

app_a = Flask(__name__)

API_B_URL = "http://localhost:5001/weather"

def get_recommendation(temp):
    if temp > 30:
        return "Está um clima do Djano! Hidrate-se e use protetor solar."
    elif 15 <= temp <= 30:
        return "O clima está agradável. Aproveite o dia!"
    else:
        return "Está frio! Recomendo usar uma Japona."

@app_a.route('/recommendation/<city>', methods=['GET'])
def get_city_recommendation(city):
    try:
        # Chamada à API B
        response = requests.get(f"{API_B_URL}/{city}")
        
        if response.status_code == 200:
            weather_info = response.json()
            recommendation = get_recommendation(weather_info['temp'])
            
            return jsonify({
                "city": weather_info['city'],
                "temperature": weather_info['temp'],
                "unit": weather_info['unit'],
                "recommendation": recommendation
            })
        else:
            return jsonify({"error": "Não foi possível obter dados da cidade"}), 404
            
    except requests.exceptions.RequestException:
        return jsonify({"error": "Serviço de clima indisponível"}), 503

if __name__ == '__main__':
    app_a.run(port=5000)