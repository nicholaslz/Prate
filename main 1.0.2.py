import json


def doNothing():
    while True:
        pass
    

def makeOffline(username):
    with open('userinfo.json', 'r+') as f:
        users = json.load(f)
        users[username]['Online'] = "false"
        json.dump(users, f)

        
def main():
    while True:
        user_input = input('For sending a message to someone, press 1. For awaiting a message request from someone, press 2.')
        if user_input == '1' or user_input == '2':
            if int(user_input) == 1:
                import socket
                import sys
                import time

                socket_server = socket.socket()
                server_host = socket.gethostname()
                ip = socket.gethostbyname(server_host)
                s_port = 8080

                print('This is your IP address: ', ip)
                server_host = input('Enter friend\'s IP address:')
                name = input('Enter Friend\'s name: ')
                 

                try:
                    socket_server.connect((server_host, s_port))
                    socket_server.send(name.encode())


                except:
                    print('Target not available')
                    doNothing()


                server_name = socket_server.recv(1024)
                server_name = server_name.decode()
                    
                 
                print(server_name,' has joined...')
                while True:
                    try:
                        message = (socket_server.recv(1024)).decode()
                        print(server_name, ":", message)
                        message = input("Me : ")
                        socket_server.send(message.encode())

                    except ConnectionResetError:
                        print('The target disconnected')
                        doNothing()


            elif int(user_input) == 2:
                import socket
                import sys
                import time

                new_socket = socket.socket()
                host_name = socket.gethostname()
                s_ip = socket.gethostbyname(host_name)
                port = 8080 

                new_socket.bind((host_name, port))
                print( "Binding successful!")
                print("This is your IP: ", s_ip)
                name = input('Enter name:')
                new_socket.listen(1)

                conn, add= new_socket.accept()
                print("Received connection from ", add[0])
                print('Connection Established. Connected From: ',add[0])
                client = (conn.recv(1024)).decode()
                print(client + ' has connected.')
                conn.send(name.encode())

                while True:
                    try:
                        message = input('Me : ')
                        conn.send(message.encode())
                        message = conn.recv(1024)
                        message = message.decode()
                        print(client, ':', message)

                    except ConnectionResetError:
                        print('The target disconnected')
                        doNothing()
                        
        else:
            print('Input not recognized as a valid command')
            doNothing()
            


def init():

    userInput = input('For logging in, press 1, for signing up, press 2')


    if int(userInput) == 1:
        username = input('Please enter your username')

        with open('userinfo.json', 'r+') as f:
            users = json.load(f)

        if username in users:
            password = input('Please enter your password')
            if password == users[username]["Password"]:
                print('You logged in!')
                main()

            else:
                print('Wrong password')
                doNothing()
                makeOffline(username)

        else:
            print('Username not recognized')
            doNothing()

    elif int(userInput) == 2:
        username = input('Please set your username')
        password = input('Please set your password')

        with open('userinfo.json', 'r+') as f:
            users = json.load(f)
            
        users[username] = {'Username': str(username), 'Password': str(password), 'Online': "true"}

        with open('userinfo.json','r+') as f:
            json.dump(users, f)
        
        main()    


init()
