import socket as SERVER

HTTP_OK_200 = 'HTTP/1.0 200 OK\n\n'
HTML_INTERFACE = '../Documents/HTML/Interface.html'

DEBUGGING = True

# Define socket host and port

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

# Instantiate internet protocol as IPV4/TCP-IP

SERVER_socket = SERVER.socket(SERVER.AF_INET, SERVER.SOCK_STREAM)
SERVER_socket.setsockopt(SERVER.SOL_SOCKET, SERVER.SO_REUSEADDR, 1)
SERVER_socket.bind((SERVER_HOST, SERVER_PORT))
SERVER_socket.listen(1)
print("\n" + "Listening on port %s " % SERVER_PORT + "\n" + "________________________" "\n")

while True:

    client_Connection, client_Address = SERVER_socket.accept()

    # When a new request is made at this IP, this data exists
    request = client_Connection.recv(1024).decode()
    print(request)

    class HTML_Server:
        def __init__(self):
            self.Response = ''
        def Response_GET(self, response):
            self.Response += response
            print("\033[1A" + "===\n" + self.Response + "GET Request received!\n" + "=\_")
            return self
        def Directory_GET(self, directory):
            self.Response += open(directory).read()
            print(f"This directory was read: {directory}\n" + "=_/\n")
            return self

    accessPoint_HTML = HTML_Server()

    # Server opens and stores the default HTML page (useful for validating)
    accessPoint_HTML = accessPoint_HTML.Response_GET(HTTP_OK_200).Directory_GET(HTML_INTERFACE)

    client_Connection.sendall(accessPoint_HTML.Response.encode())
    client_Connection.close()
    
    if DEBUGGING:
        SERVER_socket.close()

SERVER_socket.close()