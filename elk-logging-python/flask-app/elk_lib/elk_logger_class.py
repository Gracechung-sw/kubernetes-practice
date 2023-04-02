import logging
import logstash
import sys
import time

class Logging():
    def __init__(self, logger_name: str, log_stash_host='localhost', log_stash_port=5044):
        self.logger_name = logger_name
        self.log_stash_host = log_stash_host
        self.log_stash_port = log_stash_port

    def create_logger(self, file_name: str) -> logging.Logger:
        logging.basicConfig(
            filename=file_name,
            format="\n[%(levelname)s|%(name)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s",
            datefmt="%H:%M:%S",
            level=logging.INFO,
        )
        logger = logging.getLogger(self.logger_name)
        if len(logger.handlers) > 0:
          print("Logger already exists")
          return logger  # Logger already exists
        logger.addHandler(logstash.TCPLogstashHandler(self.log_stash_host, self.log_stash_port, version=1))
        return logger
