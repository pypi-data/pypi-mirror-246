import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List
import copy 

@dataclass(order=True)
class XMLObject:
    tag: str
    attribute_dict: dict = field(default_factory=dict)
    children: List['XMLObject'] = field(default_factory=list)
    parent: 'XMLObject' = None  #Initialized later
    default_tag: str = field(init=False)
    default_attribute_dict: dict = field(init=False)


    def __post_init__(self):
        # Set parent attribute for each child
        for child in self.children:
            child.parent = self
        # Set default values
        self.default_tag = copy.deepcopy(self.tag)
        self.default_attribute_dict = copy.deepcopy(self.attribute_dict)


    def convert_to_element_tree(self):
        element = ET.Element(self.tag, self.attribute_dict)
        for child in self.children:
            child_element = child.convert_to_element_tree()
            element.append(child_element)
        return element
    def save_XML(self, file_name):
        tree = ET.ElementTree(self.convert_to_element_tree())
        print(type(tree))
        ET.indent(tree, space="\t", level=0)
        tree.write(file_name, encoding="utf-8")
    def merge_with_tag(self, donor_xml_object, target_tag):
        # Find a node with a matching tag in the target_tag
        target_node = self.find_node_with_tag(donor_xml_object, target_tag)
        if target_node is not None:
            # Append donor_xml_object as a child to the found node
            target_node.append(donor_xml_object)
    def find_node_with_tag(self, tag):
        # Recursive function to find a node with a matching tag
        if self.tag == tag:
            return self
        if self.children == None:
            return None
        for child in self.children:
            node = child.find_node_with_tag(tag)
            if node is not None:
                return node
        return None
    def merge_with_id_value(self, donor_xml_object, target_id):
        # Find a node with a matching tag in the target_tag
        target_node = self.find_node_with_tag(donor_xml_object, target_id)
        if target_node is not None:
            # Append donor_xml_object as a child to the found node
            target_node.append(donor_xml_object)
    def find_node_with_id_value(self, id_value):
        # Recursive function to find a node with a matching id value
        if "id" in self.attribute_dict and self.attribute_dict["id"] == id_value:
            return self
        if self.children == None:
            return None
        for child in self.children:
            node = child.find_node_with_id_value(id_value)
            if node is not None:
                return node
        return None
    def reset_tag(self):
        self.tag = self.default_tag
    def reset_attribute(self):
        self.attribute_dict = self.default_attribute_dict
    def reset(self):
        self.reset_tag()
        self.reset_attribute()
    def edit_tag(self, new_tag):
        self.tag = new_tag
    def edit_attribute(self, key, new_attribute):
        if key in self.attribute_dict:
            self.attribute_dict[key] = new_attribute
        else:
            raise KeyError(f"Key '{key}' not found in attribute_dict")
    def create_a_population(self, id, parameter_init, parameter_class):
        return



