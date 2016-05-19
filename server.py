import socket
import struct
import time
import threading
import json
import sys

user = '[{"username":"andy","value":{"password":"123","status":"offline"},"friends":["mars"]},' \
       '{"username":"mars","value":{"password":"123","status":"offline"},"friends":["andy"]},' \
       '{"username":"shuai","value":{"password":"123","status":"offline"},"friends":["andy"]},'\
        '{"username":"wang","value":{"password":"123","status":"offline"},"friends":["mars"]}]'
json_user = json.loads(user)
thread = []
name = []
class ClientHandler(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client_sock, self.client_addr = client
        thread.append(self.client_sock)
        name.append("")
        self.index_in_thread = len(thread) - 1;
    def run(self):
        thread_username = ""
        print >> sys.stderr, 'connection from', self.client_addr
        while True:
            data = self.client_sock.recv(1600)
            if True:
                if data:
                    print >> sys.stderr, 'sending data back to the client'
                    json_data = json.loads(data)

                    print json_data

                    if json_data["command"] == "login":
                        length = len(json_user)
                        i = 0
                        while i < length:
                            if json_data["value"]["username"] == json_user[i]["username"] and json_data["value"][
                                "password"] == json_user[i]["value"]["password"]:
                                self.client_sock.sendall('{"code":"100","message":"Login success"}')
                                json_user[i]["value"]["status"] = "online"
                                self.thread_username = json_user[i]["username"]
                                name[self.index_in_thread] = self.thread_username
                            elif json_data["value"]["username"] == json_user[i]["username"] and json_data["value"][
                                "password"] != json_user[i]["value"]["password"]:
                                self.client_sock.sendall('{"code":"99","message":"Wrong password"}')
                            i += 1
                            #if i == length:
                            #    self.client_sock.sendall('{"code":"98","message":"User unexited"}')

                    elif json_data["command"] == "friend list":
                        print >> sys.stderr, 'friend list'
                        friends = ""
                        length = len(json_user)
                        i = 0
                        while i < length:
                            if json_user[i]["username"] == json_data["username"]:
                                j = 0
                                while j < len(json_user[i]["friends"]):
                                    friendname = json_user[i]["friends"][j]
                                    w=0
                                    while w < len(json_user):
                                        if friendname == json_user[w]["username"]:
                                            friends += friendname +' '+ json_user[w]["value"]["status"] +' '
                                        w += 1
                                    j +=1
                            i +=1
                        if friends != "":
                            self.client_sock.sendall('{"command":"friend list","message":"' + friends + '"}')
                        else:
                            self.client_sock.sendall('{"command":"friend list","message":"Friend list is empty!"}')

                    elif json_data["command"] == "friend add":
                        print >> sys.stderr, 'friend add'
                        add = json_data["add"]
                        i = 0
                        while i < len(json_user):
                            if json_user[i]["username"] == json_data["username"]:
                                json_user[i]["friends"].append(add)
                                print json_user[i]["friends"]
                            i+=1
                        self.client_sock.sendall('{"command":"friend add","message":"'+ add +' added into the friend list"}')

                    elif json_data["command"] == "friend rm":
                        print >> sys.stderr, 'friend rm'
                        rm = json_data["rm"]
                        i = 0
                        while i < len(json_user):
                            if json_user[i]["username"] == json_data["username"]:
                                json_user[i]["friends"].remove(rm)
                                print json_user[i]["friends"]
                            i += 1
                        self.client_sock.sendall('{"command":"friend rm","message":"' + rm + ' removed from the friend list"}')


                    elif json_data["command"] == "send":
                        who = json_data["who"]
                        message = json_data["message"]
                        i = 0
                        while i < len(json_user):
                            if who == json_user[i]["username"]:
                                if json_user[i]["value"]["status"] == "online":
                                    w = 0
                                    while w < len(thread):
                                        if who == name[w]:
                                            thread[w].sendall('{"command":"send","message":" ' + who + ':' +  message + ' "}')
                                            print >> sys.stderr, 'send message to ' + who
                                        w += 1
                            i += 1

                    elif json_data["command"] == "quit":
                        length = len(json_user)
                        i = 0
                        while i < length:
                            if json_data["username"] == json_data["username"]:
                                json_user[i]["value"]["status"] = "offline"
                            i += 1


                    else:
                        self.client_sock.sendall('{"code":"0","error":"not implemented"}')


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind(('', 8888))
sock.listen(5)
print "Waiting for clients ..."

while True:  # Serve forever
    client = sock.accept()
    ClientHandler(client).start()