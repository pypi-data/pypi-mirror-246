#This is the file the package is run from. It is still being implemented. It currently interacts read_input_xml. 
#In future versions it will save user inputs as dictionary of xml_objects which will then be compiled using compile_xml.py
#Future versions will also work with Potts

import sys
import os
import xml.etree.ElementTree as ET

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QWidget,
    QMainWindow,
    QLabel,
    QComboBox,
    QPushButton,
    QLineEdit,
    QGroupBox,
    QToolBar,
    QMenu,
    QToolButton,
    QAction,
    QMessageBox
)

current_script_path = os.path.dirname(os.path.abspath(__file__))
relative_path_to_XMLObject = os.path.normpath(os.path.join(current_script_path, '../../src/'))
sys.path.append(relative_path_to_XMLObject)
from xml_object import XMLObject
from read_input_xml import ReadInputModuleSpecific
from read_input_xml import ReadInputFunctions

class Window(QMainWindow):
    #Storage of input xml
    xml_files_dictionary = {}
    selected_xml_parameter_file = {}
    parsed_parameter_dictionary = {}
    
    #Stores user inputs for population id so that 
    population_id_list = []
    layer_id_list = []

    #Used to store layout of population tab between additions of new populations
    population_tab_layout = None
    def __init__(self):
        super(Window, self).__init__()
        self.initGeneral() 
        self.initUI()

    def initGeneral(self):
        directories = ReadInputFunctions.list_directories()
        self.xml_files_dictionary = ReadInputFunctions.find_and_store_xml_files(directories, "parameter")
    
    def initUI(self):
        #This initial UI requests which parameter .xml file you wish to use
        self.setWindowTitle('ARCADE Parameter Setup')
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)

        # Dropdown menu
        self.label = QLabel('Please select which ARCADE module you wish to run:')
        self.layout.addWidget(self.label)
        xml_file_names_list = list(self.xml_files_dictionary.keys())
        xml_file_names_list.remove("parameter")
        self.dropdown = QComboBox(self)
        self.dropdown.addItems(xml_file_names_list)
        self.layout.addWidget(self.dropdown)

        # Switch button
        self.switch_button = QPushButton('Confirm', self)
        self.switch_button.clicked.connect(self.select_parameters_screen)
        self.layout.addWidget(self.switch_button)

    def select_parameters_screen(self):
        # This is the second screen. It displays options based on the selected parameter .xml file
        # Save the selected value
        self.selected_xml_parameter_file = self.dropdown.currentText()
        self.parsed_parameter_dictionary = ReadInputModuleSpecific.read_in_module(ReadInputModuleSpecific, self.selected_xml_parameter_file, self.xml_files_dictionary)
        # Clear the current layout
        self.clear_layout()
        
        # Resize
        self.resize(1470, 1010) 

        # Create the tab widget 
        ## Possibly should have if statement for patch/potts. Separate tab_ui functions
        widget = QWidget()
        layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.addTab(self.general_tab_ui(), "General")
        tabs.addTab(self.series_tab_ui(), "Series")
        tabs.addTab(self.module_specific_tab_ui(), "Module Specific")
        tabs.addTab(self.population_tab_ui(), "Populations")
        tabs.addTab(self.layer_tab_ui(), "Layers")
        tabs.addTab(self.action_tab_ui(), "Actions")
        tabs.addTab(self.components_tab_ui(), "Components")
        layout.addWidget(tabs)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setupToolbar()

    def clear_layout(self):
        # Clear the existing layout by removing all widgets
        # Used before switching screens and displaying a new UI
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
    def setupToolbar(self):
        # While the toolbar displays. The functionality is not implemented
        # Create a toolbar 
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)

        # Create "Run" button with a dropdown menu
        run_button = QToolButton(self)
        run_button.setText('Run')
        run_menu = QMenu(self)
        run_button.setMenu(run_menu)
        toolbar.addWidget(run_button)

        # Create "Commands" button with a dropdown menu
        commands_button = QToolButton(self)
        commands_button.setText('Commands')
        commands_menu = QMenu(self)
        commands_button.setMenu(commands_menu)
        toolbar.addWidget(commands_button)

        # Add actions to the menus
        run_action = QAction('Run Action', self)
        run_action.triggered.connect(self.run_command)
        run_menu.addAction(run_action)

        commands_action = QAction('Commands Action', self)
        commands_action.triggered.connect(self.show_commands)
        commands_menu.addAction(commands_action)

    def run_command(self):
        # NOT IMPLEMENTED
        return

    def show_commands(self):
        # NOT IMPLEMENTED
        commands_text = "Example List of available commands:\n\n1. Command A\n2. Command B\n3. Command C"
        QMessageBox.information(self, 'Available Commands', commands_text)
   
    def general_tab_ui(self):
        # Creates a tab for accessing general parameter values
        #Set up Container
        general_tab = QWidget()
        layout = QVBoxLayout()
        
        #Display parameters from xml
        for element in self.parsed_parameter_dictionary["default"]:
            nested_layout = QHBoxLayout()  # Create a new instance for each iteration
            for attribute_name, current_value in element.items():
                if attribute_name == "id" or attribute_name == "description":
                    label = QLabel(f'{attribute_name}: {current_value}')
                    nested_layout.addWidget(label)
                else:
                    label = QLabel(f'{attribute_name}: ')
                    nested_layout.addWidget(label)
                    
                    text_field = QLineEdit()
                    text_field.setText(current_value)
                    nested_layout.addWidget(text_field)
            
            layout.addLayout(nested_layout)

        #display everything
        general_tab.setLayout(layout)
        return general_tab
    def series_tab_ui(self):
        # Creates a tab for accessing series parameter values
        series_tab = QWidget()
        layout = QVBoxLayout()
        
        
                #Display parameters from xml
        for element in self.parsed_parameter_dictionary["series"]:
            nested_layout = QHBoxLayout()  # Create a new instance for each iteration
            for attribute_name, current_value in element.items():
                if attribute_name == "id" or attribute_name == "description":
                    label = QLabel(f'{attribute_name}: {current_value}')
                    nested_layout.addWidget(label)
                else:
                    label = QLabel(f'{attribute_name}: ')
                    nested_layout.addWidget(label)
                    
                    text_field = QLineEdit()
                    text_field.setText(current_value)
                    nested_layout.addWidget(text_field)
            
            layout.addLayout(nested_layout)

        series_tab.setLayout(layout)
        return series_tab
    def module_specific_tab_ui(self):
        # Creates a tab for accessing module specific (i.e., patch vs potts) parameter values
        module_specific_tab = QWidget()
        layout = QVBoxLayout()
                #Display parameters from xml
        for element in self.parsed_parameter_dictionary["patch"]:
            nested_layout = QHBoxLayout()  # Create a new instance for each iteration
            for attribute_name, current_value in element.items():
                if attribute_name == "id" or attribute_name == "description":
                    label = QLabel(f'{attribute_name}: {current_value}')
                    nested_layout.addWidget(label)
                else:
                    label = QLabel(f'{attribute_name}: ')
                    nested_layout.addWidget(label)
                    
                    text_field = QLineEdit()
                    text_field.setText(current_value)
                    nested_layout.addWidget(text_field)
            
            layout.addLayout(nested_layout)

        module_specific_tab.setLayout(layout)
        return module_specific_tab
    def population_tab_ui(self):
        # Creates a tab for accessing population parameter values
        # Can add a new population to see additional sub-population parameters
        population_tab = QWidget()
        layout = QVBoxLayout()
                
        nested_layout = QHBoxLayout()
        nested_layout.addWidget(QLabel('population: '))
        nested_layout.addWidget(QLabel("id"))
        self.population_id_input = QLineEdit(self)
        nested_layout.addWidget(self.population_id_input)
        nested_layout.addWidget(QLineEdit())
        nested_layout.addWidget(QLabel("init"))
        nested_layout.addWidget(QLineEdit())
        nested_layout.addWidget(QLabel("class"))
        nested_layout.addWidget(QLineEdit())
        nested_layout.addWidget(QLabel("Valid classes include cancer_stem and tissue"))
        layout.addLayout(nested_layout)
        self.add_row_button = QPushButton('Add population', self)
        self.add_row_button.clicked.connect(self.add_new_population)
        layout.addWidget(self.add_row_button)
        #population_id_list
        population_tab.setLayout(layout)
        self.population_tab_layout = layout 
        return population_tab
    def add_new_population(self): 
        # Displays population parameters once a population is created
        # Save the given population IDs for reference by components
        population_id = self.population_id_input.text().strip()

        # Create a QGroupBox with the given group box
        group_box = QGroupBox(population_id)
        group_layout = QVBoxLayout()
        # Display parameters from xml
        for element in self.parsed_parameter_dictionary["population"]:
            nested_layout = QHBoxLayout()  # Create a new instance for each iteration
            for attribute_name, current_value in element.items():
                if attribute_name == "id" or attribute_name == "description" or attribute_name == "module" or attribute_name == "process":
                    form_layout = QFormLayout()
                    label = QLabel(f'{attribute_name}: {current_value}')
                    form_layout.addWidget(label)
                    nested_layout.addLayout(form_layout)
                else:
                    form_layout = QFormLayout()
                    label = QLabel(f'{attribute_name}: ')
                    form_layout.addWidget(label)
                    text_field = QLineEdit()
                    text_field.setText(current_value)
                    form_layout.addRow(label, text_field)
                    nested_layout.addLayout(form_layout)
            group_layout.addLayout(nested_layout)

             # Set the main layout for the QGroupBox
        group_box.setLayout(group_layout)

        # Append the group name to the class variable
        Window.population_id_list.append(population_id)
        print(f'Group Name List: {Window.population_id_list}')
        self.population_tab_layout.addWidget(group_box)
        
    def layer_tab_ui(self):
        # Creates a tab for accessing layer parameter values
        layer_tab = QWidget()
        layout = QVBoxLayout()
                #Display parameters from xml
        for element in self.parsed_parameter_dictionary["layer"]:
            nested_layout = QHBoxLayout()  # Create a new instance for each iteration
            for attribute_name, current_value in element.items():
                if attribute_name == "id" or attribute_name == "description":
                    label = QLabel(f'{attribute_name}: {current_value}')
                    nested_layout.addWidget(label)
                else:
                    label = QLabel(f'{attribute_name}: ')
                    nested_layout.addWidget(label)
                    
                    text_field = QLineEdit()
                    text_field.setText(current_value)
                    nested_layout.addWidget(text_field)
            
            layout.addLayout(nested_layout)

        layer_tab.setLayout(layout)
        return layer_tab
    def action_tab_ui(self):
        # Creates a tab for accessing action parameter values
        action_tab = QWidget()
        layout = QVBoxLayout()
                #Display parameters from xml
        for element in self.parsed_parameter_dictionary["action"]:
            nested_layout = QHBoxLayout()  # Create a new instance for each iteration
            for attribute_name, current_value in element.items():
                if attribute_name == "id" or attribute_name == "description":
                    label = QLabel(f'{attribute_name}: {current_value}')
                    nested_layout.addWidget(label)
                else:
                    label = QLabel(f'{attribute_name}: ')
                    nested_layout.addWidget(label)
                    
                    text_field = QLineEdit()
                    text_field.setText(current_value)
                    nested_layout.addWidget(text_field)
            
            layout.addLayout(nested_layout)

        action_tab.setLayout(layout)
        return action_tab
    def components_tab_ui(self):
        # Creates a tab for accessing component parameter values
        components_tab = QWidget()
        layout = QVBoxLayout()
                #Display parameters from xml
        for element in self.parsed_parameter_dictionary["component"]:
            nested_layout = QHBoxLayout()  # Create a new instance for each iteration
            for attribute_name, current_value in element.items():
                if attribute_name == "id" or attribute_name == "description":
                    label = QLabel(f'{attribute_name}: {current_value}')
                    nested_layout.addWidget(label)
                else:
                    label = QLabel(f'{attribute_name}: ')
                    nested_layout.addWidget(label)
                    
                    text_field = QLineEdit()
                    text_field.setText(current_value)
                    nested_layout.addWidget(text_field)
            
            layout.addLayout(nested_layout)

        components_tab.setLayout(layout)
        return components_tab


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())




