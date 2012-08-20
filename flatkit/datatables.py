import flask
import flask.views


class FilterView(flask.views.View):

    def __init__(self, data=[]):
        self.data = data

    def filter_data(self, offset=0, limit=None):
        end = None if limit is None else offset + limit
        return self.data[offset:end]

    def count_data(self, **kwargs):
        return len(list(self.filter_data(**kwargs)))

    def dispatch_request(self, **kwargs):
        args = flask.request.args
        columns = args['sColumns'].split(',')
        offset = args.get('iDisplayStart', 0, type=int)
        limit = args.get('iDisplayLength', 10, type=int)
        table_data = [[row.get(key) for key in columns]
                      for row in self.filter_data(offset, limit, **kwargs)]
        return flask.jsonify({
            'iTotalRecords': self.count_data(**kwargs),
            'aaData': table_data,
        })
