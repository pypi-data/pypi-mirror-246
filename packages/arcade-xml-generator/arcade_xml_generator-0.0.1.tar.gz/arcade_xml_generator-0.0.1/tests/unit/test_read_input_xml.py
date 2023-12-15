import sys
import os
import unittest
import xml.etree.ElementTree as ET

current_script_path = os.path.dirname(os.path.abspath(__file__))
relative_path_to_XMLObject = os.path.normpath(os.path.join(current_script_path, '../../src/'))
sys.path.append(relative_path_to_XMLObject)
from xml_object import XMLObject
from read_input_xml import ReadInputModuleSpecific
from read_input_xml import ReadInputFunctions

# Utilized by the tests for quick comparison
def compare_xml_files(file1, file2):
    tree1 = ET.parse(file1)
    tree2 = ET.parse(file2)

    # Get the root elements
    root1 = tree1.getroot()
    root2 = tree2.getroot()

    # Compare the XML content
    return ET.tostring(root1) == ET.tostring(root2)
def compare_element_lists(list1, list2):
    # Check if the lengths are equal
    if len(list1) != len(list2):
        return False

    # Compare each element in the lists
    for elem1, elem2 in zip(list1, list2):
        if not compare_elements(elem1, elem2):
            return False

    return True

def compare_elements(elem1, elem2):
    # Compare the tag, attributes, and text content of two elements
    return (
        elem1.tag == elem2.tag and
        elem1.attrib == elem2.attrib and
        elem1.text == elem2.text and
        compare_element_lists(elem1, elem2)
    )
class TestXMLToObject(unittest.TestCase):
    #Tests the read_input_xml.py methods
    def setUp(self):
        test_files_directory = os.path.dirname(os.path.abspath(__file__))
        os.chdir(test_files_directory)
    def test_fine_and_store_parameter_files_as_XMLObject(self):
        # Tests that read_input_xml can locate all the parameter .xml files
        list_of_directories = ReadInputFunctions.list_directories()
        list_of_parameter_files = ReadInputFunctions.find_and_store_xml_files(list_of_directories, "parameter")
        tester_parameter_list = ['parameter.patch', 'parameter.potts', 'parameter']
        self.assertEqual(len(list_of_parameter_files), len(tester_parameter_list))
    
    def test_convert_xml_to_object(self):
       # Tests that .xml file can be converted into a xml_object
       list_of_directories = ReadInputFunctions.list_directories()
       dict_of_parameter_files = ReadInputFunctions.find_and_store_xml_files(list_of_directories, "")
       print("testPrint")
       print(dict_of_parameter_files['children_test'])
       tree_with_children = ReadInputFunctions.load_xml_as_object(dict_of_parameter_files['children_test'])
       XMLObject.save_XML(tree_with_children, 'children_test_converted.xml') 
       self.assertTrue(compare_xml_files('children_test.xml', 'children_test_converted.xml'))

   
    def test_parse_xml_by_tag(self):
        # Tests that .xml can be parsed by tag
        list_of_directories = ReadInputFunctions.list_directories()
        list_of_parameter_files = ReadInputFunctions.find_and_store_xml_files(list_of_directories, "parameter")
        parsed_list_of_actions = ReadInputFunctions.grab_parameters_based_on_prefix(list_of_parameter_files['parameter.patch'], 'action')
    
        list_of_directories = ReadInputFunctions.list_directories()
        list_of_parameter_files = ReadInputFunctions.find_and_store_xml_files(list_of_directories, "parameter")
        parsed_list_of_patch = ReadInputFunctions.grab_parameters_based_on_prefix(list_of_parameter_files['parameter.patch'], 'layer')

        tree = ET.parse('action_param.xml')
        only_list_of_actions = []
        for elem in tree.getroot():
            only_list_of_actions.append(elem)

        self.assertTrue(compare_element_lists(parsed_list_of_actions, only_list_of_actions))
        self.assertFalse(compare_element_lists(parsed_list_of_actions, parsed_list_of_patch))
    
    def test_read_in_patch_parameters(self):
        #Tests that the patch specific parsing is done correctly
        list_of_directories = ReadInputFunctions.list_directories()
        list_of_parameter_files = ReadInputFunctions.find_and_store_xml_files(list_of_directories, "parameter")
        patch_dict = ReadInputModuleSpecific.read_in_patch_parameters(list_of_parameter_files)
        self.assertIn('default', patch_dict, f"default not found in the dictionary")
        self.assertIsInstance(patch_dict["default"], list)
        self.assertIn("series", patch_dict, f"series not found in the dictionary")
        self.assertIsInstance(patch_dict["series"], list)
        self.assertIn("population", patch_dict, f"population not found in the dictionary")
        self.assertIsInstance(patch_dict["population"], list)
        self.assertIn("layer", patch_dict, f"layer not found in the dictionary")
        self.assertIsInstance(patch_dict["layer"], list)
        self.assertIn("action", patch_dict, f"action not found in the dictionary")
        self.assertIsInstance(patch_dict["action"], list)
        self.assertIn("component", patch_dict, f"component not found in the dictionary")
        self.assertIsInstance(patch_dict["component"], list)
    # FUTURE IMPLEMENTATION: Potts test
    
if __name__ == "__main__":
    unittest.main()
