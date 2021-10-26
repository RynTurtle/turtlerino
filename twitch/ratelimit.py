# plebs - 20 per 30 seconds   1200ms
# broadcaster,mods,vips - 100 per 30 seconds 100ms
# verified bots - 7500 per 30 seconds  
import datetime
from twitch.irc.send_message import sendRaw

    
last_check = datetime.datetime.now()

message_queue = []


def check_queue(ratelimit):
    global last_check
    now = datetime.datetime.now()
    difference = now - last_check
    difference_milliseconds = int(difference.total_seconds() * 1000)
    quantity = int(difference_milliseconds / ratelimit) 
    
    if quantity > 0:
        for i in range(quantity): # for all the messages that need to be sent 
            if len(message_queue) == 0:
                break
            else:
                try:
                    find_message = list(message_queue[i].keys())[0]
                    find_channel = list(message_queue[i].values())[0]
                    if len(find_message) > 500:
                        print("message too long (500 character limit)")
                        message_queue.remove({str(find_message):str(find_channel)})
                    else:
                        # send to twitch
                        sendRaw(find_message,find_channel)
                        message_queue.remove({str(find_message):str(find_channel)})
                except IndexError as e: 
                    pass 

        last_check = datetime.datetime.now() 



def add_to_limit_queue(message,channel):
    message_queue.append({message:channel})
