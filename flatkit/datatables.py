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
            'order_by': (),
        }
        no_filter = {
            'search': '',
        }

        number_of_sorting_cols = args.get('iSortingCols', 0, type=int)
        if number_of_sorting_cols > 0:
            columns = args['sColumns'].split(',')
            column = columns[args.get('iSortCol_0', 0, type=int)]
            direction = args.get('sSortDir_0', 'asc', type=str)
            with_filter['order_by'] = (column, direction)

        table_data = [[row.get(key) for key in columns] for row in
                      self.query(dict(with_filter, **get_rows), **kwargs)]

        count_filtered = self.query(dict(with_filter, **get_limit), **kwargs)
        count_total = self.query(dict(no_filter, **get_limit), **kwargs)

        return flask.jsonify({
            'iTotalRecords': count_total,
            'iTotalDisplayRecords': count_filtered,
            'aaData': table_data,
        })
