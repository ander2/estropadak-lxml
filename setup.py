#!/usr/bin/env python

from distutils.core import setup

setup(name='EstropadakParser',
      version='0.1.3',
      description='Python module for parsing Estropadak',
      author='Ander Garmendia',
      author_email='kelertxiki@gmail.com',
      url='http://www.estropadak.net',
      packages=['estropadakparser', 'estropadakparser.estropada'],
      package_data={'estropadakparser': ['data/*.txt']}
     )
