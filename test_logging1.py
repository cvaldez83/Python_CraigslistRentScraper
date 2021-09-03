from test_logging2 import cool

from test_logScript import setup_custom_logger
logger = setup_custom_logger('myapp')

logger.info(f'test test test')

cool()

