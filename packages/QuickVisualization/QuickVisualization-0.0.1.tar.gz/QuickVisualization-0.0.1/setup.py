from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = "A visualization package for instant data visualization"

# Setting up
setup(
    name="QuickVisualization",
    version=VERSION,
    author="Harika Ankathi",
    author_email="<harikaankathi7@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['seaborn', 'matplotlib', 'ipywidgets','pandas'],
    keywords=['python', 'visualization'],

)