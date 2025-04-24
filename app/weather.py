import requests
from flask import current_app

class Weather:
    def __init__(self, api_key='None'):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        # fetch waether from the specified {city}
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric' #force to use celcius
            }

            print(f"Using API key: {self.api_key}")

            response = requests.get(self.base_url, params=params)

            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'message': f"Error: {response.status_code} - {response.json().get('message', 'Unknow error')}"

                }
        
        except Exception as e:
            return {
                'success': False,
                'message': f"Exeption occured: {str(e)}"
            }
        
    def parse_data(self, wdata):
        #transfrom raw data recived from the API into readable format
        if not wdata.get('success', False):
            return wdata
        
        data = wdata['data']

        return {
            'success': True,
            'city': data['name'],
            'country': data['sys']['country'],
            'temp': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'].capitalize(),
            'icon': data['weather'][0]['icon'],
            'wind_speed': data['wind']['speed']
        }