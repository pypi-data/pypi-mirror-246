from setuptools import setup, find_packages

long_description = long_description = """
Flask Adapter
=============

.. image:: https://travis-ci.org/seu-usuario/flask-adapter.svg?branch=master
    :target: https://travis-ci.org/seu-usuario/flask-adapter

.. image:: https://badge.fury.io/py/flask-adapter.svg
    :target: https://badge.fury.io/py/flask-adapter

Flask Adapter é um pacote Python que fornece funcionalidades adicionais para integrar Data Transfer Objects (DTOs) em rotas Flask.

Instalação
----------

Instale o Flask Adapter usando o pip:

.. code-block:: bash

    pip install flask-adapter

Exemplo de Uso
--------------

.. code-block:: python

    from flask import Flask
    from dataclasses import dataclass
    from flask_adapter.injection import params

    app = Flask(__name__)

    @dataclass
    class UserDTO:
        id: int
        name: str

    @dataclass
    class CreateUserDTO:
        username: str
        email: str

    @app.route("/user", methods=["GET", "POST", "PUT"])
    @params(UserDTO, whitelist=False)
    def user_controller(user_dto: UserDTO):
        return f"User: {user_dto.id}, {user_dto.name}"

    @app.route("/create_user", methods=["POST"])
    @params(CreateUserDTO)
    def create_user_controller(create_user_dto: CreateUserDTO):
        return f"Creating user: {create_user_dto.username}, {create_user_dto.email}"

    if __name__ == "__main__":
        app.run(debug=True)
"""


setup(
    name='flask-adapter',
    version='0.1.4',
    description='A simple adapter for flask to inject DTOs into route functions.',
    long_description=long_description,
    author='Diogo Souza',
    author_email='diogommtdes@gmail.com',
    packages=find_packages(),
    install_requires=[
        'Flask',
    ],
)
