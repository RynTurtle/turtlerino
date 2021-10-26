import errno
from twitch.irc.connect_socket import socket_list   
import socket 
rotate_sockets = 0

def sendRaw(message,channel):
    global rotate_sockets
    try:
        if rotate_sockets == len(socket_list()):
            rotate_sockets = 0
        print(f"Sending: {message} ")
        socket_list()[rotate_sockets].send(bytes(f"PRIVMSG #{channel} :{message}" + '\r\n', 'utf-8'))
        rotate_sockets += 1
    except IOError as e:
        if e.errno == errno.EPIPE: 
            pass



def join(channel):
    try:
        socket_list()[0].send(bytes(f"JOIN #{channel}" + '\r\n', 'utf-8'))
    except IOError as e:
        if e.errno == errno.EPIPE: 
            pass

def part(channel):
    try:
        socket_list()[0].send(bytes(f"PART #{channel}" + '\r\n', 'utf-8'))
    except IOError as e:
        if e.errno == errno.EPIPE: 
            pass