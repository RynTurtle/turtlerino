import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg 
import PyQt5.QtCore as qtc
import sys
import requests 
import gui.settings as settings_window 
import gui.viewerlist as viewerlist 
import json 
import os 
from twitch.handle_commands import parse_command  
from twitch.handle_messages import handle
from twitch.premade_commands import premade_commands
from twitch.irc.connect_socket import connect,connections_needed,socket_list
from twitch.ratelimit import check_queue
from twitch.irc.send_message import sendRaw,join,part
from functions.rainbow import hsv_to_hex,change_user_rainbow_colour
from settings.update_settings import add_key_value


chat_box_colour =   """ 
                    background-color: #1F1F1F; 
                    border: 1px solid black; 
                    color: white;
                   
                    """
background_colour = "background-color: #212121; color: white;"

class main_window(qtw.QMainWindow):
    
    def __init__(self):
        super().__init__()
        with open("settings/settings.json","r+") as settings:
            load_data = json.load(settings)
            self.rainbow_timer = load_data['settings']['user_rainbow_settings']['rainbow_timer']  

        widget = qtw.QWidget(self)
        self.setCentralWidget(widget)

        self.setWindowTitle("Turtlerino")
        self.resize(650,650)
        self.setWindowIcon(qtg.QIcon("static/icon.ico"))
        self.setStyleSheet(background_colour)


        top_bar = qtw.QHBoxLayout()  # horizontally place top bar widgets 

        self.channel_textbox = qtw.QLineEdit()
        self.ratelimit_box = qtw.QLineEdit() 

        # create buttons 
        viewer_list_button = qtw.QPushButton()
        settings_button = qtw.QPushButton()
        # edit widgets 
        self.channel_textbox.setFixedWidth(150)
        self.channel_textbox.setPlaceholderText("channel") 

        settings_button.setFixedWidth(32)
        viewer_list_button.setFixedWidth(32)
        settings_button.setIcon(qtg.QIcon("static/settings.png"))
        viewer_list_button.setIcon(qtg.QIcon("static/viewerlist.png"))

        # connect buttons to functions
        settings_button.clicked.connect(self.show_settings_window)
        viewer_list_button.clicked.connect(self.show_viewerlist_window)

        # add buttons to the horizontal layout 
        top_bar.addWidget(self.channel_textbox)
        top_bar.addWidget(self.ratelimit_box)
        top_bar.addWidget(qtw.QLabel("ms"),alignment=qtc.Qt.AlignLeft)
        top_bar.addWidget(settings_button,alignment=qtc.Qt.AlignRight)
        top_bar.addWidget(viewer_list_button)
        
        main_layout = qtw.QGridLayout() # verticle layout to place chat window and message box ontop of eachother 
        widget.setLayout(main_layout)

        main_layout.addLayout(top_bar,0,0) 
        


        checkbox_grid_layout = qtw.QGridLayout()

        main_layout.addLayout(checkbox_grid_layout,1,0)
        with open("settings/settings.json","r+") as settings:
            self.load_data = json.load(settings)      
            self.checkboxes_from_file = list(self.load_data['settings']['gui']['checkboxes'].keys())
            self.checkbox_values = list(self.load_data['settings']['gui']['checkboxes'].values())
    
        row = 0 
        column = 1 
        self.all_checkboxes = {} 
        for i in range(len(self.checkboxes_from_file)):
            if row == 5:  # i want it to be 10 wide 
                row = 0 
                column += 1  
            row += 1 

            create_checkbox = qtw.QCheckBox()
            self.all_checkboxes.update({create_checkbox:self.checkboxes_from_file[i]}) # appends a dictionary of checkboxname:checkboxobject
            create_checkbox.setText(self.checkboxes_from_file[i])
            create_checkbox.stateChanged.connect(self.checked)
            
            # reads file when window is opened, if its true or false on the file then check/uncheck the button
            if self.checkbox_values[i] == "True":
                create_checkbox.setChecked(True)
            else:
                create_checkbox.setChecked(False)
                
            checkbox_grid_layout.addWidget(create_checkbox,column,row,alignment=qtc.Qt.AlignTop) # alignment pushes all the widget right to the top       


        self.send_message_box = qtw.QTextEdit()  
        self.send_message_box.setStyleSheet(chat_box_colour)
        self.send_message_box.setFixedHeight(40)
        self.send_message_box.installEventFilter(self)
    
        self.ratelimit_box.setPlaceholderText("ratelimit") 
        self.ratelimit_box.returnPressed.connect(self.ratelimit_request)
        self.ratelimit_box.setFixedWidth(100)

        main_layout.addWidget(self.send_message_box,2,0)

        self.timer = qtc.QTimer()
        self.colour_timer = qtc.QTimer()
        self.connect_all_timer = qtc.QTimer()

        self.timer.timeout.connect(self.read_messages)
        self.colour_timer.timeout.connect(self.rainbow_change_timer)
        self.connect_all_timer.timeout.connect(self.connect_needed_amount)
        

        self.colour_timer.start(int(self.rainbow_timer) * 1000)
        self.connect_all_timer.start(3000) # every 3secs open a new connection until it hits the limit 
        self.timer.start(3)
        

        self.rate_limit_entered = 1200 # starts at 1 second ratelimit
        self.ctrl_held_state = False
        self.joined_channels = []

    def connect_needed_amount(self):
        with open("settings/settings.json","r+") as settings:
            load_data = json.load(settings)
            self.oauth = load_data['settings']['account_information']['oauth']
        
        if len(self.oauth) > 5: # if theres an oauth inside the file
            if len(socket_list()) < connections_needed(): #then connect
                connect()    

    def read_messages(self):
        check_queue(self.rate_limit_entered)
        try:
            for sockets in socket_list():
                data = sockets.recv(4096)
                decoded_data = data.decode("utf-8").split("\r\n")
                if "PING :tmi.twitch.tv" in decoded_data[0]:
                    print("PONG")
                    sockets.send(bytes('PONG :tmi.twitch.tv' + '\r\n', 'utf-8'))
       
        except BlockingIOError:
            pass 

        except ConnectionResetError:
            sockets.close()
            socket_list().remove(sockets)


    def rainbow_change_timer(self):
        with open("settings/settings.json","r+") as settings:
            load_data = json.load(settings)      
            self.rainbow_timer = load_data['settings']['user_rainbow_settings']['rainbow_timer'] 
            checkboxes = load_data['settings']['gui']['checkboxes'] 
            if checkboxes["rainbow timer"] == "True":
                change_user_rainbow_colour(self.channel_textbox.text())

            self.colour_timer.start(int(self.rainbow_timer) * 1000)


    def ratelimit_request(self):
        box_text = self.ratelimit_box.text()
        try:
            if box_text != "" or box_text != " ":
                self.rate_limit_entered = int(box_text) # if a new number is entered then change the original limit
        except:
            self.rate_limit_entered = 1200 # if it wasnt a number then use original 1sec limit
   

    def checked(self):
        for checkbox_names in list(self.all_checkboxes.keys()):
            find_checkbox_name = self.all_checkboxes[checkbox_names]     
            if checkbox_names.isChecked():
                add_key_value("checkboxes",find_checkbox_name,"True")
                #handle each chekbox with find_checkbox_newstate
            else: 
                add_key_value("checkboxes",find_checkbox_name,"False")


    def eventFilter(self,obj,event):
        if obj is self.send_message_box and event.type() == qtc.QEvent.KeyPress: # only checks kepresses within the chatbox
            if event.key() == qtc.Qt.Key_Control:
                self.ctrl_held_state = True 

            if event.key() == qtc.Qt.Key_Return and self.ctrl_held_state is True or event.key() == qtc.Qt.Key_Enter and self.ctrl_held_state is True: 
                self.send_request() 
                return True  # instead of having the carriage return 

            elif event.key() == qtc.Qt.Key_Return or event.key() == qtc.Qt.Key_Enter:
                self.send_request()  
                self.send_message_box.clear()
                return True
        return super(main_window,self).eventFilter(obj,event)


    def keyReleaseEvent(self,event):
        if event.key() == qtc.Qt.Key_Control:
            self.ctrl_held_state = False

    def send_request(self):  
        if len(self.oauth) > 5:
            try:
                textbox_messages = self.send_message_box.toPlainText()
                if textbox_messages != "" or textbox_messages != " ":
                    with open("settings/settings.json","r+") as settings:
                        load_data = json.load(settings) 
                        commands_list = list(load_data['settings']['commands'].keys())
                        commands_list_premade = list(load_data['settings']['premade_commands'].keys())
                        command = textbox_messages.split()[0] 
                        if command in commands_list:
                            handle(parse_command(command,textbox_messages),self.channel_textbox.text()) 
                        elif command in commands_list_premade:
                            premade_commands(command,textbox_messages,self.channel_textbox.text())
                        else:
                            handle(textbox_messages,self.channel_textbox.text()) 

            except IndexError:
                pass

        else:
            print("oauth not specified")

    def show_settings_window(self):
        self.window = settings_window.settings_window()
        self.window.show()


    def show_viewerlist_window(self):
        self.window = viewerlist.viewerlist_window()
        self.window.show()
        self.window.display_viewerlist(self.channel_textbox.text()) 
