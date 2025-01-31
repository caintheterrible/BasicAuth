import os
import logging
import logging.config
from app_config.settings.base import BASE_DIR


class LoggingConfiguration:
    """Handles logging functionalities."""

    def __init__(self, base_dir=BASE_DIR):
        self._base_dir = base_dir
        if not self._base_dir:
            raise ValueError(f'Base directory reference not set!')
        self._log_dir = os.path.join(self._base_dir, 'logs')
        self._info_dir = os.path.join(self._log_dir, 'info')
        self._error_dir = os.path.join(self._log_dir, 'errors')
        self._warning_dir = os.path.join(self._log_dir, 'warnings')

    def create_log_dirs(self):
        """Creates dynamically log directories by category."""
        dirs = [
            self._log_dir,
            self._info_dir,
            self._error_dir,
            self._warning_dir,
        ]
        # if directory not existing, create dynamically
        for directory in dirs:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f'Created new directory: {directory}')

    @staticmethod
    def get_formatter():
        """Standardized log formatter."""
        return logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%d %H:%M:%S'
        )

    def logging_conf(self):
        """Custom logging configurations."""
        _logging = {
            'version': 1,
            'disable_existing_handlers': False,
            'formatters': {
                'standard': {
                    '()': lambda: self.get_formatter(),  # Fix: Make it a callable
                },
            },
            'handlers': {
                'info_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'INFO',
                    'filename': os.path.join(self._info_dir, 'info.logs'),
                    'maxBytes': 1024 * 1024 * 5,
                    'backupCount': 5,
                    'formatter': 'standard',
                },
                'error_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'ERROR',
                    'filename': os.path.join(self._error_dir, 'error.log'),
                    'maxBytes': 1024 * 1024 * 5,
                    'backupCount': 5,
                    'formatter': 'standard',
                },
                'warning_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'WARNING',
                    'filename': os.path.join(self._warning_dir, 'warning.log'),
                    'maxBytes': 1024 * 1024 * 5,
                    'backupCount': 5,
                    'formatter': 'standard',
                },
                'console_logging': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',  # Change to INFO or DEBUG to see all levels
                    'formatter': 'standard',
                },
            },
            'loggers': {
                '': {
                    'handlers': [
                        'info_file',
                        'error_file',
                        'warning_file',
                        'console_logging',
                    ],
                    'level': 'INFO',  # Change to INFO or DEBUG to capture all levels
                    'propagate': True,
                },
            },
        }
        return _logging

    def configure_logging(self):
        """Sets up logging based on configurations."""
        self.create_log_dirs()
        logging.config.dictConfig(self.logging_conf())

    def get_logger(self, name):
        """Returns a configured logger instance."""
        return logging.getLogger(name)


# Example usage
#if __name__ == '__main__':
    #logging_config = LoggingConfiguration()
    #logging_config.configure_logging()

    #logger = logging_config.get_logger(__name__)
    #logger.info('This is an info message.')
    #logger.warning('This is a warning message.')
    #logger.error('This is an error message.')