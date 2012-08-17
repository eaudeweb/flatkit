import unittest
import flask
import flask_htables


class TableEnumTest(unittest.TestCase):

    def test_two_values_fetched_from_database(self):
        from flatkit import ValuesFromTable

        class Thing(object):
            valid_values = ValuesFromTable('person', field='slug')

        app = flask.Flask(__name__)
        app.config.update(HTABLES_ENGINE='sqlite',
                          HTABLES_SQLITE_PATH=':memory:')
        ht = flask_htables.HTables(app)

        with app.test_request_context():
            person_table = ht.session['person']
            person_table.create_table()
            person_table.new(slug='red')
            person_table.new(slug='blue')

            thing = Thing()
            self.assertItemsEqual(thing.valid_values, ['red', 'blue'])
