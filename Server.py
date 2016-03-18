# -*- coding: utf-8 -*-
import SocketServer, json, datetime, re, time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
connectedClients = {}
history = []
helpText = "login <username> - log in with the given username \nlogout - log out \n<msg> - send message \n\
names - list users in chat\nhelp - view help text"

#"Need something here!!"

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def __init__(self, request, client_address, tcp_server):
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, tcp_server)

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        
        # Loop that listens for messages from the client
        while True:
            try:
                received_json = self.request.recv(4096)
                message = json.loads(received_json)
                
                if message['request'] == 'login' and self not in connectedClients:
                    newUsername = True
                    for username in connectedClients.values():
                        if message['content'] == username:
                            newUsername = False

                    if not newUsername:
                        self.request.sendall(self.makePayload('SERVER', 'error', 'Username already taken!'))

                    elif not self.validUsername(message['content']):
                        self.request.sendall(self.makePayload('SERVER', 'error', 'Invalid username! Use A-Z, a-z and 0-9.'))

                    else:
                        connectedClients[self] = message['content'] #Adding client to connectedClients
                        self.request.sendall(self.makePayload('SERVER', 'info', 'You successfully logged in!'))
                        print message['content'] + " connected to server."
                        self.sendToAllClients(self.makePayload('SERVER', 'message', message['content'] + " joined the chatroom!"))

                        if history:
                            self.request.sendall(self.makePayload('SERVER', 'history', history))

                elif message['request'] == 'logout' and self in connectedClients:
                    print connectedClients[self] + ' left the server'
                    connectedClients.pop(self)
                    self.request.close()
                    break

                elif message['request'] == 'msg' and self in connectedClients:
                    payload = self.makePayload(connectedClients[self], 'message', message['content'])
                    history.append(payload)
                    self.sendToAllClients(payload)

                elif message['request'] == 'names' and self in connectedClients:
                    self.sendUsersOnline()
                    pass

                elif message['request'] == 'help':
                    self.request.sendall(self.makePayload('SERVER', 'info', helpText))

                else:
                    self.request.sendall(self.makePayload('SERVER', 'error', 'Not a valid argument. Type help for a list of commands.'))

            except ValueError:
                if self in connectedClients.keys():
                    print connectedClients[self] + ' left the server'
                    connectedClients.pop(self)
                    self.request.close()
                    break

    def sendToAllClients(self,payload):
        for client in connectedClients:
            client.request.sendall(payload)

    @staticmethod
    def makePayload(sender, response, content):
        #time = datetime.datetime.now().time()
        #timeString = str(time.hour) + ":" + str(time.minute)
        #timeString = time.strftime('%H:%M:%S', time.second)
        payload = {
            'timestamp': time.strftime("%H:%M:%S", time.localtime()),
            'sender': sender,
            'response': response,
            'content': content
        }
        return json.dumps(payload)

    @staticmethod
    def validUsername(username):
    	for c in username:
    		if not re.match('[a-zA-Z0-9]+', c):
    			return False
    	return True

    def sendUsersOnline(self):
        usersOnline = 'Users online: \n'
        for user in connectedClients:
            usersOnline += connectedClients[user]
            usersOnline += '\n'
        self.request.sendall(self.makePayload('SERVER', 'info', usersOnline))



class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9999
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
