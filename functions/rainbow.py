#hsl and hsv (hue saturation lightness)
import colorsys 
import webcolors
from twitch.irc.connect_socket import socket_list
import json
def HsvToRgb(hue, saturation, value): 
    """
    Returns RGB colour tuple from HSV (Hue, Saturation, Value).
    """
    red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
    return (
        int(round(red * 255.0)),
        int(round(green * 255.0)),
        int(round(blue * 255.0))
    )



def hsv_to_hex(h,s,v):
    h = h / 100
    s = s / 100
    v = v  / 100
    # dived because colorsys is from 0 to 1 NOT from 0 to 255 
    hsv_to_rgb = HsvToRgb(h,s,v)
    return webcolors.rgb_to_hex(hsv_to_rgb)



with open("settings/settings.json","r+") as settings:
    load_data = json.load(settings)
    rainbow_timer = load_data['settings']['user_rainbow_settings']['rainbow_timer']  
    starting_hue = load_data['settings']['user_rainbow_settings']['rainbow_hue_start'] 
    starting_saturation = load_data['settings']['user_rainbow_settings']['rainbow_saturation_start'] 
    starting_lightness = load_data['settings']['user_rainbow_settings']['rainbow_lightness_start']  



h = starting_hue
s = starting_saturation
l = starting_lightness
forwards = True

def change_user_rainbow_colour():
    global h 
    global s 
    global l 
    global forwards 

    with open("settings/settings.json","r+") as settings:
        load_data = json.load(settings)      
        checkboxes = load_data['settings']['gui']['checkboxes']

        # goes from the start to end in increments someone chooses
        starting_hue = load_data['settings']['user_rainbow_settings']['rainbow_hue_start'] 
        starting_saturation = load_data['settings']['user_rainbow_settings']['rainbow_saturation_start'] 
        starting_lightness = load_data['settings']['user_rainbow_settings']['rainbow_lightness_start']  

        ending_hue = load_data['settings']['user_rainbow_settings']['rainbow_hue_end'] 
        ending_saturation = load_data['settings']['user_rainbow_settings']['rainbow_saturation_end'] 
        ending_lightness = load_data['settings']['user_rainbow_settings']['rainbow_lightness_end']  

        hue_increment = load_data['settings']['user_rainbow_settings']['rainbow_hue_increment'] 
        saturation_increment = load_data['settings']['user_rainbow_settings']['rainbow_saturation_increment'] 
        lightness_increment = load_data['settings']['user_rainbow_settings']['rainbow_lightness_increment']  


        hue_decrease = load_data['settings']['user_rainbow_settings']['rainbow_hue_decrease'] # when it hits the end then go back to the start  

            
        if len(socket_list()) > 1:                         
            if forwards is True:
                if h > ending_hue or h > 100:
                    forwards = False 

                if s > ending_saturation or s > 100:
                    s = starting_saturation

                if l > ending_saturation or l > 100:
                    l = starting_lightness

                h += hue_increment
                s += saturation_increment
                l += lightness_increment
                    
            else:
                if h < starting_hue:
                    forwards = True

                h -= hue_decrease


            return f"/color {hsv_to_hex(h,s,l)}"