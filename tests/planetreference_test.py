import pytest

import planetreference
import logging

def test_name():
    name = planetreference.__name_soft__
    assert name == "planetreference"

def test_logger():
    loggers = [logging.getLogger()]
    loggers = loggers + [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    assert loggers[0].name == "root"
    assert loggers[1].name == "planetreference"