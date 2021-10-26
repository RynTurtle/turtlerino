# this is where we get the messages that is wanting to be sent to chat and edit it based on the checkboxes and ratelimits 
from twitch.handle_checkboxes import handle_boxes
from twitch.ratelimit import add_to_limit_queue
from functions.rainbow import change_user_rainbow_colour
import json 

alternate_number = 0 
def handle(messages,channel):
    global alternate_number
    with open("settings/settings.json","r+") as settings:
        load_data = json.load(settings)      
        checkboxes = load_data['settings']['gui']['checkboxes']

        if alternate_number % 2 != 0: # if its odd
            messages + " ⠀" # add the alternating invisible character
        alternate_number += 1 

        if "*" in messages:
            for every_line in messages.split("*"):
                if "{RAINBOW}" in every_line:
                    add_to_limit_queue(change_user_rainbow_colour(),channel)
                    add_to_limit_queue(handle_boxes(every_line.replace("{RAINBOW}","")),channel)  
                else:
                    add_to_limit_queue(handle_boxes(every_line),channel) 
        else:
            if checkboxes["rainbow per message"] == "True": 
                add_to_limit_queue(change_user_rainbow_colour(),channel)

            elif "{RAINBOW}" in messages: 
                add_to_limit_queue(change_user_rainbow_colour(),channel)

            add_to_limit_queue(handle_boxes(messages.replace("{RAINBOW}","")),channel) # add the alternating invisible character

 