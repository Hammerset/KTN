# -*- coding: utf-8 -*-
from threading import Thread

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):

        Thread.__init__(self)
        
        # Flag to run thread as a deamon
        self.daemon = True

        # TODO: Finish initialization of MessageReceiver
        self.client = client
        self.connection = connection
        #self.active = True

    def run(self):

        while True:
            
            try:
                msg = self.connection.recv(4096)
            except Exception as e:
                print(e.message)
                print('something something something is wrong')
                break

            if msg is None:
                print "no message"
                break
            else:
                self.client.receive_message(msg)
        pass
