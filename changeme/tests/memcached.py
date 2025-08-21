import argparse
from changeme import core
from .core import cli_args
from copy import deepcopy
import logging
from unittest import mock
import os
import pytest

pytestmark = pytest.mark.skip(reason="requires external services")

logger = logging.getLogger('changeme')


def reset_handlers():
    logger = logging.getLogger('changeme')
    logger.handlers = []
    core.remove_queues()


memcached_args = deepcopy(cli_args)
memcached_args['protocols'] = 'memcached'
memcached_args['target'] = '127.0.0.1'


@mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(**memcached_args))
def memcached(mock_args):
    reset_handlers()
    se = core.main()
    try:
        assert se.found_q.qsize() == 1
    except Exception as e:
        if os.environ.get('TRAVIS', None):
            raise e
        else:
            logger.warning('memcached failed')

