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

        print "---------------------------------------------------------------------"
        print "     __                                              __      __"
        print "    /  \                                            /   \  /   \ "
        print "   / /\ \                  ______                  |     \/     |"
        print "  / /__\ \      _      _   \__  /     __  __        \          / "
        print " / _____  \    \ \ _ / /    / /__    /  \/  \         \      /"
        print "/_/      \_\    \_/ \_/    /____/   /_/\__/\_\          \  /"
        print "---------------------------------------------------------\/-----------"
        print
        print
        print "Welcome to AwzmChat<3 write something awezome - aand be awezome."
        print "Type -> *help <- to see what you can do in AwzmChat<3"
        #print "Welcome to AwzmChat"+u"\u2661"+"  write something awezome - aand be awezome."
        #print "Type "+u"\u2192"+" *help " + u"\u2190"+"  to see what you can do in AwzmChat" + u"\u2661"

    def receive_message(self, message, connection):
        response = json.loads(message)

        if response.get('response') == 'error':
            print response.get('content')

        elif response.get('response') == 'history':
            print "Welcome, " + response.get('sender') + ", to AwzmChat<3"
            for message in response.get('history'):
                print message

        elif response.get('response') == 'info':
            print "Byebye " + response.get('sender')

        elif response.get('response') == 'message':
            print response.get('content')

        elif response.get('response') == 'help':
            print response.get('content')

        elif response.get('response') == 'names':
            print "These are logged in:"
            for name in response.get('content'):
                print "<3 " + name

    #def connection_closed(self, connection):
    #    connection.close()

    def send(self, data):
        if data.startswith("*login"):
            try:
                username = data.split()[1]
            except IndexError:
                username = ""
            data = {'request': 'login', 'content': username}
        elif data.startswith("*logout"):
            data = {'request': 'logout', 'content': None}
        elif data == "*names":
            data = {'request':'names', 'content': None}
        elif data.startswith("*help"):
            data = {'request':'help', 'content': None}
        else:
            data = {'request': 'msg', 'content': data}

        self.connection.sendall(json.dumps(data))

    def disconnect(self):
        self.connection.close()


if __name__ == "__main__":
    client = Client()
    #client.start('localhost', 9999)
    client.start('78.91.71.85', 9999)

    while True:
        message = raw_input('-- ')
        client.send(message)
        
        if message == '*exit':
            break

    client.disconnect()
