#!/usr/bin/env python

import urlparse, json, re, argparse
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

"""
1) Add friend pair
curl -X PUT http://localhost:80 -d "{\"friends\":[\"andy@example.com\",\"john@example.com\"]}"
curl -X PUT http://localhost:80 -d "{\"friends\":[\"common@example.com\",\"john@example.com\"]}"
curl -X PUT http://localhost:80 -d "{\"friends\":[\"andy@example.com\",\"common@example.com\"]}"
2) Get friend list
curl -X GET http://localhost:80 -d "{\"email\":\"john@example.com\"}"
3) Retrieve the common friends
curl -X GET http://localhost:80 -d "{\"friends\":[\"andy@example.com\",\"john@example.com\"]}"
4) Subscribe
curl -X POST http://localhost:80 -d "{\"requestor\":\"lisa@example.com\", \"target\":\"john@example.com\"}"
5) Block
curl -X DELETE http://localhost:80 -d "{\"requestor\":\"lisa@example.com\", \"target\":\"john@example.com\"}"
6) Get list of emails can receive update
curl -X GET http://localhost:80 -d "{\"sender\":\"john@example.com\", \"text\":\"Hello World! kate@example.com\"}"
"""

class Record:
    def __init__(self, email):
        self.email = email
        self.friends = set()
        self.subscribers = set()
        self.blocks = set()

    def add_Friend(self, email):
        if email not in self.blocks:
            self.friends.add(email)

    def get_Friends(self):
        return self.friends

    def add_Subscriber(self, email):
        self.subscribers.add(email)

    def add_Block(self, email):
        self.blocks.add(email)

    def get_Blocks(self):
        return self.blocks

    def get_Subscribers(self):
        return self.subscribers

class RecordManager:
    def __init__(self):
        self.records = {}

    def get_Record(self, email):
        return self.records[email]

    def get_or_add(self, email):
        if email not in self.records:
            self.records[email] = Record(email)
        return self.records[email]

    def add_Friends(self, email1, email2):
        r1 = self.get_or_add(email1)
        r1.add_Friend(email2)
        r2 = self.get_or_add(email2)
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
        reply = {}
        reply["success"] = False
        content_length = self.headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0
        if length==0:
            return send_reply(reply)
        content = self.rfile.read(length)
        request = json.loads(content)

        if "requestor" not in request:
            return send_reply(reply)
        if "target" not in request:
            return send_reply(reply)
        # r = self.record_manager.add_Record(request["requestor"])
        t = self.record_manager.get_or_add(request["target"])
        t.add_Subscriber(request["requestor"])
        reply["success"] = True
        self.send_reply(reply)

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
            return self.send_reply(reply)

        if "friends" in request:
            friend_pair = request["friends"]
            if len(friend_pair)!=2:
                return self.send_reply(reply)

            reply["success"] = True
            com = self.record_manager.get_Common(friend_pair[0], friend_pair[1])
            reply["friends"] = list(com)
            reply["count"] = len(com)
            return self.send_reply(reply)

        if "sender" not in request:
            return self.send_reply(reply)
        if "text" not in request:
            return self.send_reply(reply)

        sender = self.record_manager.get_Record(request["sender"])
        if sender is None:
            return self.send_reply(reply)
 
        regex = re.compile(r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.com')
        mentioned = filter(regex.match, request["text"].split())
        listener = (set(mentioned) | sender.get_Subscribers() | sender.get_Friends()) - sender.get_Blocks()
        reply["success"] = True
        reply["recipients"] = list(listener)
        return self.send_reply(reply)

    def do_DELETE(self):
        reply = {}
        reply["success"] = False
        content_length = self.headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0
        if length==0:
            return send_reply(reply)
        content = self.rfile.read(length)
        request = json.loads(content)

        if "requestor" not in request:
            return send_reply(reply)
        if "target" not in request:
            return send_reply(reply)
        # r = self.record_manager.add_Record(request["requestor"])
        t = self.record_manager.get_or_add(request["target"])
        t.add_Block(request["requestor"])
        reply["success"] = True
        self.send_reply(reply)
        
def main(port):
    print('Listening on localhost:%s' % port)
    server = HTTPServer(('', port), RequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int, nargs='?',default=80)
    main(parser.parse_args().port)
