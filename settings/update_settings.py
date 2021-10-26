import json 


def add_key_value(category,new_key,new_value):
    with open("settings/settings.json","r+") as settings:
        load_data = json.load(settings)  

        if category == "checkboxes":
            parsed_data = load_data['settings']['gui']['checkboxes']
        elif category == "sliders":
            parsed_data = load_data['settings']['gui']['sliders']
        elif category == "window_settings":
            parsed_data = load_data['settings']['gui']['window_settings']
        elif category == "commands":
            parsed_data = load_data['settings']['commands']


        titles = list(parsed_data.keys())
        if new_key not in titles: # if it doesnt already exist
            parsed_data.update({new_key:new_value})
        else:
            parsed_data[new_key] = new_value

        settings.seek(0)
        settings.truncate() # remove old content 
        rewrite_file = json.dump(load_data,settings,indent=4) # rewrite the file with the new data

    