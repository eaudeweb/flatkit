import unittest
import flask
import flask_htables


class TableEnumTest(unittest.TestCase):

    def setUp(self):
        self.app = flask.Flask(__name__)
        self.app.config.update(HTABLES_ENGINE='sqlite',
                               HTABLES_SQLITE_PATH=':memory:')
        self.ht = flask_htables.HTables(self.app)

    def test_two_values_fetched_from_database(self):
        from flatkit import ValuesFromTable

        class Thing(object):
            valid_values = ValuesFromTable('person', field='slug')

        with self.app.test_request_context():
            person_table = self.ht.session['person']
            person_table.create_table()
            person_table.new(slug='red')
            person_table.new(slug='blue')

            thing = Thing()
            self.assertItemsEqual(thing.valid_values, ['red', 'blue'])
