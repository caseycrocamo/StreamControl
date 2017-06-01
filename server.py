import os
import sys
import http.server
import socketserver
streamcontrol = open('streamcontrol.xml','rb')
port = 8000
os.chdir('D:\Dropbox\IVSmash\StreamControl')
class myRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/xml")
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        try:
            f = open('streamcontrol.xml', "rb")
            self.wfile.write(f.read())
            f.close()
        except IOError:
            print("file not found")
myServer = socketserver.TCPServer(('', port), myRequestHandler)
try:
    print('server opened on port: ',port)
    myServer.serve_forever()
except KeyboardInterrupt:
    print('Server Closed')
    myServer.socket.close()
