import re
import subprocess
import time
import unittest

import requests


class WeatherCheckerTests(unittest.TestCase):

    def test_temp_by_coords(self):
        url = 'http://localhost:8000/weather-by-coords'
        params = {'lat': 60.0, 'lon': 30.0}
        response = requests.get(url, params)
        self.assertEqual(response.status_code, 200)
        res = re.fullmatch('Temperature: -?[0-9]+(.[0-9]+)?°C\n', response.text)
        self.assertIsNotNone(res)

    def test_temp_by_city(self):
        url = 'http://localhost:8000/weather-by-city'
        params = {'city': 'Murmansk'}
        response = requests.get(url, params)
        self.assertEqual(response.status_code, 200)
        res = re.fullmatch('Temperature: -?[0-9]+(.[0-9]+)?°C\n', response.text)
        self.assertIsNotNone(res)

    def test_weather_by_coords(self):
        url = 'http://localhost:8000/weather-by-coords'
        params = {'lat': 60, 'lon': 30, 'weather_params': ['pressure', 'temperature']}
        response = requests.get(url, params)
        self.assertEqual(response.status_code, 200)
        res = re.fullmatch('Temperature: -?[0-9]+(.[0-9]+)?°C\nPressure: [0-9]+(.[0-9]+)? mmHg\n', response.text)
        self.assertIsNotNone(res)

    def test_weather_for_five_days(self):
        url = 'http://localhost:8000/week-weather-by-coords'
        params = {'lat': 60, 'lon': 30, 'weather_params': ['humidity', 'temperature']}
        response = requests.get(url, params)
        self.assertEqual(response.status_code, 200)
        res = re.fullmatch('(Date: [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\nTemperature: -?[0-9]+(.['
                           '0-9]+)?°C\nHumidity: [0-9]+%\n\n)+', response.text)
        self.assertIsNotNone(res)

    def test_weather_description(self):
        url = 'http://localhost:8000/description-by-coords'
        params = {'lat': 60, 'lon': 30}
        response = requests.get(url, params)
        self.assertEqual(response.status_code, 200)
        res = re.fullmatch('Weather description:\n.+', response.text)
        self.assertIsNotNone(res)

    def test_invalid_city(self):
        url = 'http://localhost:8000/weather-by-city'
        params = {'city': 'Mur'}
        response = requests.get(url, params)
        self.assertEqual(response.status_code, 400)
        res = re.fullmatch('City not found', response.text)
        self.assertIsNotNone(res)


if __name__ == '__main__':
    unittest.main()
