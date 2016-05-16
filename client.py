import socket
import sys
import json
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8880)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
login = False
while not login:
    try:    
        # Send username and password
        username = raw_input("Please enter username: ")
        password = raw_input("please enter password: ")    
        message = '{"command":"login","value":{"username":"' + username + '","password":"'+password+'"}}'
        sock.sendall(message)

        # Look for the response
        data = sock.recv(1600)
        json_data = json.loads(data);
        if json_data['code'] == "100":
            login = True
            print >>sys.stderr, 'login success'
        else:
            print >>sys.stderr, json_data["message"]
    except ValueError:
        print "oopas! something wrong"

command = raw_input(">")
while  command != "quit": 
    try:
        if command == "friend list":
            message = '{"command":"friend list"}'
            sock.sendall(message)
            data = sock.recv(1600)
            json_data = json.loads(data);
            if json_data["code"] == "100":
                print >>sys.stderr, json_data["message"]
            else:
                print >>sys.stderr, json_data["error"]
            command = raw_input(">")
        else:
            print >>sys.stderr, 'INVALID COMMAND!!!'
            command = raw_input(">")
    except ValueError:
        print "oops! something wrong"    
    

print >>sys.stderr, 'buy'
sock.close()