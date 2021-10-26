import json 
import requests
def pastebin_content(message):
    url = "https://pastebin.com/"
    if url in message:
        for word in message.split(" "):
            if url in word:
                pastebin_link = word
                if "/raw/" not in pastebin_link:            
                    pastebin_id = pastebin_link.split("/")[3]
                    pastebin_raw_url = f"https://pastebin.com/raw/{pastebin_id}"
                else:
                    pastebin_raw_url = pastebin_link

                request_lines = requests.get(pastebin_raw_url)
                link_to_text = request_lines.text

                if not request_lines.status_code == 404:
                    return link_to_text.split("\r\n")

def parse_command(command_name,message): 
    with open("settings/settings.json","r+") as settings:
        load_data = json.load(settings)      
        parsed_data = load_data['settings']['commands']   
        checkboxes = load_data['settings']['gui']['checkboxes']
        command_trigger_response = parsed_data[command_name]        
        trigger_response = []

        for message_to_be_sent in command_trigger_response.split():
            if not pastebin_content(message_to_be_sent):
                trigger_response.append(message_to_be_sent)
            else:
                for lines in pastebin_content(message_to_be_sent): # if there are pastebin
                    trigger_response.append("*" + lines)  # append every line with a star to indicate newline 

        if checkboxes["rainbow per message"] == "True":
            for i in range(len(trigger_response)):
                trigger_response[i] = trigger_response[i].replace("*","*{RAINBOW}") # replace the newlines to newlines with the rainbow tag

        for i in range(len(trigger_response)):
            if "{" and "}" in trigger_response[i]:
                insert = trigger_response[i].split("}")[0].split("{")[1]
                if any(str.isdigit(c) for c in insert): # if insert is an integer {1}
                    if len(message.split()) > 1:
                        trigger_response[i] = message.split()[int(insert)]  # then replace the word related to the integer with what someone writes 
                    else:
                        trigger_response[i] = ""

        return " ".join(trigger_response)
