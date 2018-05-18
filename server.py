
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class Record:
    def __init__(self, email):
        self.email = email
        self.friends = set()

    def add_Friend(self, email):
        self.friends.add(email)

    def get_Friends(self):
        return self.friends

class RecordManager:
    def __init__(self):
        self.records = {}

    def get_Record(self, email):
        return self.records[email]

    def add_Record(self, email):
        if email not in self.records:
            self.records[email] = Record(email)
        return self.records[email]

    def add_Friends(self, email1, email2):
        r1 = self.add_Record(email1)
        r1.add_Friend(email2)
        r2 = self.add_Record(email2)
        r2.add_Friend(email1)

    def get_Common(self, email1, email2):
        r1 = self.get_Record(email1)
        if r1 is None:
            return set()
        r2 = self.get_Record(email2)
        if r2 is None:
            return set()
        return r1.get_Friends() & r2.get_Friends()
        
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
