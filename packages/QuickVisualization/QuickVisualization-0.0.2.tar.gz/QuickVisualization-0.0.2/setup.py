from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = "A data visualization package for quick visualizations"

# Setting up
setup(
    name="QuickVisualization",
    version=VERSION,
    author="Harika Ankathi",
    author_email="<harikaankathi7@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['seaborn', 'matplotlib>=3.0.0', 'ipywidgets'],
    keywords=['python', 'visualization'],

)