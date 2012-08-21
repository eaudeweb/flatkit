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
        filter_ = {
            'search': args.get('sSearch', ''),
        }
        nofilter = {
            'search': '',
        }

        table_data = [[row.get(key) for key in columns] for row in
                      self.filter_data(dict(filter_, **limit), **kwargs)]

        count_filtered = self.count_data(dict(filter_, **nolimit), **kwargs)
        count_total = self.count_data(dict(nofilter, **nolimit), **kwargs)

        return flask.jsonify({
            'iTotalRecords': count_total,
            'iTotalDisplayRecords': count_filtered,
            'aaData': table_data,
        })
