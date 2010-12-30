import os.path


try:
    import json
except ImportError:
    import simplejson as json


CONFIG_FILE = os.path.expanduser('~/.collective.z3cinspector.config')


class Config(object):
    """The configuration is stored in ~/.collective.z3cinspector.config. This
    makes it possible to store the configuration per user for every zope
    installation.
    """

    def __init__(self):
        if os.path.isfile(CONFIG_FILE):
            self._config = json.loads(open(CONFIG_FILE).read())
        else:
            self._config = self._defaults()

    def _defaults(self):
        return {'open_command': 'open %(path)s',
                'column_factory': False,
                'column_file': True,
                'column_line': True}

    def get(self, key, default=None):
        return self._config.get(key, default)

    def set(self, key, value):
        self._config[key] = value
        self.save()

    def save(self):
        data = json.dumps(self._config)
        file_ = open(CONFIG_FILE, 'w')
        file_.write(data)
        file_.close()
