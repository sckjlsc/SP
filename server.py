#!/usr/bin/env python

import urlparse, json
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

"""
1) Add friend pair
curl -X PUT http://localhost -d "{\"friends\":[\"andy@example.com\",\"john@example.com\"]}"
2) Get friend list
curl -X GET http://localhost -d "{\"email\":\"john@example.com\"}"

"""
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
        self.wfile.write(json.dumps(reply_msg, ensure_ascii=False))
        self.wfile.write("\n")

    def do_PUT(self):
        reply = {}
        reply["success"] = False
        content_length = self.headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0
        if length==0:
            return send_reply(reply)

        content = self.rfile.read(length)
        request = json.loads(content)
        
        if "friends" not in request:
            return send_reply(reply)

        friend_pair = request["friends"]
        if len(friend_pair)!=2:
            return send_reply(reply)

        self.record_manager.add_Friends(friend_pair[0], friend_pair[1])
        reply["success"] = True
        self.send_reply(reply)

    def do_POST(self):
        self.send_reply("POST")

    def do_GET(self):
        reply = {}
        reply["success"] = False
        parsed_path = urlparse.urlparse(self.path)
        content = parsed_path.query
        if len(content)==0:
            content_length = self.headers.getheaders('content-length')
            length = int(content_length[0]) if content_length else 0
            content = self.rfile.read(length)
        if len(content)==0:
            return self.send_reply(reply)

        request = json.loads(content)
        if "email" in request:        
            r = self.record_manager.get_Record(request["email"])
            if r is None:
                return self.send_reply(reply)
            reply["success"] = True
            f = r.get_Friends()
            reply["friends"] = list(f)
            reply["count"] = len(f)
        self.send_reply(reply)

    def do_DELETE(self):
        self.send_reply("DEL")
        
def main():
    port = 80
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()

        
if __name__ == "__main__":
    main()
