import logging
import logstash

log_format = logging.Formatter('\n[%(levelname)s|%(name)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

def create_logger(logger_name):
    logger = logging.getLogger(logger_name)
    if len(logger.handlers) > 0:
        print("Logger already exists")
        return logger  # Logger already exists
    print("Create Logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(logstash.TCPLogstashHandler('localhost', 5044, version=1))

    return logger
