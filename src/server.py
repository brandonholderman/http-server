from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from cowpy import cow
import json
import sys

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Creates a request handler for http requests and sends response
    """
    def do_GET(self):
        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)

        if parsed_path.path == '/':
            self.send_response(200)
            self.end_headers()

            self.wfile.write(b'''
<!DOCTYPE html>
<html>
<head>
    <title> cowsay </title>
</head>
<body>
    <header>
        <nav>
        <ul>
            <li><a href="/cowsay">cowsay</a></li>
        </ul>
        </nav>
    <header>
    <main>
        <!-- project description -->
    </main>
</body>
</html>''')

        elif parsed_path.path == '/cowsay':
            self.send_response(200)
            self.end_headers()

            self.wfile.write(cow.Cheese().milk('Use /cow msg="text" to see your message').encode('utf8'))
            return

        elif parsed_path.path == '/cow':
            try:
                msg = parsed_qs['msg'][0]
                print(msg)
            except (KeyError, json.decoder.JSONDecodeError) as err:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'You did a bad thing')
                print(parsed_qs, err)
                return

            self.send_response(200)
            self.end_headers()
            self.wfile.write(cow.Cheese().milk(msg).encode('utf8'))
            return

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        """
        Allows the user to add their own query string to the url
        """
        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)

        if parsed_path.path == '/cow':
            try:
             msg = parsed_qs['msg'][0]
            except (KeyError, json.decoder.JSONDecodeError) as err:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'You did a bad thing')
                print(parsed_qs, err)
                return

            self.send_response(200)
            self.end_headers()
            content = {
                'content': cow.Cheese().milk(msg)
            }
            self.wfile.write(json.dumps(content).encode('utf8'))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Not Found')


def create_server():
    """
    Creates our server assigning the local host and port and type of server being used
    """
    return HTTPServer(('127.0.0.1', 3000), SimpleHTTPRequestHandler)


def run_forever():
    """
    Runs the server until told to shut down
    """
    server = create_server()

    try:
        print('Starting server on port 3000')
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    run_forever()
