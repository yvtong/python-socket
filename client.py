import socket
import sys
import json
import getpass
import thread

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# Connect the socket to the port where the server is listening

def recv_data():
    while 1:
        try:
            data = sock.recv(1600)
            try:
                json_data = json.loads(data)
                if json_data["command"] != "talk":
                    print >> sys.stderr, json_data["message"]
                else:
                    print >> sys.stderr, json_data["message"]
            except:
                print >> sys.stderr, data
        except:
            print "Server closed connection, thread exiting."
            thread.interrupt_main()
            break

server_address = ('localhost', 8888)
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
        json_data = json.loads(data)
        if json_data['code'] == "100":
            login = True
            print >> sys.stderr, 'login success'
        else:
            print >> sys.stderr, json_data["message"]
    except ValueError:
        print "something wrong"

thread.start_new_thread(recv_data,())

command = raw_input(">")
taling = False
talking_to = ""
while command != "quit":
    command_extends = command.split()
    try:
        if command == "friend list":
            message = '{"command":"friend list","username":"' + username + '"}'
            sock.send(message)
            command = raw_input(">")


        elif "friend add" in command:
            try:
                message = '{"command":"friend add","add":"'+ command_extends[2] +'","username":"' + username + '"}'
                sock.send(message)
                command = raw_input(">")
            except ValueError:
                command = raw_input(">")


        elif "friend rm" in command:
            try:
                message = '{"command":"friend rm","rm":"' + command_extends[2] + '","username":"' + username + '"}'
                sock.send(message)
                command = raw_input(">")
            except ValueError:
                command = raw_input(">")


        elif "send" in command:
            try:
                message = '{"command":"send","who":"' + command_extends[1] + '","message":"'+ command_extends[2] +'","username":"' + username + '"}'
                sock.send(message)
                command = raw_input(">")
            except ValueError:
                command = raw_input(">")

        elif "talk" in command:
            try:
                message = '{"command":"send","who":"'+ command_extends[1] +'","usename":"'+ username +'","message":"'+ username +',want to talk with you!"}'
                sock.send(message)
                talking = True
                talking_to = command_extends[1]
                command = raw_input(">")
            except ValueError:
                command = raw_input(">")
        elif command == "":
            command = raw_input(">")
        elif talking:
            message ='{"command":"send","who":"' + talking_to + '","usename":"' + username + '","message":"'+ command +'"}'
            sock.send(message)
            command = raw_input(">")
        else:
            print >> sys.stderr, 'INVALID COMMAND!!!'
            command = raw_input(">")
    except ValueError:
        print "something wrong"
message = '{"command":"quit","username":"' + username + '"}'
sock.send(message)
print >> sys.stderr, 'Bey!'
sock.close()