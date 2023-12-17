from setuptools import setup, find_packages

setup(
    name='flask-adapter',
    version='0.1.0',
    description='A simple adapter for flask to inject DTOs into route functions.',
    author='Diogo Souza',
    author_email='diogommtdes@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Flask',
    ],
)
