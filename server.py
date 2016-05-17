import socket
import struct
import time
import threading
import json
import sys

user = '[{"username":"andy","value":{"password":"123","status":"offline"}},' \
        '{"username":"mars","value":{"password":"123","status":"offline"}},' \
        '{"username":"shuai","value":{"password":"123","status":"offline"}}]'
json_user = json.loads(user)

class ClientHandler(threading.Thread):
 
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client_sock, self.client_addr = client

    def run(self):
 
        global thread_username
 
        while True:
            data = self.client_sock.recv(1600)
            if True:
                if data:
                    print >> sys.stderr, 'sending data back to the client'
                    json_data = json.loads(data)
                    if json_data["command"] == "login":
                        length = len(json_user)
                        i = 0
                        while i < length:
                            if json_data["value"]["username"] == json_user[i]["username"] and json_data["value"]["password"] == json_user[i]["value"]["password"]:
                                self.client_sock.sendall('{"code":"100","message":"Login success"}')
                                json_user[i]["value"]["status"] = "online"
                                thread_username = json_user[i]["username"]
                            elif json_data["value"]["username"] == json_user[i]["username"] and json_data["value"]["password"] != json_user[i]["value"]["password"]:
                                self.client_sock.sendall('{"code":"99","message":"Wrong password"}')
                            i+=1
                    elif json_data["command"] == "friend list":
                        print >> sys.stderr, 'get online friend'
                        length = len(json_user)
                        i = 0
                        online_users = ""
                        while i < length:
                            if json_user[i]["value"]["status"] == "online" and json_user[i]["username"] != thread_username:
                                online_users += json_user[i]["username"] + " "
                            i+=1
                        if online_users != "":
                            self.client_sock.sendall('{"code":"100","message":"' + online_users + ' online "}')
                        else:
                            self.client_sock.sendall('{"code":"100","message":"no friends online!"}')
                    elif json_data["command"] == "quit":
                        length = len(json_user)
                        i = 0
                        while i < length:
                            if json_data["username"] == thread_username:
                                json_user[i]["value"]["status"] = "offline"
                            i+=1
                    else:
                        self.client_sock.sendall('{"code":"0","error":"not implemented"}')
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 8880))
sock.listen(0)
print "Waiting_for_clients_..."
 
while True: # Serve forever
    client = sock.accept()
    ClientHandler(client).start()