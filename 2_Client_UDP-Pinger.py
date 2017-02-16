import time
from socket import *

# Get the server hostname and port as command line arguments
host = "localhost"
port = 9999
timeout = 1  # in seconds

# Create UDP client socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
# Note the second parameter is NOT SOCK_STREAM
# but the corresponding to UDP

# Set socket timeout as 1 second
clientSocket.settimeout(timeout)

# Sequence number of the ping message
ptime = 0

# Ping for 10 times
while ptime < 10:
    ptime += 1

    # Record the "sent time"
    sentTime = time.time()

    # Format the message to be sent as in the Lab description
    data = "Ping" + str(ptime) + " " + str(sentTime)

    try:
        # FILL IN START

        # Send the UDP packet with the ping message
        clientSocket.sendto(data.encode(), (host, port))

        # Receive the server response
        returned, server_adress = clientSocket.recvfrom(1024)

        # Record the "received time"
        recieveTime = time.time()

        # Display the server response as an output
        print(returned)

        # Round trip time is the difference between sent and received time
        print("Sent: " + str(sentTime))
        print("Recieved: " + str(recieveTime))
        print("RRT: " + str(recieveTime - sentTime) + "ms")

    except:
        # Server does not response
        # Assume the packet is lost
        print("Request timed out.")
        continue

# Close the client socket
clientSocket.close()

