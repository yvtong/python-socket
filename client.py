import socket
import sys
import json
import getpass

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# Connect the socket to the port where the server is listening
server_address = ('localhost', 8880)
print >> sys.stderr, '========Welcome to WeChat!========'
print >> sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
login = False
username = ""
while not login:
    try:
        # Send username and password
        username = raw_input("Please enter username:")
        password = raw_input("Please enter password:")
        message = '{"command":"login","value":{"username":"' + username + '","password":"' + password + '"}}'
        sock.send(message)

        # Look for the response
        data = sock.recv(160)
        json_data = json.loads(data);
        if json_data['code'] == "100":
            login = True
            print >> sys.stderr, 'login success'
        else:
            print >> sys.stderr, json_data["message"]
    except ValueError:
        print "something wrong"

command = raw_input(">")
while command != "quit":
    try:
        if command == "friend list":
            message = '{"command":"friend list","username":"' + username + '"}'
            sock.send(message)
            data = sock.recv(1600)
            json_data = json.loads(data);
            print >> sys.stderr, json_data["message"]
            command = raw_input(">")
        else:
            print >> sys.stderr, 'INVALID COMMAND!!!'
            command = raw_input(">")
    except ValueError:
        print "something wrong"
message = '{"command":"quit","username":"' + username + '"}'
sock.send(message)
print >> sys.stderr, 'buy'
sock.close()