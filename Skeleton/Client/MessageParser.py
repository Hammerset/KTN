import json

class MessageParser():
    def __init__(self):

        # This is response from the server 
        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history   
        }

    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return

    def parse_error(self, payload):
        print "parse_error: %s" % payload['content']
        #return payload['content'];
    
    def parse_info(self, payload):
        print "parse_info: %s" % payload['content']
        #return payload['content'];

    def parse_message(self, payload):
        print "%s %s : %s" % (payload['timestamp'], payload['sender'],  payload['content'])
        # Timestamp - from - msg

    def parse_history(self, payload): 
        print "This is what you missed since last time"

        for payload in payload['content']:
            history = json.loads(payload)
            self.parse_message(history)
