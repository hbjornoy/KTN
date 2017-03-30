# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json
import time


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
        # TODO: Finish init process with necessary code
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        self.thread = MessageReceiver(self, self.connection)
        self.thread.start()
        while True:
            time.sleep(0.5)
            request_content = input("Type in your request:").split(' ', 1)

            try:
                request_content[0] = request_content[0].lower()
                request_content[1] = request_content[1].lower()
                print(request_content)

                if request_content[1] == "none":
                    if request_content[0] == "names":
                        self.send_payload(
                            {"request": "names", "content": "None"})
                    elif request_content[0] == "help":
                        self.send_payload(
                            {"request": "help", "content": "None"})
                else:
                    if request_content[0] == "logout":
                        self.disconnect()
                    elif request_content[0] == "names":
                        self.send_payload(
                            {"request": "names", "content": "None"})
                    elif request_content[0] == "help":
                        self.send_payload(
                            {"request": "help", "content": "None"})
                    elif request_content[0] == "login":
                        self.send_payload(
                            {"request": "login", "content": request_content[1]})
                    elif request_content[0] == "msg":
                        self.send_payload(
                            {"request": "msg", "content": request_content[1]})
                    else:
                        self.not_supported(request_content)
            except IndexError:
                print("Input not valid!")

    def disconnect(self):
        payload = {"request": "logout", "content": "None"}
        self.send_payload(payload)

    def receive_message(self, message):
        message_parser = MessageParser()
        print(message_parser.parse(message))


    def send_payload(self, data):
        temp_data = json.dumps(data)
        self.connection.send(temp_data.encode())

    def not_supported(self, request_content):
        print("The following request and/or content: " + request_content[0] +
              " and " + request_content[1] + " is not supported.")

    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.
    No alterations are necessary
    """
    client = Client('localhost', 9998)