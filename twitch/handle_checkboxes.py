from functions.pepege_capitilisation import pepege 
from functions.mrdestructoid_binary import mrdestructoid 
import json 
from functions.rainbow import change_user_rainbow_colour


def handle_boxes(message):
    with open("settings/settings.json","r+") as settings:
        load_data = json.load(settings)      
        checkboxes = load_data['settings']['gui']['checkboxes']
        new_message = []
        new_message.append(" " + message) # adds the original message to the list
        if checkboxes["/me"] == "True":
            new_message.insert(0,"/me")  # inserts /me to the beginning of every message

        
        if checkboxes["PePegE MoDe"] == "True": 
            return pepege("".join(new_message))
        elif checkboxes["MrDestructoid"] == "True": 
            return mrdestructoid("".join(new_message))
        else:
            return "".join(new_message)
            


