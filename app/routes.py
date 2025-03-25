from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from app.weather import Weather
from datetime import datetime

main_blueprint = Blueprint('main', __name__)
weather = Weather

@main_blueprint.route('/health', methods=['GET'])
def health_ck():
    return jsonify({"status": "healthy"}), 200

@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if request.method == 'POST':
        city = request.form.get('city')
        if not city:
            flash('Please enter a city name')
            return redirect(url_for('main.index'))
        
        raw_data = weather.get_weather(city)
        wdata = weather.parse_weather_data(raw_data)
        
        if not wdata.get('success'):
            flash(wdata.get('message', 'Failed to retrieve weather data'))
    
    return render_template('index.html', 
                            weather=wdata, 
                            current_time=current_time)

@main_blueprint.route('/api/weather', methods=['GET'])
def get_weather_api(city):
    raw_data = weather.get_weather(city)
    wdata = weather.parse_data(raw_data)

    if wdata.get('success'):
        return jsonify(wdata), 200
    else:
        return jsonify(wdata), 404