# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'Telegrapi (Telegram Api) is a package for using Telegram network within Python.'
LONG_DESCRIPTION = 'Telegrapi (Telegram Api) is a package for using Telegram network within Python.'

# Setting up
setup(
    name="telegrapi",
    version=VERSION,
    author="Kunthet",
    author_email="<mail@kunthet.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    #package_dir={"": "telegrapi"},
    install_requires=[],
    license='MIT',
    license_files = ('LICENSE',),
    url='https://github.com/kunthet/telegrapi',
    keywords=['python', 'telegram', 'bot', 'api', 'light', 'simple'],
    
    classifiers=[
        # "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        # "Operating System :: Unix",
        # "Operating System :: MacOS :: MacOS X",
        # "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
    ],
    
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2", 'dotenv']
    },
    
    python_requires=">=3.9"
)