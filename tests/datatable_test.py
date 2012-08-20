import unittest
import flask
from flatkit.testing import FlaskTestCase


class TableEnumTest(FlaskTestCase):

    def from_json(self, resp):
        self.assertEqual(resp.status_code, 200)
        return flask.json.loads(resp.data)

    def setUp(self):
        data = [
            {'n': "1", 'name': "flask", 'language': "python"},
            {'n': "2", 'name': "django", 'language': "python"},
            {'n': "3", 'name': "zope", 'language': "python"},
            {'n': "4", 'name': "sinatra", 'language': "ruby"},
            {'n': "5", 'name': "rails", 'language': "ruby"},
            {'n': "6", 'name': "merb", 'language': "ruby"},
        ]
        @self.app.route('/filter')
        def table_filter():
            args = flask.request.args
            columns = args['sColumns'].split(',')
            window_offset = args.get('iDisplayStart', 0, type=int)
            window_limit = args.get('iDisplayLength', 10, type=int)
            window_end = window_offset + window_limit
            table_data = [[row.get(key) for key in columns] for row in data]
            table_data = table_data[window_offset:window_end]
            return flask.jsonify({
                'aaData': table_data,
            })
        self.client = self.app.test_client()

    def test_filter_with_columns_returns_only_those_columns(self):
        resp = self.client.get('/filter?sColumns=n,name')
        resp_data = self.from_json(resp)
        self.assertEqual(resp_data['aaData'], [
            ["1", "flask"],
            ["2", "django"],
            ["3", "zope"],
            ["4", "sinatra"],
            ["5", "rails"],
            ["6", "merb"],
        ])

    def test_filter_with_limit_2_returns_first_2_rows(self):
        resp = self.client.get('/filter?sColumns=n,name&iDisplayLength=2')
        resp_data = self.from_json(resp)
        self.assertEqual(resp_data['aaData'], [
            ["1", "flask"],
            ["2", "django"],
        ])

    def test_filter_with_offset_2_returns_middle_2_rows(self):
        resp = self.client.get('/filter?sColumns=n,name'
                                      '&iDisplayLength=2'
                                      '&iDisplayStart=2')
        resp_data = self.from_json(resp)
        self.assertEqual(resp_data['aaData'], [
            ["3", "zope"],
            ["4", "sinatra"],
        ])
