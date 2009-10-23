#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='fabric_factory',
      version='0.1',
      description='fabric_factory',
      author='Yann Malet',
      author_email='yann.malet@gmail.com',
      url='',
      #packages=find_packages('src'),
      package_dir = {'':'src'},
     )
