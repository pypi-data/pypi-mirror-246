from setuptools import setup, find_packages

setup(
    name='flask-adapter',
    version='0.1.1',
    description='A simple adapter for flask to inject DTOs into route functions.',
    long_description=open('readme.rst').read(),
    author='Diogo Souza',
    author_email='diogommtdes@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Flask',
    ],
)
