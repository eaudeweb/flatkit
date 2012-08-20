import flask
import flask.views


class FilterView(flask.views.View):

    def __init__(self, data=[]):
        self.data = data

    def filter_data(self, offset, limit):
        end = offset + limit
        return self.data[offset:end]

    def dispatch_request(self, **kwargs):
        args = flask.request.args
        columns = args['sColumns'].split(',')
        offset = args.get('iDisplayStart', 0, type=int)
        limit = args.get('iDisplayLength', 10, type=int)
        table_data = [[row.get(key) for key in columns]
                      for row in self.filter_data(offset, limit, **kwargs)]
        return flask.jsonify({
            'aaData': table_data,
        })
