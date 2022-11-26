import json
import os
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import parse_qs
from datetime import datetime
import requests


def extract_params(response, weather_params):
    result = dict()
    if ('temperature' in weather_params):
        result['Temperature'] = f"{response['main']['temp']}°C"
    if ('pressure' in weather_params):
        result['Pressure'] = f"{response['main']['pressure']*0.750061575} mmHg"
    if ('humidity' in weather_params):
        result['Humidity'] = f"{response['main']['humidity']}%"
    if ('wind' in weather_params):
        result['Wind'] = (f"{response['wind']['speed']} m/s, {response.json()['wind']['deg']}°")
    return result


def get_description_by_coords(coords):
    try:
        params = {
            "lat": coords[0],
            "lon": coords[1],
            "appid": "a6d4686bc37eb06407d816dd402239fa",
            "units": "metric",
        }
        url = "https://api.openweathermap.org/data/2.5/weather"
        response = requests.get(url, params)
        res_weather = response.json()['weather'][0]

        return f"{res_weather['main']}({res_weather['description']})"
    except KeyError:
        return None


def get_week_weather_by_coords(coords, weather_params):
    try:
        params = {
            "lat": coords[0],
            "lon": coords[1],
            "appid": "a6d4686bc37eb06407d816dd402239fa",
            "units": "metric",
        }
        url = "http://api.openweathermap.org/data/2.5/forecast"
        response = requests.get(url, params)
        timestamps = []
        for timestamp in response.json()['list']:
            timestamps.append({
                'Date': datetime.fromtimestamp(timestamp['dt']),
                **extract_params(timestamp, weather_params)
            })
        return timestamps
    except KeyError:
        return None


def get_weather_by_coords(coords, weather_params):
    try:
        params = {
            "lat": coords[0],
            "lon": coords[1],
            "appid": "a6d4686bc37eb06407d816dd402239fa",
            "units": "metric",
        }
        url = "https://api.openweathermap.org/data/2.5/weather"
        response = requests.get(url, params)
        return extract_params(response.json(), weather_params)
    except KeyError:
        return None


def get_weather_by_city(city_name, weather_params):
    with open(os.path.join(os.path.dirname(__file__), 'city.list.json'), encoding='utf-8') as file:
        cities = json.load(file)
        for city in cities:
            if city['name'] == city_name:
                params = {
                    "id": city['id'],
                    "appid": "a6d4686bc37eb06407d816dd402239fa",
                    "units": "metric"
                }
                url = "https://api.openweathermap.org/data/2.5/weather"
                response = requests.get(url, params)
                return extract_params(response.json(), weather_params)
        return None


class HttpGetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        query_components = parse_qs(self.path)
        route = self.path
        if query_components:
            old_key = list(query_components.keys())[0]
            route, new_key = old_key.split('?')
            query_components[new_key] = query_components.pop(old_key)

        if route == '/weather-by-coords':

            if 'lat' not in query_components or 'lon' not in query_components:
                self.send_response(400)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write("Location not provided".encode())
            else:
                weather = get_weather_by_coords(
                    [query_components["lat"], query_components["lon"]],
                    query_components['weather_params'] if 'weather_params' in query_components else ['temperature'],
                )
                if weather:
                    self.send_response(200)
                    self.send_header("Content-type", "text/plain; charset=utf-8")
                    self.end_headers()
                    for key, value in weather.items():
                        self.wfile.write(f"{key}: {value}\n".encode())
                else:
                    self.send_response(400)
                    self.send_header("Content-type", "text/plain; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("Invalid parameters".encode())

        elif route == '/weather-by-city':
            if 'city' not in query_components:
                self.send_response(400)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write("City not provided".encode())
            else:
                weather = get_weather_by_city(
                    query_components["city"][0],
                    query_components['weather_params'] if 'weather_params' in query_components else ['temperature'],
                )
                if weather:
                    self.send_response(200)
                    self.send_header("Content-type", "text/plain; charset=utf-8")
                    self.end_headers()
                    for key, value in weather.items():
                        self.wfile.write(f"{key}: {value}\n".encode())
                else:
                    self.send_response(400)
                    self.send_header("Content-type", "text/plain; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("City not found".encode())

        elif route == '/week-weather-by-coords':
            if 'lat' not in query_components or 'lon' not in query_components:
                self.send_response(400)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write("Location not provided".encode())
            else:
                weather = get_week_weather_by_coords(
                    [query_components["lat"], query_components["lon"]],
                    query_components['weather_params'] if 'weather_params' in query_components else ['temperature'],
                )
                if weather:
                    self.send_response(200)
                    self.send_header("Content-type", "text/plain; charset=utf-8")
                    self.end_headers()
                    for weather_timestamp in weather:
                        for key, value in weather_timestamp.items():
                            self.wfile.write(f"{key}: {value}\n".encode())
                        self.wfile.write('\n'.encode())
                else:
                    self.send_response(400)
                    self.send_header("Content-type", "text/plain; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("Invalid parameters".encode())

        elif route == '/description-by-coords':
            if 'lat' not in query_components or 'lon' not in query_components:
                self.send_response(400)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write("Location not provided".encode())

            weather = get_description_by_coords([query_components["lat"], query_components["lon"]])
            if weather:
                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(f'Weather description:\n{weather}'.encode())
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write("Invalid parameters".encode())

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(f'Page not found'.encode())


def run(server_class=HTTPServer, handler_class=HttpGetHandler):
    port = 8000
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
        print(f"Server started at port: {port}")
    except KeyboardInterrupt:
        httpd.server_close()


run()
