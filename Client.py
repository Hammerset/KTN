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
        
        self.host = host
        self.server_port = server_port
        self.run()
        self.msg = ''

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))

        self.thread = MessageReceiver(self, self.connection)
        self.thread.start() 

        while True:
            user_input = raw_input().split(' ', 1) 

            #Send input to server 
            payload = self.make_payload(user_input)
            self.send_payload(payload)
	    
    	    #If user logs out, disconnet from server and terminate process
    	    if user_input[0] == 'logout':
                self.disconnect()
                break



    def disconnect(self):
        self.connection.close()
        print "Your have disconnect from server."

    def receive_message(self, message):
        messageParser = MessageParser()
        messageParser.parse(message)

    def send_payload(self, data):
        self.connection.send(data)

    def make_payload(self, data):
    	request = data[0]
    	content = None
    	try:
    	    content = data[1]
        except Exception, e:
            pass
        return json.dumps({'request': request, 'content': content})

if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    print "You are now connected to the server"
    print "Type help for a list of commands."
    client = Client('localhost', 9999)

