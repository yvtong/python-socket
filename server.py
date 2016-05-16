import socket
import sys
import json
from thread import start_new_thread
#create an INET, STREAMing socket
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
#bind the socket to a public host,
# and a well-known port
serversocket.bind(('localhost', 8880))
#become a server socket
serversocket.listen(5)

def client_thread(conn):

    while True:
        # Wait for a connection
        try:
            print >>sys.stderr, 'connection from', client_address
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(1600)
                print >>sys.stderr, 'received "%s"' % data
                if data:
                    print >>sys.stderr, 'sending data back to the client'
                    json_data = json.loads(data);
                    if json_data["command"] == "login":
                       if json_data["value"]["username"] == "awang" and json_data["value"]["password"] == "1234567":
                           connection.sendall('{"code":"100","message":"login success"}')
                       else:
                           connection.sendall('{"code":"99","message":"wrong password"}')
                    else:
                        connection.sendall('{"code":"0","error":"not implemented"}')
                else:
                    print >>sys.stderr, 'no more data from', client_address
                    break
                
        finally:
            # Clean up the connection
            connection.close()

while True:
    # blocking call, waits to accept a connection
    connection, client_address = serversocket.accept()
    start_new_thread(client_thread, (connection,))

serversocket.close()