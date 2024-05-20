import time
import logging

logger = logging.getLogger()

logging.basicConfig(level=logging.INFO)
while True:
    logger.info('Gas price data pulled')
    time.sleep(60)
