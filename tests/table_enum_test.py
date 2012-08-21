import unittest
import flask
import flask_htables
from flatkit.testing import FlaskTestCase


class TableEnumTest(FlaskTestCase):

    def setUp(self):
        self.app.config.update(HTABLES_ENGINE='sqlite',
                               HTABLES_SQLITE_PATH=':memory:')
        self.ht = flask_htables.HTables(self.app)

    def test_two_values_fetched_from_database(self):
        from flatkit.schema import ValuesFromTable

        class Thing(object):
            valid_values = ValuesFromTable('person', field='slug')

        with self.app.test_request_context():
            person_table = self.ht.session['person']
            person_table.create_table()
            person_table.new(slug='red')
            person_table.new(slug='blue')

            thing = Thing()
            self.assertItemsEqual(thing.valid_values, ['red', 'blue'])

    def test_multiple_fetches_call_htables_only_once(self):
        from flatkit.schema import ValuesFromTable

        class Thing(object):
            valid_values = ValuesFromTable('person', field='slug')

        thing = Thing()

        with self.app.test_request_context():
            person_table = self.ht.session['person']
            person_table.create_table()
            person_table.new(slug='red')
            thing.valid_values
            person_table.new(slug='blue')

            self.assertItemsEqual(thing.valid_values, ['red'])

    def test_dict_fetched_from_database(self):
        from flatkit.schema import DictFromTable

        class Thing(object):
            value_labels = DictFromTable('person', key_field='slug',
                                                   value_field='label')

        with self.app.test_request_context():
            person_table = self.ht.session['person']
            person_table.create_table()
            person_table.new(slug='red', label="Color Red")

            thing = Thing()
            self.assertItemsEqual(thing.value_labels, {'red': "Color Red"})

    def test_dict_fetched_from_database_with_primary_key_as_key(self):
        from flatkit.schema import DictFromTable

        class Thing(object):
            value_labels = DictFromTable('person', value_field='label')

        with self.app.test_request_context():
            person_table = self.ht.session['person']
            person_table.create_table()
            person_table.new(label="Red")
            person_table.new(label="Blue")

            thing = Thing()
            self.assertItemsEqual(thing.value_labels, {1: "Red", 2: "Blue"})
