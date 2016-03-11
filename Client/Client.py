# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json

request = ""
content = ""
data = ""
username = ""

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port
        username = self.connect()

        receiver = MessageReceiver(self,self.connection)
        # TODO: Finish init process with necessary code
        self.run()

    def connect(self):
        self.connection.connect((self.host, self.server_port))
        notLoggedIn = True
        while notLoggedIn:
            username = raw_input('Enter username: ')
            self.login(username)
            response = json.loads(self.connection.recv(4096))
            if response['response'] == 'info':
                notLoggedIn = False
                print response['content']
            else:
                print response['response'] + ": " + response['content']
        return username

    def run(self):
        while True:
            command = raw_input()
            if command.lower() == 'logout' or command.lower() == 'names' or command.lower() == 'help':
                payload = {
                'request': command.lower(),
                'content': None
                }
                self.connection.sendall(json.dumps(payload))
                if command.lower() == 'logout':
                    self.disconnect()
                    break
            else:
                payload = {
                'request': 'msg',
                'content': command
                }
                self.connection.sendall(json.dumps(payload))
        print "Chatroom disconnected."

    def login(self,username):
        payload = {
        'request': 'login',
        'content': username
        }
        payload = json.dumps(payload)
        self.connection.sendall(payload)

        
    def disconnect(self):
        # TODO: Handle disconnection
        self.connection.close()

    def receive_message(self, message):
        # TODO: Handle incoming message
        parser = MessageParser()
        messageType = parser.parse(message)
        print messageType

    def send_payload(self, data, content):
        # TODO: Handle sending of a payload
        data = {'request':request,'content':content}
        payload = json.dumps(data)
        self.connection.send(payload)
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
