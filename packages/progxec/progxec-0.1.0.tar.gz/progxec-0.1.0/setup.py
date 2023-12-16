# setup.py
from setuptools import setup, find_packages

setup(
    name='progxec',
    version='0.1.0',
    author="Jaysheel",
    packages=find_packages(),
    install_requires=[
        'subprocess', 'os'
    ],
)
