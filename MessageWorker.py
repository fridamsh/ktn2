import threading

class MessageReceiver(threading.Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and permits
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """
        
        self.daemeon = True
        self.listener = client
        self.connection = connection
        super(MessageReceiver, self).__init__()

    def run(self):
        while True:
            data = self.connection.recv(1024).strip()
            if data:
                self.listener.receive_message(data, self.connection)