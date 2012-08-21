import flask


def get_request_cache():
    if not hasattr(flask.g, '_flatkit_cache'):
        flask.g._flatkit_cache = {}
    return flask.g._flatkit_cache


class ValuesFromTable(object):

    def __init__(self, table, field):
        self.table = table
        self.field = field

    def __get__(self, ob, cls):
        cache = get_request_cache()
        key = (self,)
        if key not in cache:
            session = flask.current_app.extensions['htables'].session
            ret = [row[self.field] for row in
                   session[self.table].find()]
            cache[key] = ret
        return cache[key]


class DictFromTable(object):

    def __init__(self, table, key_field, value_field):
        self.table = table
        self.key_field = key_field
        self.value_field = value_field

    def __get__(self, ob, cls):
        cache = get_request_cache()
        key = (self,)
        if key not in cache:
            session = flask.current_app.extensions['htables'].session
            ret = dict((row[self.key_field], row[self.value_field])
                       for row in session[self.table].find())
            cache[key] = ret
        return cache[key]
