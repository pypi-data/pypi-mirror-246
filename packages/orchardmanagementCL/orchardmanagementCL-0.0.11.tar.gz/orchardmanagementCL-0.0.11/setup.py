import codecs
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.11'
DESCRIPTION = 'orchard management system'
LONG_DESCRIPTION = ('This repository contains the code for an Orchard Management Package, '
                    'designed to manage fruit production, inventory, and sales. '
                    'The system is implemented in Python and utilizes the pandas library for data manipulation and matplotlib for plotting.')

setup(
    name="orchardmanagementCL",
    version=VERSION,
    author="Yahan Cong, Kang Lu",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
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
