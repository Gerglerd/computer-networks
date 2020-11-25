#https://stackabuse.com/serving-files-with-pythons-simplehttpserver-module/
#python3 -m http.server 8000 --directory

import http.server
import socketserver
import sys

# file_path = sys.argv[1]
# file_path.split('/')
# length = len(file_path)
# for i in range(length - 1):
#     path = '/' + file_path[i]


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = 'mywebhtml.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


handler_object = MyHttpRequestHandler

PORT = 8000

handler = http.server.SimpleHTTPRequestHandler

my_server = socketserver.TCPServer(("", PORT), handler_object)
my_server.serve_forever()
