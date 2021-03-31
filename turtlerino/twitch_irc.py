import socket
import errno
import threading
import textwrap
import twitch_spam as spam
import time
import json
import colorsys

with open("account_options.txt") as myfile:
    oauth = myfile.readlines()[0:1]
    oauth = oauth[0].replace("oauth:", "").replace(" ", "")


def connect():
    global sock
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('irc.chat.twitch.tv', 6667))


def sendRaw(data):
    try:
        sock.send(bytes(data + '\r\n', 'utf-8'))
    except IOError as e:
        if e.errno == errno.EPIPE:
            pass


def send(text: str, channel: str, slash_me, color_each_msg):
        channel = "#" + channel.lower() if not channel.startswith("#") else channel.lower()
        messages = textwrap.wrap(text , 500, break_long_words=False, replace_whitespace=False)
        if slash_me == "On":
            sendRaw(f'PRIVMSG {channel} :/me {str(messages[0])}')
            if len(messages) > 1:
                nextmsg = ' '.join(messages[1:])
                send(" " + nextmsg + " ",channel,slash_me,color_each_msg)
            if color_each_msg == "On":
                rainbow(color_each_msg, channel, slash_me)
        else:
            sendRaw(f'PRIVMSG {channel} :{str(messages[0])}')
            if color_each_msg == "On":
                rainbow(color_each_msg, channel, slash_me)
        if len(messages) > 1:
            nextmsg = ' '.join(messages[1:])
            send(" " + nextmsg + " ",channel,slash_me,color_each_msg)


def sendcommand(message, channel):
    channel = "#" + channel.lower() if not channel.startswith("#") else channel.lower()
    sendRaw(f'PRIVMSG {channel} :{message}')


def login():
    sendRaw('PASS oauth:' + oauth)
    sendRaw('NICK turtlerino')


def keep_alive():
    while True:  # continuously getting the data
        chat = sock.recv(1024).decode('utf -8')  # socket data (chat)
        print(chat)
        if "PING" in chat:
            sendRaw("PONG")  # This keeps the bot alive  when  twitch sends PING a bot needs to send PONG back.


def connect_and_stay_alive():
    connect()
    login()
    keep_alive()


thread_twitch = threading.Thread(target=connect_and_stay_alive)
thread_twitch.start()


def connect_and_login_and_keep_spam_alive():
    try:
        count = 0
        for all_sockets in spam.sockets():
            time.sleep(0.2)
            print("Connecting")
            count += 1
            all_sockets.connect(('irc.chat.twitch.tv', 6667))
            print("Logging in")
            if count == 10:
                print("--------------------------")
                print("you can spam now WideHardo")
                print("--------------------------")
            spam.sendRaw_as_spam('PASS oauth:' + oauth, all_sockets)
            spam.sendRaw_as_spam('NICK turtlerino', all_sockets)

        while True:
            for all_sockets in spam.sockets():
                time.sleep(1)
                data = all_sockets.recv(2048).decode('utf -8')  # keeps sockets alive
                if "PING" in data:  # keeps sockets alive
                    time.sleep(1)
                    all_sockets.send(bytes('PONG tmi.twitch.tv\r\n', 'utf-8'))  # keeps sockets alive

    except Exception as e:
        print(e)


def spam_connect():
    thread_twitch = threading.Thread(target=connect_and_login_and_keep_spam_alive)
    thread_twitch.start()


spam_connect()


def hexcode(colortuple):
    return '#' + ''.join(f'{i:02X}' for i in colortuple)


def r_g_b():
    (r, g, b) = colorsys.hsv_to_rgb(number, 1.0, 1.0)  # first argument is the hue(from 0.0 to 1.0)
    R, G, B = int(255 * r), int(255 * g), int(255 * b)
    return R,G,B


number = 0.1


def rainbow(answer,channel,slashme):
    global number
    if answer == "On":
        sendcommand("/color " + hexcode(r_g_b()), channel)
        number += 0.1
    else:
        if answer == "Off":
            pass


def custom_commands(message, channel, slash_me,color_each_msg):
    with open("commands.json") as custom_commands_file:
        custom_cmd = json.load(custom_commands_file)
    send(custom_cmd[message], channel, slash_me,color_each_msg)  # parses the command and sends it to chat


def commands(message, channel,slash_me,color_each_msg):
    def pyramid(rows, msg):
        try:
            i = rows
            if len(msg * (i + 1)) >= 500:
                print("maximum is 500 characters")
            else:
                for i in range(0, rows - 1):
                    first_half = msg * (i + 1)  # first half
                    send(first_half, channel,slash_me,color_each_msg)
                for i in range(rows + 1, 0, -1):
                    second_half = msg * (i - 1)  # second half
                    send(second_half, channel,slash_me,color_each_msg)
        except Exception:
            pass

    if "pyramid" in message:
        number = message.split(" ")
        emote = message.split(" ")
        emote = " ".join(emote[2:])
        try:
            pyramid(int(number[1]), " " + emote + " ")
        except:
            pass
