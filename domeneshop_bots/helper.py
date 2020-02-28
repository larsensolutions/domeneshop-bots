"""
Decorations functions and other helper functions for domeneshop_bots
"""
import logging

logger = logging.Logger('botHelper')

def on_error(msg):
    """
    Just a simple generic exception decorator

    :param msg: Readble message for the anticipated exception
    """
    def wrapper(func):
        def helper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error("%s error: %s", msg, str(e))
            finally:
                return None
        return helper
    return wrapper
