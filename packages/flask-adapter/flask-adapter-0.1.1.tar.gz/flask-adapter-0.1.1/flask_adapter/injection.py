"""
Module to inject a DTO instance into a flask route function.

Decorators:
    params: Decorator to inject a DTO instance into a flask route function.
    
"""
from flask import request
from functools import wraps
from dataclasses import fields




def params(dto_class, whitelist=True):
    """Decorator to inject a DTO instance into a flask route function.

    Args:
        dto_class (dataclass): The DTO class to be injected.
        whitelist (bool, optional): If True, only the DTO fields will be injected. Defaults to True.
    
    Important:
        - The decorator only accepts the following request methods: GET, POST, PUT, DELETE.
        - If the request method is GET or DELETE, the data will be extracted from the request.args.
        - If the request method is POST or PUT, the data will be extracted from the request.json.
        - If the whitelist is True, only the DTO fields will be injected.
        - If the whitelist is False, all the request data will be injected.
        - The decorator only accepts dataclasses as DTOs.

    Examples:
        >>> from dataclasses import dataclass
        >>> from flask import Flask
        >>> from flask_adapter.injection import params
        >>>
        >>> app = Flask(__name__)
        >>>
        >>> @dataclass
        >>> class UserDTO:
        >>>     name: str
        >>>     age: int
        >>>
        >>> @app.route('/user')
        >>> @params(UserDTO)
        >>> def get_user(user_dto: UserDTO):
        >>>     return user_dto.name
        >>>
        >>> if __name__ == '__main__':
        >>>     app.run()

    Raises:
        Exception: If the request method is not allowed.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            accepted_methods = ['GET', 'POST', 'PUT', 'DELETE']
            if request.method not in accepted_methods:
                raise Exception(f"Method {request.method} not allowed at params decorator.")
            

            if request.method in ['GET', 'DELETE']:
                data = request.args.to_dict()
            elif request.method in ['POST', 'PUT']:
                data = request.json
            else:
                data = {}

            if whitelist:
                valid_keys = {f.name for f in fields(dto_class)}
                data = {key: value for key, value in data.items() if key in valid_keys}

            dto_instance = dto_class(**data)
            return func(dto_instance, *args, **kwargs)

        return wrapper

    return decorator
