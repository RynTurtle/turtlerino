
import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg 
import PyQt5.QtCore as qtc
from functions.rainbow import hsv_to_hex
import json 

colour =  "#212121"
original_colour = f"background-color: {colour}; color: white;"
# todo add a decrease value aswell, so you can go back through colours and forwords through them (e,g a breathing effect on your username)

class rainbow_window(qtw.QWidget):
    def __init__(self):
        super().__init__()

        with open("settings/settings.json","r+") as settings:
            load_data = json.load(settings)      
            checkboxes = load_data['settings']['gui']['checkboxes']
            self.rainbow_timer = load_data['settings']['user_rainbow_settings']['rainbow_timer']  

        self.main_layout = qtw.QGridLayout()

        self.setLayout(self.main_layout)
        self.setWindowTitle("rainbow settings")
        self.resize(800,400)
        self.setWindowIcon(qtg.QIcon("static/rainbow.png"))

        self.setStyleSheet(original_colour)
        self.colour_checkbox = qtw.QCheckBox()
        self.colour_checkbox.setText("Amount of seconds to change username colour")
        self.main_layout.addWidget(self.colour_checkbox,0,0)


        # sliders 
        self.amount_of_time = qtw.QSlider(qtc.Qt.Horizontal)
        self.hue_slider = qtw.QSlider(qtc.Qt.Horizontal)
        self.saturation_slider = qtw.QSlider(qtc.Qt.Horizontal)
        self.light_slider = qtw.QSlider(qtc.Qt.Horizontal)


        self.amount_of_time.setTickInterval(101)
        self.hue_slider.setTickInterval(101)
        self.saturation_slider.setTickInterval(101)
        self.light_slider.setTickInterval(101)

        self.amount_of_time.setSingleStep(1)
        self.hue_slider.setSingleStep(1)
        self.saturation_slider.setSingleStep(1)
        self.light_slider.setSingleStep(1)

        self.amount_of_time.setValue(self.rainbow_timer)
        self.amount_of_time.setMinimum(1)



        self.hue_increment = qtw.QLineEdit()
        self.hue_decrease = qtw.QLineEdit()

        self.saturation_increment = qtw.QLineEdit()
        self.lightness_increment = qtw.QLineEdit()
        
        self.hue_increment.setPlaceholderText("increase:")
        self.hue_decrease.setPlaceholderText("decrease:")

        self.saturation_increment.setPlaceholderText("increase:")
        self.lightness_increment.setPlaceholderText("increase:")


        # buttons 
        
        self.hue = ["Set start hue","Set end hue"]
        self.saturation = ["Set start saturation","Set end saturation"]
        self.lightness = ["Set start lightness","Set end lightness"]


        #add widgets 
        self.main_layout.addWidget(qtw.QLabel("How frequently you want your colour changed"),0,0)
        self.time_value = qtw.QLabel(f"{str(self.amount_of_time.value())} seconds")
        self.main_layout.addWidget(self.time_value,1,1)
        self.main_layout.addWidget(self.amount_of_time,1,0)
        
        self.main_layout.addWidget(qtw.QLabel("Hue (another word for colour) "),2,0)
        self.hue_value = qtw.QLabel(str(self.hue_slider.value()))
        self.main_layout.addWidget(self.hue_value,3,1)
        self.main_layout.addWidget(self.hue_slider,3,0)

        rows = 1 
        for values in self.hue:
            rows += 1
            hue_pushbuttons = qtw.QPushButton()
            hue_pushbuttons.setText(values)
            hue_pushbuttons.clicked.connect(lambda state, button_names=values: self.manage_hue(button_names))
            self.main_layout.addWidget(hue_pushbuttons,3,rows)
            
        self.main_layout.addWidget(self.hue_increment,3,4)
        self.main_layout.addWidget(self.hue_decrease,3,5)

        self.hue_increment.returnPressed.connect(lambda:self.manage_hue("increment"))
        self.hue_decrease.returnPressed.connect(lambda:self.manage_hue("decrease"))

        self.main_layout.addWidget(qtw.QLabel("Saturation (the intensity or purity of a hue)"),4,0)
        self.saturation_value = qtw.QLabel(str(self.saturation_slider.value()))
        self.main_layout.addWidget(self.saturation_value,5,1)
        self.main_layout.addWidget(self.saturation_slider,5,0)


        rows = 1 
        for values in self.saturation:
            rows += 1
            saturation_pushbuttons = qtw.QPushButton()
            saturation_pushbuttons.setText(values)
            saturation_pushbuttons.clicked.connect(lambda state, button_names=values: self.manage_saturation(button_names))
            self.main_layout.addWidget(saturation_pushbuttons,5,rows)

            
        self.main_layout.addWidget(self.saturation_increment,5,4)
        self.saturation_increment.returnPressed.connect(lambda:self.manage_hue("increment"))
    

        self.main_layout.addWidget(qtw.QLabel("Lightness (the relative degree of black or white mixed with a given hue)"),6,0)
        self.light_value = qtw.QLabel(str(self.light_slider.value()))
        self.main_layout.addWidget(self.light_value,7,1)
        self.main_layout.addWidget(self.light_slider,7,0)


        rows = 1 
        for values in self.lightness:
            rows += 1
            lightness_pushbuttons = qtw.QPushButton()
            lightness_pushbuttons.setText(values)
            lightness_pushbuttons.clicked.connect(lambda state, button_names=values: self.manage_lightness(button_names))
            self.main_layout.addWidget(lightness_pushbuttons,7,rows)
        

        self.main_layout.addWidget(self.lightness_increment,7,4)
        self.lightness_increment.returnPressed.connect(lambda:self.manage_hue("increment"))
            

        self.amount_of_time.valueChanged.connect(self.amount_of_time_slider_changed)
        self.hue_slider.valueChanged.connect(self.hue_slider_changed)
        self.saturation_slider.valueChanged.connect(self.saturation_slider_changed)
        self.light_slider.valueChanged.connect(self.light_slider_changed)


        self.h = 0
        self.s = 0
        self.l = 0    


    def amount_of_time_slider_changed(self):
        self.time = self.amount_of_time.value()
        self.time_value.setText(f"{str(self.time)} seconds")
        with open("settings/settings.json","r+") as settings:
            load_settings = json.load(settings)
            load_settings['settings']['user_rainbow_settings']['rainbow_timer'] = self.time 

            settings.seek(0)
            settings.truncate() # remove old content 
            rewrite_file = json.dump(load_settings,settings,indent=4)



    def hue_slider_changed(self):
        self.h = self.hue_slider.value()
        self.hue_value.setText(str(self.h))
        colour = hsv_to_hex(self.h,self.s,self.l)
        self.setStyleSheet(f"background-color: {colour}; color: white;")


    def saturation_slider_changed(self):
        self.s = self.saturation_slider.value()
        self.saturation_value.setText(str(self.s))

        colour = hsv_to_hex(self.h,self.s,self.l)
        self.setStyleSheet(f"background-color: {colour}; color: white;")


    def light_slider_changed(self):
        self.l = self.light_slider.value()
        self.light_value.setText(str(self.l))
        colour = hsv_to_hex(self.h,self.s,self.l)
        self.setStyleSheet(f"background-color: {colour}; color: white;")


    def time_slider_position(self):
        return self.amount_of_time.value()

    def custom_background_colour(self):
        return hsv_to_hex(self.h,self.s,self.l)



    def manage_hue(self,button_name): 
        with open("settings/settings.json","r+") as settings:
            load_data = json.load(settings)      
            colour_settings = load_data['settings']['user_rainbow_settings']

            if "start" in button_name:
                colour_settings["rainbow_hue_start"] = self.h

            if "end" in button_name:
                colour_settings["rainbow_hue_end"] = self.h

            if "increment" in button_name:
                try:
                    colour_settings["rainbow_hue_increment"] = int(self.hue_increment.text())
                except:
                    pass

            if "decrease" in button_name:
                try:
                    colour_settings["rainbow_hue_decrease"] = int(self.hue_decrease.text())
                except:
                    pass


            settings.seek(0)
            settings.truncate() # remove old content 
            rewrite_file = json.dump(load_data,settings,indent=4)


    
    def manage_saturation(self,button_name): 
        with open("settings/settings.json","r+") as settings:
            load_data = json.load(settings)      
            colour_settings = load_data['settings']['user_rainbow_settings']

            if "start" in button_name:
                colour_settings["rainbow_saturation_start"] = self.s

            if "end" in button_name:
                colour_settings["rainbow_saturation_end"] = self.s

            if "increment" in button_name:
                try:
                    colour_settings["rainbow_saturation_increment"] = int(self.hue_increment.text())
                except:
                    pass

            settings.seek(0)
            settings.truncate() 
            rewrite_file = json.dump(load_data,settings,indent=4)



    def manage_lightness(self,button_name): 
        with open("settings/settings.json","r+") as settings:
            load_data = json.load(settings)      
            colour_settings = load_data['settings']['user_rainbow_settings']

            if "start" in button_name:
                colour_settings["rainbow_lightness_start"] = self.l

            if "end" in button_name:
                colour_settings["rainbow_lightness_end"] = self.l

            if "increment" in button_name:
                try:
                    colour_settings["rainbow_lightness_increment"] = int(self.hue_increment.text())
                except:
                    pass

            settings.seek(0)
            settings.truncate() 
            rewrite_file = json.dump(load_data,settings,indent=4)

