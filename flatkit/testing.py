import unittest
from werkzeug.datastructures import ImmutableDict
import flask

__test__ = False


class FlaskTestCase(unittest.TestCase):

    APP_CONFIG = ImmutableDict(TESTING=True)

    def _pre_setup(self):
        self.app = flask.Flask(__name__)
        self.app.config.update(self.APP_CONFIG)

    def __call__(self, result=None):
        self._pre_setup()
        super(FlaskTestCase, self).__call__(result)
