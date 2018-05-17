
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    record_manager = RecordManager()

    def send_reply(self, reply_msg):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(reply_msg)
        self.wfile.write("\n")

    def do_PUT(self):
        self.send_reply("PUT")

    def do_POST(self):
        self.send_reply("POST")

    def do_GET(self):
        self.send_reply("PUT")

    def do_DELETE(self):
        self.send_reply("DEL")
        
def main():
    port = 80
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()

        
if __name__ == "__main__":
    main()
