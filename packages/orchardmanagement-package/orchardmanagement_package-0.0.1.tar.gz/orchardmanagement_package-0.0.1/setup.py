import codecs
import os
from setuptools import setup, find_packages

# you need to change all these
VERSION = '0.0.1'
DESCRIPTION = 'orchard management system'
LONG_DESCRIPTION = ('This repository contains the code for an Orchard Management Package, '
                    'designed to manage fruit production, inventory, and sales. '
                    'The system is implemented in Python and utilizes the pandas library for data manipulation and matplotlib for plotting.')

setup(
    name="orchardmanagement_package",
    version=VERSION,
    author="Yahan Cong, Kang Lu",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'orchard', 'orchardmanagement'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
