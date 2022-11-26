import json
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import parse_qs
import requests


def get_temp_by_coords(coords):
    params = {
        "lat": coords[0],
        "lon": coords[1],
        "appid": "a6d4686bc37eb06407d816dd402239fa",
        "units": "metric"
    }
    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url, params)
    return response.json()['main']['temp']


def get_temp_by_city(city_name):
    with open('city.list.json', encoding='utf-8') as file:
        cities = json.load(file)
        for city in cities:
            if city['name'] == city_name:
                params = {
                    "id": city['id'],
                    "appid": "a6d4686bc37eb06407d816dd402239fa",
                    "units": "metric"
                }
                url = f"https://api.openweathermap.org/data/2.5/weather"
                response = requests.get(url, params)
                return response.json()['main']['temp']
        return None


class HttpGetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        query_components = parse_qs(self.path)
        route = self.path
        if query_components:
            old_key = list(query_components.keys())[0]
            route, new_key = old_key.split('?')
            query_components[new_key] = query_components.pop(old_key)
        if route == '/temp-by-coords':
            temp = get_temp_by_coords([query_components["lat"], query_components["lon"]])
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"{temp} °C".encode())
        if route == '/temp-by-city':
            temp = get_temp_by_city(query_components["city"][0])
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            if temp:
                self.wfile.write(f"{temp} °C".encode())
            else:
                self.wfile.write("City not found".encode())


def run(server_class=HTTPServer, handler_class=HttpGetHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


run()
