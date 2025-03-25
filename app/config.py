import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY') or 'your-openweathermap-api-key'