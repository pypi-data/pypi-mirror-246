import os, logging, functools
from logging.handlers import RotatingFileHandler
from typing import Any, List


# def handle_errors(func):
#     @functools.wraps(func)
#     def wrapper(self, *args, **kwargs):
#         try: 
#             print(func.__class__.__name__)
#             return func(self, *args, **kwargs)
#         except Exception as e:
#             self.logger.error(f"Error in {func.__name__}: {e}", extra={'instance_name': self.instance_name})
#     return wrapper


def handle_errors(func):
    """
    A decorator that handles errors raised by the wrapped function and logs them.

    :param func: The function to be wrapped.

    >>> class Test:
    ...     @handle_errors
    ...     def __init__(self):
    ...         raise Exception
    ...
    >>> Test()

    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            if hasattr(self, 'logger') and self.logger is not None:
                
                if hasattr(self, 'instance_name') :
                    self.logger.error(f"Error in {func.__name__}: {e}", extra={'instance_name': self.instance_name})
                else:
                    self.logger.error(f"Error in {func.__name__}: {e}", extra={'instance_name': 'no instance_name attributs'})
            else:
                print(f"Error in {func.__name__}: {e}")
    return wrapper


class Logger:
    
    @handle_errors
    def __init__(self, instance_name='default', name='default', level=logging.DEBUG, log_file='my_log.log', max_size=1024, backup_count=5):
        
        self.instance_name = instance_name
        self.name = name

        self.log_file = log_file

        self.log_directory = os.path.dirname(log_file)

        if not self.log_directory:
            self.log_directory = './'

        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(instance_name)s] - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

        if self.log_file:
            file_handler = RotatingFileHandler(self.log_file, maxBytes=max_size, backupCount=backup_count)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    @handle_errors
    def __call__(self, instance_name=None, name=None) -> Any:
        if instance_name is not None:
            self.instance_name = instance_name
        if name is not None:
            self.logger.name = name
        return self

    @handle_errors
    def set_log_level(self, level):
        self.logger.setLevel(level)

    @handle_errors
    def set_log_format(self, log_format):
        formatter = logging.Formatter(log_format)
        for handler in self.logger.handlers:
            handler.setFormatter(formatter)

    @handle_errors
    def add_handler(self, handler):
        self.logger.addHandler(handler)

    @handle_errors
    def add_file_handler(self, log_file, max_size=1024, backup_count=5):
        file_handler = RotatingFileHandler(log_file, maxBytes=max_size, backupCount=backup_count)
        file_handler.setLevel(self.logger.level)
        file_handler.setFormatter(self.logger.handlers[0].formatter)
        self.logger.addHandler(file_handler)

    @handle_errors
    def log_with_context(self, level, message, context=None):
        log_method = getattr(self.logger, level)
        log_method(message, extra={'instance_name': self.instance_name, 'context': context})

    @handle_errors
    def set_log_rotation(self, max_size, backup_count):
        for handler in self.logger.handlers:
            if isinstance(handler, RotatingFileHandler):
                handler.maxBytes = max_size
                handler.backupCount = backup_count

    @handle_errors
    def debug(self, message):
        self.logger.debug(message, extra={'instance_name': self.instance_name})

    @handle_errors
    def info(self, message):
        self.logger.info(message, extra={'instance_name': self.instance_name})

    @handle_errors
    def warning(self, message):
        self.logger.warning(message, extra={'instance_name': self.instance_name})

    @handle_errors
    def error(self, message):
        self.logger.error(message, extra={'instance_name': self.instance_name})

    @handle_errors
    def critical(self, message):
        self.logger.critical(message, extra={'instance_name': self.instance_name})



# Running the doctest
if __name__ == "__main__":
    # The logging setup is required for the logger used in the doctest
    # logging.basicConfig(level=logging.DEBUG)

    # # Importing the required function for the doctest
    handle_errors = handle_errors
    print('doctest')
    import doctest
    doctest.testmod()