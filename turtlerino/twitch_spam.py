from socket import socket

sock1 = socket()
sock2 = socket()
sock3 = socket()
sock4 = socket()
sock5 = socket()
sock6 = socket()
sock7 = socket()
sock8 = socket()
sock9 = socket()
sock10 = socket()


def sockets():
    sockets = [sock1, sock2, sock3, sock4, sock5, sock6, sock7, sock8, sock9, sock10]
    return sockets


def sendRaw_as_spam(data, allsocks):
    try:
        allsocks.send(bytes(data + '\r\n', 'utf-8'))  # enables you to communicate to the irc server
    except:
        pass
