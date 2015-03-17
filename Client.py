import socket
import json
from MessageWorker import MessageReceiver

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

        print "Welcome to AwzmChat<3 write something awezome - aand be awezome."
        print "Received thread: ", serverThread.name

    def receive_message(self, message, connection):
        response = json.loads(message)

        if response.get('error') is not None:
            print response.get('error')
        elif response.get('response') == 'login':
            print "Welcome, " + response.get('username') + ", to AwzmChat<3"
            for message in response.get('messages'):
                print message
        elif response.get('response') == 'logout':
            print "Byebye " + response.get('username')
        elif response.get('response') == 'message':
            print response.get('message')

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
        else:
            data = {'request': 'message', 'message': data}

        self.connection.sendall(json.dumps(data))

    def disconnect(self):
        self.connection.close()


if __name__ == "__main__":
    client = Client()
    #client.start('localhost', 9999)
    client.start('78.91.48.164', 9999)

    while True:
        message = raw_input('-- ')
        client.send(message)
        
        if message == '*exit':
            break

    client.disconnect()
