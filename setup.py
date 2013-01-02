#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
from setuptools import setup, find_packages

from fktb import NAME, VERSION, AUTHOR, CONTACT

CURRENT_DIR = os.path.dirname(__file__)

README_PATH = os.path.join(CURRENT_DIR, 'README.txt')
if os.path.exists(README_PATH):
    with open(README_PATH) as readme:
        README = readme.read().strip()
else:
    README = ''

REQUIREMENTS_PATH = os.path.join(CURRENT_DIR, 'requirements.txt')
if os.path.exists(REQUIREMENTS_PATH):
    with open(REQUIREMENTS_PATH) as requirements:
        REQUIREMENTS = requirements.read().strip()
else:
    REQUIREMENTS = ''

setup(
    name=NAME,
    version=VERSION,
    description="Boite à outils orientés sécurité",
    long_description=README,
    author=AUTHOR,
    author_email=CONTACT,
    url='http://www.free-knowledge.net',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'fktb = fktb.interface.gui.module:main',
            #'fktb-cli = fktb.cli:main'
        ]
    },
    data_files=[
        ('fktb/images/', ['fktb/images/icone.png',
                          'fktb/images/logo_gpl_v3.png',
                          'fktb/images/logo_april.png',
                          'fktb/images/logo_zbar.png',
                          'fktb/images/white_hat.svg',
                          'fktb/images/a_propos.png',
                          'fktb/images/attente.gif',
                          'fktb/images/enregistrer.png'])
    ]
)
