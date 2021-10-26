
from twitch.handle_messages import handle

def premade_commands(command_name,message,channel):
    if command_name == "/pyramid":
        try:
            rows = int(message.split()[1])
            msg = " ".join(message.split()[2:]) + " "
            if len(rows * msg.replace(" ","r")) < 501: # .replace is used for len() to calculate the space
                for i in range(0, rows - 1):
                    first_half = msg * (i + 1)  # first half
                    handle(first_half,channel)

                for i in range(rows + 1, 0, -1):
                    second_half = msg * (i - 1)  # second half
                    handle(second_half,channel)

            else:
                print("pyramid is too large (500 character twitch limit)")
        except:
            print("correct usage: /pyramid number emote")




