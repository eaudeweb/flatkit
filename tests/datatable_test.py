import unittest
import flask
import flask.views
from flatkit.testing import FlaskTestCase


class DataTablesFilterView(flask.views.View):

    def filter_data(self, offset, limit):
        data = [
            {'n': "1", 'name': "flask", 'language': "python"},
            {'n': "2", 'name': "django", 'language': "python"},
            {'n': "3", 'name': "zope", 'language': "python"},
            {'n': "4", 'name': "sinatra", 'language': "ruby"},
            {'n': "5", 'name': "rails", 'language': "ruby"},
            {'n': "6", 'name': "merb", 'language': "ruby"},
        ]
        end = offset + limit
        return data[offset:end]

    def dispatch_request(self):
        args = flask.request.args
        columns = args['sColumns'].split(',')
        offset = args.get('iDisplayStart', 0, type=int)
        limit = args.get('iDisplayLength', 10, type=int)
        table_data = [[row.get(key) for key in columns]
                      for row in self.filter_data(offset, limit)]
        return flask.jsonify({
            'aaData': table_data,
        })


class TableEnumTest(FlaskTestCase):

    def from_json(self, resp):
        self.assertEqual(resp.status_code, 200)
        return flask.json.loads(resp.data)

    def setUp(self):
        table_filter = DataTablesFilterView.as_view('table_filter')
        self.app.route('/filter')(table_filter)
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
