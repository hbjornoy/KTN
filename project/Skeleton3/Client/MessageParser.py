import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history
            # More key:values pairs are needed
        }

    def parse(self, payload):
        payload = json.loads(payload)  # decode the JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        return "Respons not valid"

    def parse_error(self, payload):
        return str(payload["timestamp"]) + ": " \
               + payload["response"] + " from " \
               + payload["sender"] + ": " + payload["content"] + "."

    def parse_info(self, payload):
        return str(payload["timestamp"]) + ": " \
               + payload["response"] + " from " \
               + payload["sender"] + ": " + payload["content"] + "."

    def parse_message(self, payload):
        return str(payload["timestamp"]) + ": " \
               + payload["response"] + " from " \
               + payload["sender"] + ": " + payload["content"] + "."

    def parse_history(self, payload):
        content = payload["content"]
        string = ""
        for i in content:
            string += str(i) + ", "

        return str(payload["timestamp"]) + ": " + \
               payload["response"] + " from " \
               + payload["sender"] + ": " + string + "."

# Include more methods for handling the different responses...
