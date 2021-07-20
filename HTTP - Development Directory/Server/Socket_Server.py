import socket as SERVER

HTTP_OK_200 = "HTTP/1.0 200 OK\n\n"
HTTP_NOT_FOUND_404 = "HTTP/1.0 404 NOT FOUND\n\n"
DOCUMENTS_HTML = "../Documents/HTML/"
HTML_404_LABEL = "404-File-Does-Not-Exist.html"

DEBUGGING = False

# Define socket host and port

SERVER_HOST = "0.0.0.0"
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

# Instantiate the internet protocol to use as IPV4/TCP-IP

SERVER_socket = SERVER.socket(SERVER.AF_INET, SERVER.SOCK_STREAM)
SERVER_socket.setsockopt(SERVER.SOL_SOCKET, SERVER.SO_REUSEADDR, 1)
SERVER_socket.bind((SERVER_HOST, SERVER_PORT))
SERVER_socket.listen(1)
print("\n" + "Listening on port %s " % SERVER_PORT + "\n" + "________________________" "\n")

# Open the server to requests

while True:

    client_Connection, client_Address = SERVER_socket.accept()

    # When a new request is made at this IP, this data exists:

    client_Request = client_Connection.recv(1024).decode()
    print(client_Request)
    REQUESTED_DIRECTORY_HEADERS = client_Request.split('\n')
    REQUESTED_HTML_LABEL = REQUESTED_DIRECTORY_HEADERS[0].split()[1]
    if REQUESTED_HTML_LABEL == '/' or REQUESTED_HTML_LABEL == "0x5C":
        REQUESTED_HTML_LABEL = "Interface.html"

    try:

        # The server opens and temporarily stores the requested HTML page for routing

        accessPoint_HTML = HTML_Server()
        accessPoint_HTML = accessPoint_HTML.Response_GET(HTTP_OK_200).Directory_GET(DOCUMENTS_HTML + REQUESTED_HTML_LABEL)
    except:

        # If the requested page does not exist, or there is an error, the server opens and temporarily stores the 404 error HTML page for routing

        accessPoint_HTML = HTML_Server()
        accessPoint_HTML = accessPoint_HTML.Response_GET(HTTP_NOT_FOUND_404).Directory_GET(DOCUMENTS_HTML + HTML_404_LABEL)

        # The data is then sent to the client in a byte stream

    client_Connection.sendall(accessPoint_HTML.Response.encode())

        # After sending information, the endpoint is closed, and the connection is terminated

    del accessPoint_HTML
    client_Connection.close()
    
    if DEBUGGING:
        SERVER_socket.close()

SERVER_socket.close()