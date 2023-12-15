#This module is not yet implemented. When it has been fully developed it will be a small module that takes a dictionary of xml_objects
# and organizes them using xml_object methods. The method of arranging the xml_objects will be specific by the string title of the initial .xml parameter file
# A final version of .xml will be saved for setup. Future iterations may include a Linter and a connection to Bash to directly run the setup.

from logging import raiseExceptions
import tkinter as tk
import xml.etree.ElementTree as ET
import sys
import os

current_script_path = os.path.dirname(os.path.abspath(__file__))
relative_path_to_XMLObject = os.path.normpath(os.path.join(current_script_path, '../../src/'))
sys.path.append(relative_path_to_XMLObject)
from xml_object import XMLObject


class ReadOutputFunctions():
    def compile(self, dictionary_of_inputs, input_parameter_filename):
        #Takes dictionary of inputs, and calls the function associated with the input_parameter_filename
        if (input_parameter_filename == "parameter.patch"):
            self.user_input_to_patch_setup(dictionary_of_inputs)
        elif (input_parameter_filename == "potts.patch"):
            self.user_input_to_potts_setup(dictionary_of_inputs)
        else:
            raise NotImplementedError("This function is not yet implemented.")
        return
    def user_input_to_patch_setup(self, dictionary_of_inputs):
        #Compiles dictionary to create patch setup .xml
        #NOT IMPLEMENTED
        return
    def user_input_to_potts_setup(self, dictionary_of_inputs):
        #Compiles dictionary to create potts .xml
        #NOT IMPLEMENTED
        return
