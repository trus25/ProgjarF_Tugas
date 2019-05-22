import socket
import os
import json

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8889


class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (TARGET_IP,TARGET_PORT)
        self.sock.connect(self.server_address)
        self.tokenid=""
        self.currentclient=""

    def proses(self,cmdline):
        j=cmdline.strip().split(" ")
        try:
            command=j[0]
            if (command=='auth'):
                username=j[1]
                password=j[2]
                return self.login(username,password)
            elif (command=='send'):
                usernameto = j[1]
                message=""
                for w in j[2:]:
                    message="{} {}" . format(message,w)
                return self.sendmessage(usernameto,message)
            elif (command=='inbox'):
                return self.inbox()
            elif (command=='logout'):
                self.tokenid=""
                print "logout berhasil"
                return self.tokenid
            elif (command == 'join_group'):
                group_token = j[1]
                return self.join_group(group_token)

            elif (command == 'leave_group'):
                group_token = j[1]
                return self.leave_group(group_token)

            elif (command == 'create_group'):
                group_name = j[1]
                return self.create_group(group_name)

            elif (command == 'inbox_group'):
                group_name = j[1]
                return self.inbox_group(group_name)

            elif (command == 'list_group'):
                group_name = j[1]
                return self.list_group(group_name)

            elif (command == 'send_group'):
                group_token = j[1]
                message=""
                for w in j[2:]:
                    message="{} {}" . format(message, w)
                return self.send_group(group_token, message)

            elif (command == 'send_file'):
                usernameto = j[1]
                filename = j[2]
                return self.send_file(usernameto, filename)
            else:
                return "*Maaf, command tidak benar"
        except IndexError:
            return "-Maaf, command tidak benar"

    def sendstring(self,string):
        try:
            self.sock.sendall(string)
            receivemsg = ""
            while True:
                data = self.sock.recv(10)
                if (data):
                    receivemsg = "{}{}" . format(receivemsg,data)
                    if receivemsg[-4:]=="\r\n\r\n":
                        return json.loads(receivemsg)
        except:
            self.sock.close()
    def login(self,username,password):
        string="auth {} {} \r\n" . format(username,password)
        result = self.sendstring(string)
        if result['status']=='OK':
            self.tokenid=result['tokenid']
            return "username {} logged in, token {} " .format(username,self.tokenid)
        else:
            return "Error, {}" . format(result['message'])
    def sendmessage(self,usernameto="xxx",message="xxx"):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="send {} {} {} \r\n" . format(self.tokenid,usernameto,message)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "message sent to {}" . format(usernameto)
        else:
            return "Error, {}" . format(result['message'])
    def inbox(self):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="inbox {} \r\n" . format(self.tokenid)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "{}" . format(json.dumps(result['messages']))
        else:
            return "Error, {}" . format(result['message'])
    def send_file(self, usernameto, filename):
        if (self.tokenid==""):
            return "Error, not authorized"

        string="send_file {} {} {} \r\n" . format(self.tokenid, usernameto, filename)
        self.sock.sendall(string)
        try:
            with open(filename, 'rb') as file:
                while True:
                    bytes = file.read(1024)
                    if not bytes:
                        result = self.sendstring("DONE")
                        break
                    self.sock.sendall(bytes)
                file.close()
        except IOError:
            return "Error, file not found"
        if result['status']=='OK':
            return "{} successfully sent to {}" . format(filename,usernameto)
        else:
            return "Error, {}" . format(result['message'])

    def create_group(self, group_name):
        if (self.tokenid==""):
            return "Error, not authorized"
        string = "create_group {} {} \r\n" . format(self.tokenid, group_name)
        result = self.sendstring(string)

        if result['status']=='OK':
            return "{}" . format(result['messages'])
        else:
            return "Error, {}" . format(json.dumps(result['messages']))

    def join_group(self, group_token):
        if (self.tokenid==""):
            return "Error, not authorized"
        string = "join_group {} {} \r\n" . format(self.tokenid, group_token)
        result = self.sendstring(string)

        if result['status']=='OK':
            return "{}" . format(result['message'])
        else:
            return "Error, {}" . format(result['message'])

    def leave_group(self, group_token):
        if (self.tokenid==""):
            return "Error, not authorized"
        string = "leave_group {} {} \r\n" . format(self.tokenid, group_token)
        result = self.sendstring(string)

        if result['status']=='OK':
            return "{}" . format(result['message'])
        else:
            return "Error, {}" . format(result['message'])

    def inbox_group(self, group_token):
        if (self.tokenid == ""):
            return "Error, not authorized"
        string = "inbox_group {} {} \r\n".format(self.tokenid, group_token)
        result = self.sendstring(string)

        if result['status'] == 'OK':
            for i in result['message']:
                print i
            return ""
        else:
            return "Error, {}".format(result['message'])

    def list_group(self, group_token):
        if (self.tokenid==""):
            return "Error, not authorized"
        string = "list_group {} {} \r\n" . format(self.tokenid, group_token)
        result = self.sendstring(string)

        if result['status']=='OK':
            return "{}" . format(json.dumps(result['message']))
        else:
            return "Error, {}" . format(result['message'])

    def send_group(self, group_token, message):
        if (self.tokenid==""):
            return "Error, not authorized"
        string = "send_group {} {} {} \r\n" . format(self.tokenid, group_token, message)
        result = self.sendstring(string)
        print result

        if result['status']=='OK':
            return "{}" . format(result['message'])
        else:
            return "Error, {}" . format(result['message'])


if __name__=="__main__":
    cc = ChatClient()
    while True:
        cmdline = raw_input("Command :")
        print cc.proses(cmdline)

