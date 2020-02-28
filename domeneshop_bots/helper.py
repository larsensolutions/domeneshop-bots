"""
Decorations functions and other timbits for domeneshop bots
"""
import logging
from jsonschema import validate, ValidationError

logger = logging.Logger('botHelper')


def on_error(msg, fatal=False):
    """
    Generic exception handler

    :param msg: Readble message for the anticipated exception
    """
    def wrapper(func):
        def helper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error("%s error: %s", msg, str(e))
            finally:
                if fatal:
                    raise Exception(msg)
        return helper
    return wrapper


def validator(schema):
    """
    JSON schema validator

    :param schema: schema
    """
    def wrapper(func):
        def helper(*args, **kwargs):
            try:
                _, data = args
                validate(data, schema)
            except ValidationError as e:
                msg = "Schema validation failed. %s" % (str(e))
                logger.error(msg)
                raise ValidationError(msg)
            return func(*args, **kwargs)
        return helper
    return wrapper
