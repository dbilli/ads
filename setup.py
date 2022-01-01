# -*- coding: utf-8 -*-
import os

from setuptools import find_packages
from setuptools import setup

import ads

base_dir = os.path.dirname(__file__)

setup(
    name='ads',
    version=ads.__version__,
    description='',

    author='Diego Billi',
    author_email='diegobilli@gmail.com',

    setup_requires='setuptools',
    
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],

    entry_points={
        'console_scripts': [
            'ads-daemon=ads.server.launcher:main',
        ]
    },
    
    packages=find_packages(),

    install_requires=[
        'adtk==0.6.2',
        'Flask==1.1.2',
        'numpy==1.20',
        'uwsgi==2.0.19.1',
    ]
)
