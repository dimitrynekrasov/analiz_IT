from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import urllib.request 


class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_request = urlparse(self.path)
        print('>>> %s ' % parsed_request.query)
        #download
        #message = referat()
        #file_name, headers = urllib.request.urlretrieve(parsed_request.params)
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