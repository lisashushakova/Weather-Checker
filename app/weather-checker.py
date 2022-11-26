from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import parse_qs


class HttpGetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        query_components = parse_qs(self.path)
        route = self.path
        if query_components:
            old_key = list(query_components.keys())[0]
            route, new_key = old_key.split('?')
            query_components[new_key] = query_components.pop(old_key)

        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"TEST RESPONSE. QUERY: {query_components}".encode())


def run(server_class=HTTPServer, handler_class=HttpGetHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


run()
