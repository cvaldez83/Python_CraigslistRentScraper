#DEBUG:     Detailed information, typically of interest only when diagnosing problems
#INFO:      Confirmation that things are working as expected
#WARNING:   An indication that something unexpected happened.
#ERROR:     Due to a more serious problem, the software has not been able to perform some function
#CRITICAL:  A serious error, indicating that the program itself ma be unable to continue running

def setup_custom_logger(name):
    import sys
    import logging
    """ define path to log file """
    from config import path_to_logfile

    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    """ add ability to log to file """
    file_handler = logging.FileHandler(path_to_logfile, mode='a')
    file_handler.setFormatter(formatter)
    """ add ability to log to screen """
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    """ initialize a logger """
    logger = logging.getLogger(name)
    """ set level """
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(screen_handler)
    return logger

# """ setup logger instance """
# logger = setup_custom_logger('myapp', log_path)
# logger.debug('This is a debug message!')
# logger.info('This is a info message!')
# logger.warning('This is a warning message!')