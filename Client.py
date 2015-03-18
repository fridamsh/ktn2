import socket
import json
from MessageWorker import MessageReceiver
# -*- coding: utf-8 -*-

class Client(object):
    """
    This is the chat client class
    """

    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, server_port):
        self.connection.connect((host, server_port))

        serverThread = MessageReceiver(client, self.connection)
        serverThread.daemon = True
        serverThread.start()

        print "-------------------------------------------------------"
        print "     __       "
        print "    /  \       "
        print "   / /\ \                 ______       "
        print "  / /__\ \     _      _   \__  /      --  --    "
        print " / _____  \    \ \ _ / /    / /__    /  \/  \   "
        print "/_/      \_\    \_/ \_/    /____/   /_/\__/\_\ "
        print "--------------------------------------------------------"
        print
        print
        print "Welcome to AwzmChat"+u"\u2661"+"  write something awezome - aand be awezome."
        print "Type "+u"\u2192"+" *help " + u"\u2190"+"  to see what you can do in AwzmChat" + u"\u2661"
        

    def receive_message(self, message, connection):
        response = json.loads(message)

        if response.get('error') is not None:
            print response.get('error')
        elif response.get('response') == 'login':
            print "Welcome, " + response.get('username') + ", to AwzmChat" + u"\u2661"
            for message in response.get('messages'):
                print message
        elif response.get('response') == 'logout':
            print "Byebye " + response.get('username')
        elif response.get('response') == 'message':
            print response.get('message')
        elif response.get('response') == 'help':
            print response.get('content')
        elif response.get('response') == 'names':
            print "These are logged in:"
            for name in response.get('content'):
                print u"\u2661"+" "+name

    #def connection_closed(self, connection):
    #    connection.close()

    def send(self, data):
        if data.startswith("*login"):
            try:
                username = data.split()[1]
            except IndexError:
                username = ""
            data = {'request': 'login', 'username': username}
        elif data.startswith("*logout"):
            data = {'request': 'logout'}
        elif data == "*names":
            data = {'request':'names'}
        elif data.startswith("*help"):
            data = {'request':'help'}
        else:
            data = {'request': 'message', 'message': data}

        self.connection.sendall(json.dumps(data))

    def disconnect(self):
        self.connection.close()


if __name__ == "__main__":
    client = Client()
    client.start('78.91.68.195', 9999)
    #client.start('78.91.68.195', 9999)

    while True:
        message = raw_input('-- ')
        client.send(message)
        
        if message == '*exit':
            break

    client.disconnect()
