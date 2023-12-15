
from setuptools import find_packages, setup

# To use a consistent encoding
from pathlib import Path
#from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
#with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()

#read the contents of your README file

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = 'pystatslib',
    packages = find_packages(include = ['pystatslib']),
    version = '0.1.0',
    description = "Python Statistics and Probability library",
    long_description_content_type = 'text/markdown',
    long_description = open('README.md').read(),
    author = ['Michael Dobo', 'Michael Gannon', 'Maia Bolko', 'Nicole Messina'],
    url = 'https://github.com/maiabolko/AMS-595-Final-Project', 
    license = 'MIT',
    install_requires = ['numpy', 'scipy', 'pandas', 'matplotlib.pyplot', 'time', 'sympy', 'sys', 'math', 'mpl_toolkits.mplot3d'],
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest==4.4.1'],
    test_suite = 'tests',
)












