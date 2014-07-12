"""Defines fixtures available to all tests."""
import pytest
from webtest import TestApp

from config import TestConfig
from web import create_app
from data.db import db as _db

@pytest.yield_fixture(scope='session')
def app():
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()

@pytest.fixture(scope='function')
def client(app):
    """A Webtest app."""
    return TestApp(app)

@pytest.yield_fixture(scope='function')
def db(app):
    _db.create_all()

    yield _db

    _db.session.remove()
    _db.drop_all()
