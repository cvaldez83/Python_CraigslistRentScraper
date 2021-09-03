
""" To be able to use the initialized logger you 
    need to 'get' the logger that you initially
    created like so: """
import logging
logger = logging.getLogger('myapp')


""" Then, you'll be able to use it like so: """
def cool():
    logger.info(f'testing from cool')
    pass