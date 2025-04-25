#use environment variables to securly handle the API key and include fallback defaults. 

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Not allowed'
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY') or 'your_actual_api_key_here'
