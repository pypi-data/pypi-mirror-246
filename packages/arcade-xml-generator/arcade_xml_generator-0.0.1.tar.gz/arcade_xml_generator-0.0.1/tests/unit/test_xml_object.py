import unittest
import sys
import os

current_script_path = os.path.dirname(os.path.abspath(__file__))
relative_path_to_XMLObject = os.path.normpath(os.path.join(current_script_path, '../../src/'))
sys.path.append(relative_path_to_XMLObject)
from xml_object import XMLObject

class TestObjectCreation(unittest.TestCase):
    #Tests the xml_object initializaiton and associated functions

    def setUp_nochildren_noparent(self):
        #Creates an object with no children or parents.
        self.population_simple = XMLObject(tag = 'population', attribute_dict = {'id':'C', 'init':'100', 'class':'cancer'})
    def setUp_children(self):
        #Creates an object with children and parents.
        """
        populations
        |-population
            |-population parameter
            |-population process
            |-population process
        """
        self.tree_with_children = XMLObject(tag = 'populations')
        self.tree_with_children.children.append(XMLObject(tag = 'population', attribute_dict = {'id':'C', 'init':'100', 'class':'cancer'}))
        self.tree_with_children.children[0].children.append(XMLObject(tag = 'population.parameter', attribute_dict = {'id':'DIVISION_POTENTIAL', 'value':'3'}))
        self.tree_with_children.children[0].children.append(XMLObject(tag = 'population.process', attribute_dict = {'id':'METABOLISM', 'version':'complex'}))
        self.tree_with_children.children[0].children.append(XMLObject(tag = 'population.process', attribute_dict = {'id':'SIGNALING', 'version':'complex'}) )
        
    def test_to_convert_to_element_tree_simple(self):
        #tests the creation of childless tree
        self.setUp_nochildren_noparent()
        root_element = XMLObject.convert_to_element_tree(self.population_simple)
        self.assertEqual(root_element.tag, 'population')
        self.assertEqual(root_element.attrib, {'id':'C', 'init':'100', 'class':'cancer'})
        XMLObject.save_XML(self.population_simple, "simpleTest.xml")  
    
    def test_object_save(self):
        #tests that the object can be saved as an .xml file
        path = os.path.join(os.getcwd(), "saveTest.xml")
        if os.path.isfile(path):
            os.remove(path)
        self.setUp_nochildren_noparent()
        XMLObject.save_XML(self.population_simple, path)
        self.assertTrue(os.path.isfile(path))
        os.remove(path)

    def test_to_convert_to_element_tree_children(self):
        #tests that the object can be turned into a ET from .xml level manipulation
        self.setUp_children()
        root_element = XMLObject.convert_to_element_tree(self.tree_with_children)
        
        self.assertEqual(root_element.tag, 'populations')
        self.assertEqual(root_element[0].tag, 'population')
        self.assertEqual(root_element[0].attrib, {'id':'C', 'init':'100', 'class':'cancer'})

        children_elements = list(root_element[0])
        
        self.assertEqual(children_elements[0].tag, 'population.parameter')
        self.assertEqual(children_elements[0].attrib, {'id':'DIVISION_POTENTIAL', 'value':'3'})

        self.assertEqual(children_elements[1].tag, 'population.process')
        self.assertEqual(children_elements[1].attrib, {'id':'METABOLISM', 'version':'complex'})
        
        self.assertEqual(children_elements[2].tag, 'population.process')
        self.assertEqual(children_elements[2].attrib, {'id':'SIGNALING', 'version':'complex'})

        XMLObject.save_XML(self.tree_with_children, "children_test.xml") 
    
    def test_edit_attribute(self):
        #tests that attributes can be edited
        self.setUp_nochildren_noparent()
        XMLObject.edit_attribute(self.population_simple,"id", "barry")
        self.assertEqual(self.population_simple.attribute_dict["id"], "barry")

    def test_reset_attribute(self):
        #tests that attributes can be reset
        self.setUp_nochildren_noparent()
        XMLObject.edit_attribute(self.population_simple,"id", "barry")
        self.population_simple.reset_attribute()
        self.assertEqual(self.population_simple.attribute_dict["id"], "C")

    def test_edit_tag(self):
        #tests that tags can be edited
        self.setUp_nochildren_noparent()
        XMLObject.edit_tag(self.population_simple, "barry")
        self.assertEqual(self.population_simple.tag, "barry")
    def test_reset_tag(self):
        #tests that tags can be reset
        self.setUp_nochildren_noparent()
        XMLObject.edit_tag(self.population_simple, "barry")
        self.population_simple.reset_tag()
        self.assertEqual(self.population_simple.tag, "population")
    def test_reset(self):
        #tests that both attributes and tags can be reset at once
        self.setUp_nochildren_noparent()
        XMLObject.edit_attribute(self.population_simple,"id", "barry")
        XMLObject.edit_tag(self.population_simple, "barry")
        self.population_simple.reset()
        self.assertEqual(self.population_simple.attribute_dict["id"], "C")
        self.assertEqual(self.population_simple.tag, "population")
    def test_find_node_with_tag(self):
        #tests that a node can be identified using a tag
        self.setUp_children()
        node = XMLObject.find_node_with_tag(self.tree_with_children, "population.parameter")
        root_element = XMLObject.convert_to_element_tree(self.tree_with_children)
        children_elements = list(root_element[0])
        self.assertEqual(children_elements[0].tag, node.tag)
        self.assertEqual(children_elements[0].get("id"), node.attribute_dict["id"])

    def test_find_node_with_id_value(self):
        #tests that a node can be identified using an id
        self.setUp_children()
        node = XMLObject.find_node_with_id_value(self.tree_with_children, "METABOLISM")
        root_element = XMLObject.convert_to_element_tree(self.tree_with_children)
        children_elements = list(root_element[0])
        self.assertEqual(children_elements[1].tag, node.tag)
        self.assertEqual(children_elements[1].get("id"), node.attribute_dict["id"])
    #Potential future methods:
    # def test_merge_with_id_value(self):
    #     self.setUp_children()
    #     self.setUp_nochildren_noparent()
        
    # def test_merge_with_tag(self):
    #     self.setUp_children()
    #     self.setUp_nochildren_noparent()
        

if __name__ == "__main__":
    unittest.main()
