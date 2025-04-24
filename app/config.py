#use environment variables to securly handle the API key and include fallback defaults. 

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Not allowed'
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY') or '0f595912d5a8bd80b773dcb4d3828a8b'