#!/usr/bin/env python3
from setuptools import setup

def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()

setup(name='aura-api',
      version='1.0.2',
      description='Python API for Yandex.Aura',
      long_description=read('README.md'),
      long_description_content_type="text/markdown",
      author='mickxolotl',
      author_email='mickxolotl@yandex.ru',
      url='https://github.com/skorpionikus/aura-api',
      packages=['aura'],
      license='GPL3',
      keywords='yandex aura api',
      install_requires=['requests'],
      )