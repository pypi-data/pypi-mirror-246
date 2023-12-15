from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.01'
DESCRIPTION = 'GUI to load parameters into agent-based modeling with ARCADE'
LONG_DESCRIPTION = 'A package that creates a GUI for taking input .xml files and creating a .xml file for ARCADE to use as its parameters'

# Setting up
setup(
    name="arcade_xml_generator",
    version=VERSION,
    author="olafc",
    author_email="olafc@uw.edu",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['os', 'sys', 'xml.etree.ElementTree', 'PyQt5.QtCore', 'PyQt5.QtWidgets', 'logging', 'unittest'],
    keywords=['agent-based', 'modeling', 'xml', 'editor', 'gui'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
