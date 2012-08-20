import flask
import flask.views


class FilterView(flask.views.View):

    def filter_data(self, offset, limit):
        raise NotImplementedError

    def count_data(self, **kwargs):
        return len(list(self.filter_data(0, None, **kwargs)))

    def dispatch_request(self, **kwargs):
        args = flask.request.args
        columns = args['sColumns'].split(',')
        offset = args.get('iDisplayStart', 0, type=int)
        limit = args.get('iDisplayLength', 10, type=int)
        table_data = [[row.get(key) for key in columns]
                      for row in self.filter_data(offset, limit, **kwargs)]
        count_total = self.count_data(**kwargs)
        return flask.jsonify({
            'iTotalRecords': count_total,
            'iTotalDisplayRecords': count_total,
            'aaData': table_data,
        })
