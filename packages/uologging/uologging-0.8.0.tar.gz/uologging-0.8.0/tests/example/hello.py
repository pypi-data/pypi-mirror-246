# hello.py
import logging

import uologging

logger = logging.getLogger(__name__)


@uologging.trace(logger)
def hello():
    print('hello from example!')
    logger.debug('This is a DEBUG msg.')
    logger.info('This is a INFO msg.')
    logger.warning('This is a WARNING msg.')
