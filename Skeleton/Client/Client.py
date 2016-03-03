# -*- coding: utf-8 -*-
import socket, json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

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
        
        # TODO: Finish init process with necessary code
        self.host = host
        self.server_port = server_port
        self.run()
        self.msg = ''

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

        self.thread = MessageReceiver(self, self.connection)
        self.thread.start() 
        thread_running = self.thread.is_alive() 

        while thread_running:
            #print "You are connected to the server. Use login,logout,msg,names,help"
            user_input = raw_input().split(' ', 1) 
            request = user_input[0]
            content = 'None'

            try:
                content = user_input[1]
            except Exception, e:
                # ?
                pass
            

            if request == "login":
                print "Your request was login" 
                payload = json.dumps({'request': 'login', 'content': content})
                self.send_payload(payload)
                #print payload

            elif request == "logout":
                payload = json.dumps({'request': 'logout', 'content': None})
                self.send_payload(payload)

            elif request == "msg":
                payload = json.dumps({'request': 'msg', 'content': content})
                self.send_payload(payload)

            elif request == "names":
                payload = json.dumps({'request': 'names', 'content': None})
                self.send_payload(payload)

            elif request == "help":
                payload = json.dumps({'request': 'help', 'content': None})
                self.send_payload(payload)
        pass

    def disconnect(self):
        # /kill
        self.connection.close()
        self.Thread.is_alive = False
        print "connection closed"
        pass

    def receive_message(self, message):
        messageParser = MessageParser()
        messageParser.parse(message)
        pass

    def send_payload(self, data):
        self.connection.send(data)
        pass

if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    print "You are now connected to the server"
    print "Please start by using login <your username> "
    client = Client('localhost', 8080)

