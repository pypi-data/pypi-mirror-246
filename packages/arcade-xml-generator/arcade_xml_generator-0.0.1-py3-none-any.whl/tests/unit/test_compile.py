import unittest
import sys
import os

current_script_path = os.path.dirname(os.path.abspath(__file__))
relative_path_to_XMLObject = os.path.normpath(os.path.join(current_script_path, '../../src/'))
sys.path.append(relative_path_to_XMLObject)
from xml_object import XMLObject
from compile_xml import ReadOutputFunctions

#These tests and the module it tests are not implemented.
class TestCompileSetUpFile(unittest.TestCase):
    
    #This method will test the pipeline of user input into a xml_object
    def test_user_input_to_object(self):
        return
    
    #This method tests the ability to create a .xml patch set up file.
    def test_patch_specific(self):
        return


if __name__ == "__main__":
    unittest.main()
