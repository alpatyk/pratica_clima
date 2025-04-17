from flask import Flask, jsonify
import requests
import redis
import json

app = Flask(__name__)

# Configuração do Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

API_B_URL = "http://localhost:5001/weather"
CACHE_EXPIRATION = 300  # 5 minutos em segundos

def get_recommendation(temp):
    if temp > 30:
        return "Está Djano de quente! Hidrate-se e use protetor solar."
    elif temp >= 15:
        return "O clima está agradável. Aproveite o dia!"
    else:
        return "Está frio! Recomendo não esquecer a Japona."

@app.route('/recommendation/<city>')
def get_city_recommendation(city):
    # Verifica se existe no cache
    cache_key = f"weather:{city.lower()}"
    cached_data = redis_client.get(cache_key)
    
    if cached_data:
        return jsonify({**json.loads(cached_data), "cached": True})
    
    try:
        response = requests.get(f"{API_B_URL}/{city}")
        weather_info = response.json()
        
        if response.status_code == 200:
            recommendation = get_recommendation(weather_info['temp'])
            result = {
                "city": weather_info['city'],
                "temperature": weather_info['temp'],
                "unit": weather_info['unit'],
                "recommendation": recommendation
            }
            
            # Armazena no Redis
            redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps(result))
            
            return jsonify({**result, "cached": False})
            
        return jsonify({"error": "Cidade não encontrada"}), 404
        
    except requests.exceptions.RequestException:
        return jsonify({"error": "Serviço de clima indisponível"}), 503

if __name__ == '__main__':
    app.run(port=5000)