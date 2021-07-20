import socket as SERVER

HTTP_OK_200 = 'HTTP/1.0 200 OK\n\n'
DOCUMENTS_HTML = '../Documents/HTML/'

DEBUGGING = True

# Define socket host and port

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

# Define a server structure

class HTML_Server:
    def __init__(self):
        self.Response = ''
    def Response_GET(self, response):
        self.Response += response
        print("\033[1A" + "===\n" + self.Response + "GET Request received!\n" + "=\_")
        return self
    def Directory_GET(self, directory):
        self.Response += open(directory).read() # add .close()
        print(f"This directory was read: {directory}\n" + "=_/\n")
        return self

# Instantiate internet protocol as IPV4/TCP-IP

SERVER_socket = SERVER.socket(SERVER.AF_INET, SERVER.SOCK_STREAM)
SERVER_socket.setsockopt(SERVER.SOL_SOCKET, SERVER.SO_REUSEADDR, 1)
SERVER_socket.bind((SERVER_HOST, SERVER_PORT))
SERVER_socket.listen(1)
print("\n" + "Listening on port %s " % SERVER_PORT + "\n" + "________________________" "\n")

# Open the server to requests

while True:

    client_Connection, client_Address = SERVER_socket.accept()

    # When a new request is made at this IP, this data exists
    client_Request = client_Connection.recv(1024).decode()
    print(client_Request)
    REQUESTED_DIRECTORY_HEADERS = client_Request.split('\n')
    REQUESTED_HTML_LABEL = REQUESTED_DIRECTORY_HEADERS[0].split()[1]
    if REQUESTED_HTML_LABEL == '/' or REQUESTED_HTML_LABEL == "0x5C":
        REQUESTED_HTML_LABEL = "Interface.html"

    accessPoint_HTML = HTML_Server()

    # Server opens and stores the default HTML page (useful for validating)
    accessPoint_HTML = accessPoint_HTML.Response_GET(HTTP_OK_200).Directory_GET(DOCUMENTS_HTML + REQUESTED_HTML_LABEL)

    client_Connection.sendall(accessPoint_HTML.Response.encode())
    client_Connection.close()
    
    if DEBUGGING:
        SERVER_socket.close()

SERVER_socket.close()