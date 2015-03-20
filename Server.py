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
        username = json_object.get('content')
        username.lower()
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M')
        if not re.match('[A-Za-z0-9_]{2,}', username):
            #return_data = {'timestamp':timestamp(), 'sender':username, 'response':'error', 'content':'invalid username :('}
            return_data = {'timestamp': timestamp, 'sender': username, 'response': 'error', 'content': 'Invalid username!'}
            self.connection.sendall(json.dumps(return_data))
        elif username.lower() in self.server.clients.values():
            return_data = {'timestamp': timestamp, 'sender': username, 'response': 'error', 'content': 'Name already taken!'}
            self.connection.sendall(json.dumps(return_data))
        else:
            #if self.server.messages != None:
            self.server.clients[self.connection] = username
            return_data = {'timestamp':timestamp, 'sender':username, 'response': 'history', 'content': self.server.messages}
            self.connection.sendall(json.dumps(return_data))
            


    def logout(self):
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M')
        if not self.connection in self.server.clients:
            return_data = {'timestamp': timestamp, 'sender': '','response': 'error', 'content': 'Not logged in!'}
            self.connection.sendall(json.dumps(return_data))
        else:
            username = self.server.clients[self.connection]
            return_data = {'timestamp': timestamp, 'sender': username, 'response': 'info', 'content': 'Logged out! Byebye '+username+"<3"}
            self.connection.sendall(json.dumps(return_data))
            del self.server.clients[self.connection]

    def send_message(self, json_object):
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M')
        if not self.connection in self.server.clients:
            return_data = {'timestamp': timestamp, 'sender': '','response': 'error', 'content': 'Not logged in!'}
            self.connection.sendall(json.dumps(return_data))
        else:
            username = self.server.clients[self.connection]
            json_message = json_object.get('content')
            if json_message=='':
                return_data = {'timestamp': timestamp, 'sender':'','response': 'error', 'content': 'Cannot send empty message'}
                self.connection.sendall(json.dumps(return_data))
            else:
                message = self.printPretty(json_message, username, timestamp)
                self.server.messages.append(message)
                return_data = {'timestamp': timestamp, 'sender':username,'response': 'message', 'content': message}
                self.server.broadcast(json.dumps(return_data))

    def welcome(self):
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M')
        welcomeInfo ="\n---------------------------------------------------------------------\n \
     __                                              __      __\n \
    /  \                                            /   \  /   \ \n \
   / /\ \                  ______                  |     \/     |\n \
  / /__\ \      _      _   \__  /     __  __        \          / \n \
 / _____  \    \ \ _ / /    / /__    /  \/  \         \      /\n \
/_/      \_\    \_/ \_/    /____/   /_/\__/\_\          \  /\n \
---------------------------------------------------------\/-----------\n\n\
Welcome to AwzmChat<3 write something awezome - aand be awezome.\n\
Type -> *help <- to see what you can do in AwzmChat<3"
        return_data = {'timestamp': timestamp, 'sender': '','response': 'info', 'content': welcomeInfo}
        self.connection.sendall(json.dumps(return_data))

    def getNames(self):
        #username = self.server.clients[self.connection]
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M')
        names = self.server.clients.values()

        print names[0]
        listNames = ""
        for name in names:
            listNames += "\n<3 "+name
        return_data = {'timestamp':timestamp, 'sender':'username', 'response':'info', 'content':"These are logged in:"+listNames}
        self.connection.sendall(json.dumps(return_data))

    def getHelp(self):
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M')
        info = '\nType *login <username> to log in. \nType *logout to log out. \nType *names to get a list of active clients. \nType *exit to close the AwzmChat<3 \nTo chat; just chat.'
        return_data = {'timestamp':timestamp, 'sender':'username', 'response':'info', 'content':info}
        self.connection.sendall(json.dumps(return_data))

    def handle(self):
        self.connection = self.request
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.welcome()
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
                elif request == 'msg':
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

            if not message.startswith("Cannot send empty message"):
                client.sendall(message)
        

if __name__ == "__main__":

    #HOST = '78.91.48.164'

    HOST, PORT = '78.91.69.239', 9999

    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
