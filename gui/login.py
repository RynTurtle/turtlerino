
import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg 
from PyQt5.QtCore import Qt
import json 

background_colour = "background-color: #212121; color: white;"

class login_window(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.verticle_layout = qtw.QVBoxLayout()
        self.setLayout(self.verticle_layout)
        self.setWindowTitle("login")
        self.resize(470,70)
        self.setFixedSize(self.size())
        self.setWindowIcon(qtg.QIcon("static/wrench.png"))
        self.setStyleSheet(background_colour)

        self.horizontal_layout = qtw.QHBoxLayout()

        self.oauth_title = qtw.QLabel('<a href="https://twitchapps.com/tmi/" style="color:green"> Click this link to get the oauth token needed to send messages in chat (do not show anyone)</a>')
        self.oauth_title.setOpenExternalLinks(True)
        self.verticle_layout.addWidget(self.oauth_title, alignment=Qt.AlignTop)

        self.oauth_input_box = qtw.QLineEdit()
        self.oauth_input_box.returnPressed.connect(self.write_oauth)
        self.verticle_layout.addWidget(self.oauth_input_box)


    def write_oauth(self):
        oauth_box = self.oauth_input_box.text()
        if "oauth:" in oauth_box:
            oauth = oauth_box.split("oauth:")[1]
        else:
            oauth = oauth_box      
        
        with open("settings/settings.json","r+") as settings:
            load_data = json.load(settings)  
            load_data['settings']['account_information']['oauth'] = oauth

            settings.seek(0)
            settings.truncate() # remove old content 
            rewrite_file = json.dump(load_data,settings,indent=4) # rewrite the file with the new data

        

