import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg 
import requests 
background_colour = "background-color: #212121; color: white;"

class viewerlist_window(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        self.setWindowTitle("Viewerlist")
        self.resize(325,650)
        self.setWindowIcon(qtg.QIcon("static/viewerlist.png"))
        self.setStyleSheet(background_colour)    

    def display_viewerlist(self,channel_name):
        viewerlist_request = requests.get(f"https://tmi.twitch.tv/group/user/{channel_name}/chatters")
        list_of_users = qtw.QListWidget()
        self.layout.addWidget(list_of_users) # add the one list widget to contain all users and titles
        if not viewerlist_request.status_code == 404:
            viewerlist_request = viewerlist_request.json()
            chatter_count = viewerlist_request['chatter_count']
            mod_count = len(viewerlist_request['chatters']['moderators'])
            vip_count = len(viewerlist_request['chatters']['vips'])
            
            list_of_users.addItem(f"Current people who have chat open:")
            list_of_users.addItem(f"Total Chatters: {chatter_count}")
            list_of_users.addItem(f"Mods: {mod_count}")
            list_of_users.addItem(f"Vips: {vip_count}")
        

            for each_viewer_type in viewerlist_request['chatters']:
                list_of_users.addItem("")
                list_of_users.addItem(each_viewer_type)
                for users in viewerlist_request['chatters'][each_viewer_type]:
                    list_of_users.addItem(users)

        else:
            list_of_users.addItem("Channel not found")