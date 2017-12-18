from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import urllib.request 


class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_request = urlparse(self.path)
        parsed_url = parsed_request.query
        print('>>> %s ' % parsed_url)
        with urllib.request.urlopen(parsed_url) as response:
            data = response.read() # a `bytes` object
        #print('>>>>>>>>>>>>>>> %s ' % data)
        #message = referat()
        message = 'Hello world'
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8081), GetHandler)
    print('Starting server, use <Ctrl-C> to stop')
    try:
      server.serve_forever()
    except KeyboardInterrupt:
      print("\n\nfinished")