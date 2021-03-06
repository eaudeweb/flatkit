import unittest
import flask
from flatkit.testing import FlaskTestCase


DATA = [
    {'n': "1", 'name': "flask", 'language': "python"},
    {'n': "2", 'name': "django", 'language': "python"},
    {'n': "3", 'name': "zope", 'language': "python"},
    {'n': "4", 'name': "sinatra", 'language': "ruby"},
    {'n': "5", 'name': "rails", 'language': "ruby"},
    {'n': "6", 'name': "merb", 'language': "ruby"},
]


class TableEnumTest(FlaskTestCase):

    def from_json(self, resp):
        self.assertEqual(resp.status_code, 200)
        return flask.json.loads(resp.data)

    def setUp(self):
        from flatkit.datatables import FilterView

        class MockFilterView(FilterView):

            def __init__(self, data=[]):
                self.data = data

            def query(self, options):
                offset = options['offset']
                limit = options['limit']
                search = options['search']
                count = options['count']
                end = None if limit is None else offset + limit
                filtered = [d for d in self.data if search in d['name']]
                result = filtered[offset:end]
                if count:
                    return len(result)
                else:
                    return iter(result)

        table_filter = MockFilterView.as_view('table_filter', data=DATA)
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

    def test_view_returns_count_of_full_collection(self):
        resp = self.client.get('/filter?sColumns=n,name')
        resp_data = self.from_json(resp)
        self.assertEqual(resp_data['iTotalRecords'], 6)
        self.assertEqual(resp_data['iTotalDisplayRecords'], 6)

    def test_view_sends_kwargs_to_filter(self):
        from flatkit.datatables import FilterView

        class MyFilterView(FilterView):

            def query(self, options, name=None):
                assert name is not None
                if options['count']:
                    return 1
                return [{'msg': "my name is %s" % name}]

        view = MyFilterView.as_view('some_filter')
        self.app.add_url_rule('/<string:name>/filter', view_func=view)
        resp_data = self.from_json(self.client.get('/red/filter?sColumns=msg'))
        self.assertEqual(resp_data['aaData'], [['my name is red']])

    def test_string_search_returns_filtered_results(self):
        resp = self.client.get('/filter?sColumns=n,name'
                                      '&sSearch=ra')
        resp_data = self.from_json(resp)
        self.assertEqual(resp_data['aaData'], [
            ["4", "sinatra"],
            ["5", "rails"],
        ])

    def test_limited_string_search_returns_good_total_and_partial_counts(self):
        resp = self.client.get('/filter?sColumns=n,name'
                                      '&sSearch=ra'
                                      '&iDisplayLength=1')
        resp_data = self.from_json(resp)
        self.assertEqual(resp_data['iTotalRecords'], 6)
        self.assertEqual(resp_data['iTotalDisplayRecords'], 2)
        self.assertEqual(len(resp_data['aaData']), 1)
