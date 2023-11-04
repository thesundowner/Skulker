# from _modules import *
# import webview.http as w

# class DocView:
#     def __init__(self):
       
        





# DocView()

from http.server import HTTPServer , BaseHTTPRequestHandler


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('127.0.0.1', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()
    BaseHTTPRequestHandler.send_response(200 , "working")
    BaseHTTPRequestHandler.responses = {200}



run()