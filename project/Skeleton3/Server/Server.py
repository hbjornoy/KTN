import socketserver
import json
import re
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""


class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.username = None
        # Add this connection to list of connections
        self.server.connections.append(self)
        # Received data
        self.recv = None

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096).decode()

            try:
                recv = json.loads(received_string)
            except Exception:
                self.logout()
                break

            if recv["request"] == "login" and recv["content"] != "None":
                self.login(recv["content"])
            elif recv["request"] == "help" and recv["content"] == "None":
                self.help()
            elif self.username is not None:
                if recv["request"] == "logout" and recv["content"] == "None":
                    if self.username is not None:
                        self.logout()
                        break
                    else:
                        self.error("Not logged in.")
                elif recv["request"] == "msg" and recv["content"] != "None":
                    self.message(self.username, recv["content"])
                elif recv["request"] == "names" and recv["content"] == "None":
                    self.names()
                else:
                    self.error("The request and/or content\
                    you sent is/are not supported.")
            else:
                self.error("The request and/or content\
                 you sent is/are not supported.")

    def login(self, username):
        if re.match("^[A-Za-z0-9_-]+$", username)\
                and not self.user_connected(username):
            self.username = username
            print(username + " logged in.")
            self.info("Login successful.")

        else:
            self.error('Invalid username or already taken')

    def logout(self):
        if self.username is not None:
            print(self.username + " logged out.")
        else:
            print("A user disconnected from the server.")
        self.info("Logout successful.")
        server.connections.remove(self)
        self.connection.close()

    def names(self):
        names = ""
        for user in server.connections:
            if user.username is not None:
                names += user.username + ", "

        self.info(names.strip(", "))

    def help(self):
        self.info("Available commands: login <username>,\
         logout, msg <message>, names, help")

    def user_connected(self, username):
        for user in server.connections:
            if user.username == username:
                return True
        return False

    def history(self):
        content_list = []
        for message in server.messages:
            content_list.append(message)

        self.send_payload("Server", "history", content_list)

    def message(self, sender, content):
        self.send_payload_all(sender, "message", content)

    def info(self, content):
        self.send_payload("Server", "info", content)

    def error(self, content):
        self.send_payload("Server", "error", content)

    def send_payload_all(self, sender, response, content):
        for user in server.connections:
            user.send_payload(sender, response, content)

    def send_payload(self, sender, response, content):
        payload = {"timestamp": time.asctime(time.localtime(time.time())),
                   "sender": sender, "response": response, "content": content}
        payload_json = json.dumps(payload)
        self.connection.send(payload_json.encode())

        if response == "message":
            print(type(payload_json))
            server.messages.append(payload_json)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.
    No alterations are necessary
    """
    allow_reuse_address = True
    connections = []
    messages = []


if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.
    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()