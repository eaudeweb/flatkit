import flask
import flask.views


class FilterView(flask.views.View):

    def query(self, options, **kwargs):
        raise NotImplementedError

    def dispatch_request(self, **kwargs):
        args = flask.request.args
        columns = args['sColumns'].split(',')
        get_rows = {
            'offset': args.get('iDisplayStart', 0, type=int),
            'limit': args.get('iDisplayLength', 10, type=int),
            'count': False,
        }
        get_limit = {
            'offset': 0,
            'limit': None,
            'count': True,
        }
        with_filter = {
            'search': args.get('sSearch', ''),
        }
        no_filter = {
            'search': '',
        }

        table_data = [[row.get(key) for key in columns] for row in
                      self.query(dict(with_filter, **get_rows), **kwargs)]

        count_filtered = self.query(dict(with_filter, **get_limit), **kwargs)
        count_total = self.query(dict(no_filter, **get_limit), **kwargs)

        return flask.jsonify({
            'iTotalRecords': count_total,
            'iTotalDisplayRecords': count_filtered,
            'aaData': table_data,
        })
