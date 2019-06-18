from PyQt5 import QtWidgets, QtCore
import time
from combiner import *
from GLSLInstance import GLSLInstance
from GLWindow import GLWindow
import pickle

#Dictionary to store customizable parameters for each shader
shader_dict = {
    "Aesthetic" :
    ['resolutionX_Aesthetic', 'resolutionY_Aesthetic', 'xZoom_Aesthetic', 'yZoom_Aesthetic', 'rate_Aesthetic', 'strength_Aesthetic'],
    "Cryptid" :
    ['resolutionX_Cryptid', 'resolutionY_Cryptid', 'strength_Cryptid'],
    "Cube" :
    ['resolutionX_Cube', 'resolutionY_Cube', 'rate_Cube', 'strength_Cube'],
    "CubeField" :
    ['resolutionX_CubeField', 'resolutionY_CubeField', 'rate_CubeField', 'strength_CubeField'],
	"Kaleidoscope" :
	["resolutionX_Kaleidoscope", "resolutionY_Kaleidoscope"],
    "Eyeball" :
    ['resolutionX_Eyeball', 'resolutionY_Eyeball', 'eyeX_Eyeball', 'eyeY_Eyeball', 'strength_Eyeball'],
    "FeverDream" :
    ['resolutionX_FeverDream', 'resolutionY_FeverDream', 'speed_FeverDream', 'zoom_FeverDream', 'fieldStrength_FeverDream', 'cloud_FeverDream', 'transverseSpeed_FeverDream', 'strength_FeverDream'],
    "Galaxy" :
    ['resolutionX_Galaxy', 'resolutionY_Galaxy', 'posX_Galaxy', 'posY_Galaxy', 'freq1_Galaxy', 'freq2_Galaxy', 'freq3_Galaxy', 'strength_Galaxy'],
    "Lagoon" :
    ['resolutionX_Lagoon', 'resolutionY_Lagoon', 'rate1_Lagoon', 'rate2_Lagoon', 'rate3_Lagoon', 'rate4_Lagoon', 'rate5_Lagoon', 'strength_Lagoon'],
    "Skull" :
    ['resolutionX_Skull', 'resolutionY_Skull', 'chinWidth_Skull', 'faceStrength_Skull', 'nostril_Skull', 'rotateRate_Skull', 'bloom_Skull', 'zoomRate_Skull'],
    "Synapse" :
    ['resolutionX_Synapse', 'resolutionY_Synapse', 'posX_Synapse', 'posY_Synapse', 'strength_Synapse'],
}

# add Leap attributes here to display in selection menu (need accompanying function in combiner.py)
leap_mapping = ['None', 'Right_PalmX', 'Right_PalmY', 'Right_SphereX', 'Right_SphereY', 'Right_SphereR', 'Right_PalmRoll', 'Right_PalmPitch', 'Right_PalmYaw', 'Right_PalmVelX', 'Right_PalmVelY', 'Right_PalmVelZ', 'Left_PalmX', 'Left_PalmY', 'Left_SphereX', 'Left_SphereY', 'Left_SphereR', 'Left_PalmRoll', 'Left_PalmPitch', 'Left_PalmYaw', 'Left_PalmVelX', 'Left_PalmVelY', 'Left_PalmVelZ', 'Right_IndexDirX']


#Class to define the Desktop Application
class SelectionMenu(QtWidgets.QWidget):
    def __init__(self, parentLayout):
        super(SelectionMenu, self).__init__()

        self.combiner = Combiner()
        
        self.parentLayout = parentLayout
        
        self.shouldRun = True
        self.num_shader = 0
        self.shaders = ["None"]
        self.selected_shaders = []
        self.options_menus = []
        for key in shader_dict.keys():
            self.shaders.append(key)

        self.parentLayout.setRowStretch(0, 100)
        self.parentLayout.setRowStretch(1, 1)
        self.parentLayout.setRowStretch(2, 99)

        self.parentLayout.addWidget(QtWidgets.QLabel(), 3, 0)
        
        #Defining each button and which function is linked to it    
        self.add_shader_button = QtWidgets.QPushButton("Add Shader", self)
        self.add_shader_button.clicked.connect(self.add_shader)
            
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.add_shader_button, 0, 0)

        self.save_preset_button = QtWidgets.QPushButton("Save Preset")
        self.save_preset_button.clicked.connect(self.save_preset)
        self.layout.addWidget(self.save_preset_button, 0, 1)

        self.load_preset_button = QtWidgets.QPushButton("Load Preset")
        self.load_preset_button.clicked.connect(self.load_preset_file)
        self.layout.addWidget(self.load_preset_button, 0, 2)

        self.demo_button1 = QtWidgets.QPushButton("Demo Preset 1")
        self.demo_button1.clicked.connect(self.demo1)
        self.layout.addWidget(self.demo_button1, 0, 4)

        self.demo_button2 = QtWidgets.QPushButton("Demo Preset 2")
        self.demo_button2.clicked.connect(self.demo2)
        self.layout.addWidget(self.demo_button2, 0, 5)

        self.demo_button3 = QtWidgets.QPushButton("Demo Preset 3")
        self.demo_button3.clicked.connect(self.demo3)
        self.layout.addWidget(self.demo_button3, 0, 6)

        for col in range(7, 11):
            l = QtWidgets.QLabel()
            self.layout.addWidget(l, 0, col, 1, 2)

        self.quit_button = QtWidgets.QPushButton("Quit")
        self.quit_button.clicked.connect(self.quit)
        self.layout.addWidget(self.quit_button, 0, 11)

        self.add_shader()
        
        self.run_default()
 
 #Function that defines saving presets       
    def save_preset(self):
        preset = {}
        row = 1
        for menu in self.options_menus:
            shader_presets = {}
            selected_shader = menu.currentText()
            if selected_shader != "None":
                
                for col in range(1, self.layout.columnCount()):
                    labelItem = self.layout.itemAtPosition(row, col)
                    if labelItem is not None:
                        label = labelItem.widget().text() + "_" + selected_shader
                    leapMappingItem = self.layout.itemAtPosition(row + 1, col)
                    if leapMappingItem is not None:
                        leapMapping = leapMappingItem.widget().currentText()
                        
                    if labelItem is not None and leapMappingItem is not None and leapMapping != "None":
                        shader_presets[label] = leapMapping
                        
                preset[selected_shader] = shader_presets
            row += 2
        
        preset_file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save current configuration')
        with open(preset_file, 'wb') as f:
            pickle.dump(preset, f, pickle.HIGHEST_PROTOCOL)

    def quit(self):
        QtCore.QCoreApplication.instance().quit()
            
    def demo1(self):
        self.load_preset("Presets/demo1.pkl")
        
    def demo2(self):
        self.load_preset("Presets/demo2.pkl")
            
    def demo3(self):
        self.load_preset("Presets/demo3.pkl")

    def load_preset_file(self):
        preset_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose a preset to load')
        self.load_preset(preset_file)
    
    def load_preset(self, preset_file):        
        # clear existing stuff
        for row in range(1, 1 + 2*self.num_shader):
            for col in range(0, self.layout.columnCount()):
                widgetItem = self.layout.itemAtPosition(row, col)
                if widgetItem is not None:
                    widget = widgetItem.widget()
                    self.layout.removeWidget(widget)
                    widget.deleteLater()
        
        # reinitialize everything
        self.parentLayout.setRowStretch(1, 1)
        self.parentLayout.setRowStretch(2, 99)
        self.num_shader = 0
        self.shaders = ["None"] + [key for key in shader_dict.keys()]
        self.selected_shaders = []
        self.options_menus = []

        with open(preset_file, "rb") as f:
            preset = pickle.load(f)

            for (shader, mappings) in preset.items():
                self.add_shader()

                self.shouldRun = False
                self.options_menus[self.num_shader-1].setCurrentText(shader)
                self.shouldRun = True
                
                for col in range(1, self.layout.columnCount()):
                    widgetItem = self.layout.itemAtPosition(self.num_shader*2-1, col)
                    if widgetItem is not None:
                        widget = widgetItem.widget()
                        widgetParamName = widget.text() + "_" + shader
                        if widgetParamName in mappings:
                            leapMappingItem = self.layout.itemAtPosition(self.num_shader*2, col)
                            if leapMappingItem is not None:
                                leapMappingItem.widget().blockSignals(True)
                                leapMappingItem.widget().setCurrentText(mappings[widgetParamName])
                                leapMappingItem.widget().blockSignals(False)

        self.run_shader()

    def run_default(self):
        (glsl, fragShader, listener, attributes) = self.combiner.run(["Empty"], {})
        shader = GLWindow((1280, 720), "Shader")
        glsl.wnd = shader.wnd
        shader.lam = lambda: glsl(fragShader, listener, attributes)
        shaderItem = self.parentLayout.itemAtPosition(0, 0)
        if shaderItem is not None:
            w = shaderItem.widget()
            try:
                w.ex.controller.remove_listener(listener)
            except:
                pass
            self.parentLayout.removeWidget(w)
            w.deleteLater()
        self.parentLayout.addWidget(shader, 0, 0)
    #launches shader code once run button is clicked
    def run_shader(self):
        if self.shouldRun:
            shaders = []
            mappings = {}
            row = 1
            for menu in self.options_menus:
                selected_shader = menu.currentText()
                if selected_shader != "None":
                    shaders.append(selected_shader)
                    
                    for col in range(1, self.layout.columnCount()):
                        labelItem = self.layout.itemAtPosition(row, col)
                        if labelItem is not None:
                            label = labelItem.widget().text() + "_" + selected_shader
                        leapMappingItem = self.layout.itemAtPosition(row + 1, col)
                        if leapMappingItem is not None:
                            leapMapping = leapMappingItem.widget().currentText()
                            
                        if labelItem is not None and leapMappingItem is not None and leapMapping != "None":
                            mappings[label] = leapMapping
                            
                row += 2
            
            if shaders != []:
                (glsl, fragShader, listener, attributes) = self.combiner.run(shaders, mappings)
                # this is wack
                shader = GLWindow((1280, 720), "Shader")
                glsl.wnd = shader.wnd
                shader.lam = lambda: glsl(fragShader, listener, attributes)
                shaderItem = self.parentLayout.itemAtPosition(0, 0)
                if shaderItem is not None:
                    w = shaderItem.widget()
                    try:
                        w.ex.controller.remove_listener(listener)
                    except:
                        pass
                    self.parentLayout.removeWidget(w)
                    w.deleteLater()
                self.parentLayout.addWidget(shader, 0, 0)
            else:
                self.run_default()
        
    #function that checks the shader selected and updates parameters accordingly
    def update_selection(self, selected):
        self.selected_shaders = [menu.currentText() for menu in self.options_menus if menu.currentText() != "None"]
        
        row = 1
        for menu in self.options_menus:
            current_selection = menu.currentText()
            if current_selection == "None" or current_selection == selected:
                for col in range(1, self.layout.columnCount()):
                    widgetItem = self.layout.itemAtPosition(row, col)
                    if widgetItem is not None:
                        widget = widgetItem.widget()
                        self.layout.removeWidget(widget)
                        widget.deleteLater()
                    widgetItem = self.layout.itemAtPosition(row + 1, col)
                    if widgetItem is not None:
                        widget = widgetItem.widget()
                        self.layout.removeWidget(widget)
                        widget.deleteLater()
                if current_selection != "None":
                    col = 1
                    for param in shader_dict[current_selection]:
                        label = QtWidgets.QLabel()
                        label.setText(param.split("_")[0])
                        self.layout.addWidget(label, row, col)
                        
                        comboBox = QtWidgets.QComboBox()
                        for mapping in leap_mapping:
                            comboBox.addItem(mapping)
                        comboBox.currentIndexChanged.connect(self.update_mapping)
                        self.layout.addWidget(comboBox, row + 1, col)
                        
                        col += 1
                
            row += 2

        self.update_shaders()

    def update_mapping(self, idx):
        self.run_shader()
        
    def update_shaders(self):
        for menu in self.options_menus:
            selected = menu.currentText()

            menu.blockSignals(True)
            menu.clear()
            menu.addItems([shader for shader in self.shaders if shader not in self.selected_shaders or shader == selected])
            menu.setCurrentText(selected)
            menu.blockSignals(False)
        self.run_shader()

    def add_shader(self):
        self.num_shader += 1
    
        label = QtWidgets.QLabel()
        label.setText("Shader " + str(self.num_shader))

        self.layout.addWidget(label, 2*self.num_shader - 1, 0)
        
        #Loop that updates menu with ability to choose another shader
        comboBox = QtWidgets.QComboBox()
        for shader in [shader for shader in self.shaders if shader not in self.selected_shaders]:
            comboBox.addItem(shader)
        comboBox.currentIndexChanged[str].connect(self.update_selection)
        self.layout.addWidget(comboBox, 2*self.num_shader, 0)
        
        self.options_menus.append(comboBox)
              
        # try to counteract stretching upward
        self.parentLayout.setRowStretch(1, self.parentLayout.rowStretch(1) + 10)
        self.parentLayout.setRowStretch(2, self.parentLayout.rowStretch(2) - 10)
