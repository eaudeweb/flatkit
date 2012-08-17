import flask


class ValuesFromTable(object):

    def __init__(self, table, field):
        self.table = table
        self.field = field

    def __get__(self, ob, cls):
        session = flask.current_app.extensions['htables'].session
        return [row[self.field] for row in
                session[self.table].find()]
