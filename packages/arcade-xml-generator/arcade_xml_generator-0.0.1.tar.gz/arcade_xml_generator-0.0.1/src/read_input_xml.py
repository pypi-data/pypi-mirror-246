import xml.etree.ElementTree as ET
import sys
import os

current_script_path = os.path.dirname(os.path.abspath(__file__))
relative_path_to_XMLObject = os.path.normpath(os.path.join(current_script_path, '../../src/'))
sys.path.append(relative_path_to_XMLObject)
from xml_object import XMLObject


def element_to_xml_object(element, parent=None):
    #helper function for ReadInputFunctions. Takes a element tree and creates an xml_object
    xml_object = XMLObject(
        tag=element.tag,
        attribute_dict=element.attrib,
        parent=parent
    )
    for child_element in element:
        child_xml_object = element_to_xml_object(child_element, parent=xml_object)
        xml_object.children.append(child_xml_object)
    return xml_object
def list_to_xml_object(element, wrapper):
    #helper function for ReadInputFunctions. Takes a list and creates an xml_object
    childrenList= []
    for child_element in element:
        child_xml_object = XMLObject(
            tag=child_element.tag,
            attribute_dict=child_element.attrib
        )
        childrenList.append(child_xml_object)
    root = XMLObject(
        tag=wrapper,
        children = childrenList
    )
    
    return root

#Contains functions that locate and reads in .xml files and outputs dictionaries of element trees.
class ReadInputFunctions():
    def list_directories():
        #Lists all directories starting one level above and going down
        directoryList =[]
        directoryTuples = os.walk(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        for x in directoryTuples:
            directoryList.append(x[0])
        return directoryList

    def find_and_store_xml_files(directories, keyword):
        # Saves all .xml files found in given list of directories that contain the keyword. Currently, the keyword is always "parameter"
        xml_files = {}
        for directory in directories:
            for filename in os.listdir(directory):
                if filename.endswith(".xml") and keyword in filename:
                    file_path = os.path.join(directory, filename)
                    key = os.path.splitext(os.path.basename(filename))[0]#drops extension
                    xml_files[key] = (file_path)
        return xml_files


   
    def grab_parameters_based_on_prefix(file_name, prefix):
        #Grabs ET elements out of .xml file based on prefix
        #file_name is a string identifying the .xml file. prefix is a string
        tree = ET.parse(file_name)
        default_parameters = []
        for elem in tree.iter():
            if elem.tag.startswith(prefix):
                default_parameters.append(elem)
        return default_parameters

    def load_xml_as_object(file_name):
        #Load .xml as an element tree and return the root. Gives a file_name
        tree = ET.parse(file_name)
        root_element = tree.getroot()
        return element_to_xml_object(root_element)
    

class ReadInputModuleSpecific():
    def read_in_patch_parameters(xml_files):
        #Reads in from dictionary of xml_files
        #Requires parameters.patch.xml and parameters.xml as identified by their keys without .xml 
        dict_of_parameters = {}
        #get default from parameters
        dict_of_parameters.update({"default": ReadInputFunctions.grab_parameters_based_on_prefix(xml_files["parameter"], "default")})
        #get series from patch (tag is also default)
        dict_of_parameters.update({"series": ReadInputFunctions.grab_parameters_based_on_prefix(xml_files["parameter.patch"], "default")})
        #get patch from patch
        dict_of_parameters.update({"patch": ReadInputFunctions.grab_parameters_based_on_prefix(xml_files["parameter.patch"], "patch")})
        #get population from patch
        dict_of_parameters.update({"population": ReadInputFunctions.grab_parameters_based_on_prefix(xml_files["parameter.patch"], "population")})
        #get layer from patch
        dict_of_parameters.update({"layer": ReadInputFunctions.grab_parameters_based_on_prefix(xml_files["parameter.patch"], "layer")})
        #get action from patch
        dict_of_parameters.update({"action": ReadInputFunctions.grab_parameters_based_on_prefix(xml_files["parameter.patch"], "action")})
        #get component from patch
        dict_of_parameters.update({"component": ReadInputFunctions.grab_parameters_based_on_prefix(xml_files["parameter.patch"], "component")})
        return dict_of_parameters
    
    def read_in_potts_parameters(xml_files):
            raise NotImplementedError("This function is not yet implemented.")
            
    def read_in_module(self, module, xml_files):
        if module == "parameter.potts":
            return self.read_in_potts_parameters(xml_files)
        elif module == "parameter.patch":
            return self.read_in_patch_parameters(xml_files)
        else:
            raise NotImplementedError("This is either an invalid parameter file or this function is not yet implemented.")
