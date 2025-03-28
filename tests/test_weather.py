import unittest
from unittest.mock import patch, MagicMock
from app.weather import WeatherService

class TestWeatherService(unittest.TestCase):
    def setUp(self):
        self.weather_service = WeatherService(api_key='test_api_key')
    
    @patch('app.weather.requests.get')
    def test_get_weather_success(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'London',
            'sys': {'country': 'GB'},
            'main': {
                'temp': 15.5,
                'feels_like': 14.2,
                'humidity': 76
            },
            'weather': [{'description': 'clear sky', 'icon': '01d'}],
            'wind': {'speed': 3.6}
        }
        mock_get.return_value = mock_response
        
        result = self.weather_service.get_weather('London')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['data']['name'], 'London')
        
    @patch('app.weather.requests.get')
    def test_get_weather_city_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'message': 'city not found'}
        mock_get.return_value = mock_response
        
        result = self.weather_service.get_weather('NonExistentCity')
        
        self.assertFalse(result['success'])
        self.assertIn('city not found', result['message'])
    
    def test_parse_weather_data(self):
        raw_data = {
            'success': True,
            'data': {
                'name': 'Paris',
                'sys': {'country': 'FR'},
                'main': {
                    'temp': 22.4,
                    'feels_like': 21.8,
                    'humidity': 65
                },
                'weather': [{'description': 'few clouds', 'icon': '02d'}],
                'wind': {'speed': 2.1}
            }
        }
        
        result = self.weather_service.parse_weather_data(raw_data)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['city'], 'Paris')
        self.assertEqual(result['country'], 'FR')
        self.assertEqual(result['temp'], 22)
        self.assertEqual(result['description'], 'Few clouds')

if __name__ == '__main__':
    unittest.main()

