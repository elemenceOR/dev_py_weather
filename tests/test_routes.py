import json
import unittest
from unittest.mock import patch, MagicMock
from app import create_app
from app.config import Config

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        self.app_context.pop()
    
    def test_health_check(self):
        response = self.client.get('/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
    
    @patch('app.routes.weather_service.get_weather')
    def test_api_weather_success(self, mock_get_weather):
        mock_get_weather.return_value = {
            'success': True,
            'data': {
                'name': 'Berlin',
                'sys': {'country': 'DE'},
                'main': {'temp': 18.5, 'feels_like': 17.9, 'humidity': 70},
                'weather': [{'description': 'broken clouds', 'icon': '04d'}],
                'wind': {'speed': 4.1}
            }
        }
        
        response = self.client.get('/api/weather/Berlin')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['city'], 'Berlin')
    
    @patch('app.routes.weather_service.get_weather')
    def test_api_weather_city_not_found(self, mock_get_weather):
        mock_get_weather.return_value = {
            'success': False,
            'message': 'Error: 404 - city not found'
        }
        
        response = self.client.get('/api/weather/NonExistentCity')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

if __name__ == '__main__':
    unittest.main()

