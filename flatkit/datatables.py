import flask
import flask.views


class FilterView(flask.views.View):

    def filter_data(self, options, **kwargs):
        raise NotImplementedError

    def count_data(self, options, **kwargs):
        return len(list(self.filter_data(options, **kwargs)))

    def dispatch_request(self, **kwargs):
        args = flask.request.args
        columns = args['sColumns'].split(',')
        limit = {
            'offset': args.get('iDisplayStart', 0, type=int),
            'limit': args.get('iDisplayLength', 10, type=int),
        }
        nolimit = {
            'offset': 0,
            'limit': None,
        }

        table_data = [[row.get(key) for key in columns] for row in
                      self.filter_data(limit, **kwargs)]

        count_total = self.count_data(nolimit, **kwargs)

        return flask.jsonify({
            'iTotalRecords': count_total,
            'iTotalDisplayRecords': count_total,
            'aaData': table_data,
        })
