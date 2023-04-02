from flask import Blueprint

from elk_lib.elk_logger_class import Logging

elk_test = Blueprint('elk_test', __name__)


@elk_test.route('/', methods=['GET'])
def elk_test_show():
    instance = Logging('DeepDx Connect')
    logger = instance.create_logger('dxc-viewer')

    logger.info('hello elk-test-logstash~~~~~')

    return "hello world~~~~~"