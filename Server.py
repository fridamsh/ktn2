import SocketServer
import json
import time
import datetime
import re

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def printPretty(self, message, username, timestamp):
        return timestamp + " " + username + ' | ' + message

    def login(self, json_object):
        username = json_object.get('username')
        username.lower()
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M')
        if not re.match('[A-Za-z0-9_]{2,}', username):
            #return_data = {'timestamp':timestamp(), 'sender':username, 'response':'error', 'content':'invalid username :('}
            return_data = {'timestamp': timestamp, 'response': 'login', 'error': 'Invalid username!', 'username': username}
            self.connection.sendall(json.dumps(return_data))
        elif username.lower() in self.server.clients.values():
            return_data = {'timestamp': timestamp, 'response': 'login', 'error': 'Name already taken!', 'username': username}
            self.connection.sendall(json.dumps(return_data))
        else:
            self.server.clients[self.connection] = username
            return_data = {'timestamp':timestamp, 'response': 'login', 'username': username, 'messages': self.server.messages}
            self.connection.sendall(json.dumps(return_data))

    def logout(self):
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M')
        if not self.connection in self.server.clients:
            return_data = {'response': 'logout', 'error': 'Not logged in!'}
            self.connection.sendall(json.dumps(return_data))
        else:
            username = self.server.clients[self.connection]
            return_data = {'response': 'logout', 'username': username}
            self.connection.sendall(json.dumps(return_data))
            del self.server.clients[self.connection]

    def send_message(self, json_object):
        if not self.connection in self.server.clients:
            return_data = {'response': 'message', 'error': 'Not logged in!'}
            self.connection.sendall(json.dumps(return_data))
        else:
            username = self.server.clients[self.connection]
            json_message = json_object.get('message')
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M')
            message = self.printPretty(json_message, username, st)
            self.server.messages.append(message)
            return_data = {'response': 'message', 'message': message}
            self.server.broadcast(json.dumps(return_data))

    def getNames(self):
        #username = self.server.clients[self.connection]
        names = self.server.clients.values()
        return_data = {'timestamp':'x', 'username':'username', 'response':'names', 'content':names}
        self.connection.sendall(json.dumps(return_data))

    def getHelp(self):
        info = '\nType *login <username> to log in. \n Type *logout to log out. \n Type *names to get a list of active clients. \n Type *exit to close the AwzmChat<3. \n To chat; just chat.'
        return_data = {'timestamp':'x', 'username':'username', 'response':'help', 'content':info}
        self.connection.sendall(json.dumps(return_data))

    def handle(self):
        self.connection = self.request
        self.ip = self.client_address[0]
        self.port = self.client_address[1]

        print 'Client connected @' + self.ip + ':' + str(self.port)
        # Wait for data from the client
        # Check if the data exists
        # (recv could have returned due to a disconnect)

        while True:
            data = self.connection.recv(1024).strip()
            if data:
                json_object = json.loads(data)
                request = json_object.get('request')
                if request == 'login':
                    self.login(json_object)
                elif request == 'logout':
                    self.logout()
                elif request == 'names':
                    self.getNames()
                elif request == 'help':
                    self.getHelp()
                elif request == 'message':
                    self.send_message(json_object)
            else:
                break

        print 'Client disconnected @' + self.ip + ':' + str(self.port)
    
    def finish(self):
        if self.connection in self.server.clients:
            del self.server.clients[self.connection]



class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    messages = []
    clients = {}

    def broadcast(self, message):
        for client in self.clients:
            client.sendall('   '+message)


if __name__ == "__main__":

    #HOST = '78.91.48.164'

    HOST, PORT = '78.91.68.195', 9999

    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
