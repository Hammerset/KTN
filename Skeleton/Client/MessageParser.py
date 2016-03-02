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
            # Response not valid

    def parse_error(self, payload):
        return payload['content'];
    
    def parse_info(self, payload):
        return payload['content'];

    def parse_message(self, payload):
        return payload['timestamp'] + " " + payload['sender'] + ": " payload['content']

    def parse_history(self, payload): 
        return payload['content'];
