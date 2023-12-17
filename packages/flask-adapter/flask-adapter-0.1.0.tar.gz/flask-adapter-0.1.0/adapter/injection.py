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
