#!/usr/bin/env python

from distutils.core import setup

setup(
    name='EstropadakParser',
    version='0.1.20',
    description='Python module for parsing Estropadak',
    author='Ander Garmendia',
    author_email='kelertxiki@gmail.com',
    url='http://www.estropadak.eus',
    packages=['estropadakparser', 'estropadakparser.estropada', 'estropadakparser.parsers', 'estropadakparser.egutegia_parsers'],
    package_data={'estropadakparser': ['data/*.txt']},
    install_requires=[
        'lxml',
        'cssselect'
    ]
)
