import socket
import json 

with open("settings/settings.json","r+") as settings:
    load_data = json.load(settings)  
    oauth = load_data['settings']['account_information']['oauth']

sockets = []
connections_made = len(sockets) 

def connect():
    global sockets
    global sock 
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('irc.chat.twitch.tv', 6667))       
        sock.setblocking(0) # makes it nonblocking to receive data instantly in a loop
        sock.send(bytes('PASS oauth:' + oauth + '\r\n', 'utf-8'))
        sock.send(bytes('NICK turtlerino' + '\r\n', 'utf-8'))
        sock.send(bytes('CAP REQ :twitch.tv/commands' + '\r\n', 'utf-8'))
        sock.send(bytes('CAP REQ :twitch.tv/tags' + '\r\n', 'utf-8'))
        print(f"connection {len(sockets)}  / {connections_needed()} ") 
        sockets.append(sock)
    except:
        print(f"connecting exception: {Exception}")

def socket_list():
    return sockets 

def connections_needed():
    return 10