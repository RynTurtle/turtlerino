
import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg 
import PyQt5.QtCore as qtc
import json 
from gui.commands import commands_window 
from gui.login import login_window 
from gui.rainbow_window import rainbow_window
background_colour = "background-color: #212121; color: white;"

class settings_window(qtw.QWidget):
    def __init__(self):
        super().__init__()
        global create_checkbox
        self.setWindowTitle("Settings")
        self.resize(650,100)
        self.setWindowIcon(qtg.QIcon("static/settings.png"))
        self.setStyleSheet(background_colour)

        verticle_layout = qtw.QVBoxLayout()

        commands_button = qtw.QPushButton("commands")
        commands_button.clicked.connect(self.show_commands)

        login_button = qtw.QPushButton("login")
        login_button.clicked.connect(self.show_login)

        rainbow_button = qtw.QPushButton("rainbow settings")
        rainbow_button.clicked.connect(self.show_rainbow)

        verticle_layout.addWidget(commands_button)
        verticle_layout.addWidget(login_button) 
        verticle_layout.addWidget(rainbow_button,alignment=qtc.Qt.AlignTop) 

        main_layout = qtw.QGridLayout()
        verticle_layout.addLayout(main_layout)   

        self.setLayout(verticle_layout)



    def show_commands(self):
        self.window = commands_window()
        self.window.show()

    def show_login(self):
        self.window = login_window()
        self.window.show()

    def show_rainbow(self):
        self.window = rainbow_window()
        self.window.show()
