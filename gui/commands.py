import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg 
from PyQt5.QtCore import Qt
import json
from settings.update_settings import add_key_value

background_colour = "QWidget {background-color: #212121; color: white;} QHeaderView::section { background-color: #212121; } QTableWidget QTableCornerButton::section {background-color: #212121; }"

# i mixed up the meaning of trigger when writing this 🤦🏼‍
class commands_window(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = qtw.QGridLayout()

        self.setLayout(self.layout)
        self.table = qtw.QTableWidget()

        self.layout.addWidget(self.table,0,0)
        

        self.setWindowIcon(qtg.QIcon("static/commands.png"))
        self.setStyleSheet(background_colour)
        self.setWindowTitle("Commands")
        self.resize(500,500)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        
        self.table.setColumnCount(2)
        self.table.setRowCount(len(self.commands_list()))

        self.table.setHorizontalHeaderLabels(["Command name","message to be sent"])
        self.table.horizontalHeader().setSectionResizeMode(1,qtw.QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1,qtw.QHeaderView.Stretch)
        self.table.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)


        # create table 
        row = 0
        for commands in self.commands_list():
            command_in_table = self.table.setItem(row,0,qtw.QTableWidgetItem(commands))
            trigger_in_table = self.table.setItem(row,1,qtw.QTableWidgetItem(self.commands_list()[commands]))
            row+= 1 

        self.table.resizeRowsToContents()

        command_name_title = qtw.QLabel("new or previous command name")
        command_trigger_title = qtw.QLabel("new message (can be pastebin links and can contain * for a newline)")
        delete_command_title = qtw.QLabel("remove command")

        self.character_counter_label = qtw.QLabel()
        self.command_name_textbox = qtw.QLineEdit()
        self.command_trigger_textbox = qtw.QLineEdit()

        self.delete_command_textbox = qtw.QLineEdit()

        self.command_trigger_textbox.textChanged.connect(self.character_counter)

        self.layout.addWidget(command_name_title,1,0)
        self.layout.addWidget(self.command_name_textbox,2,0)
        self.layout.addWidget(command_trigger_title,3,0)
        self.layout.addWidget(self.character_counter_label,4,0)
        self.layout.addWidget(self.command_trigger_textbox,5,0)
        self.layout.addWidget(delete_command_title,6,0)
        self.layout.addWidget(self.delete_command_textbox,7,0)


        self.command_trigger_textbox.returnPressed.connect(self.write_custom_command) 
        
        self.delete_command_textbox.returnPressed.connect(self.delete_command)

    def character_counter(self): # doesnt detect mouse double click highlight + type a word (need to bind on mouse double click event)
        self.count_characters = len(self.command_trigger_textbox.text())

        if len(self.command_trigger_textbox.text().split()) > 1:
            if "*" in self.command_trigger_textbox.text().split()[-1]: # checks if user writes * 
                self.count_characters = 0 
                
        if self.count_characters > 499:
            self.character_counter_label.setStyleSheet("color: red;")
        elif self.count_characters < 499:
            self.character_counter_label.setStyleSheet("color: white;")

        self.character_counter_label.setText(f"{str(self.count_characters)} (500 character twitch limit)")

    def commands_list(self):
        with open("settings/settings.json","r+") as self.settings:
            load_data = json.load(self.settings) 
            return load_data['settings']['commands']
    

    def add_to_table(self,command,command_trigger):
        row_count = self.table.rowCount()
        if command not in list(self.commands_list().keys()): # if the command  writing to the table isnt already in the file

            self.table.insertRow(row_count)
            self.table.setItem(row_count,0,qtw.QTableWidgetItem(command))
            self.table.setItem(row_count,1,qtw.QTableWidgetItem(command_trigger))

        else:
            row_count -= 1 # if the command is already specified then go back one row and set the trigger again
            self.table.setItem(row_count,1,qtw.QTableWidgetItem(command_trigger))


    def remove_table_item(self,command_name):
        for i in range(self.table.rowCount()):
            find_command = self.table.item(i,0)
            if find_command is not None:
                if find_command.text() == command_name: # goes through every command to find where in the table the command is located
                    self.table.removeRow(i)
                
    def delete_command(self):
        command_to_delete = self.delete_command_textbox.text()
        if command_to_delete != "":
            if command_to_delete in self.commands_list():
                with open("settings/settings.json","r+") as settings:
                    load_data = json.load(settings)  
                    current_commands = load_data['settings']['commands']
                    remove_unwanted_command = current_commands.pop(command_to_delete,None)
                
                    settings.seek(0)
                    settings.truncate() # remove old content 
                    rewrite_file = json.dump(load_data,settings,indent=4) # rewrite the file with the new data
                
                self.remove_table_item(command_to_delete)
            
    def write_custom_command(self):
        new_command = self.command_name_textbox.text()
        new_trigger = self.command_trigger_textbox.text()
        if new_trigger != "" and new_trigger != " " and new_command != "" and new_command != " ": # needs to have something in both boxes
            self.add_to_table(new_command,new_trigger)
            add_key_value("commands",new_command,new_trigger)

            