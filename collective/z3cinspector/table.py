from collective.z3cinspector import utils
from collective.z3cinspector.config import Config
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class TableRenderer(object):

    results = ViewPageTemplateFile('templates/results.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, adapters, show_descriminators=False):

        config = Config()

        headings = ['Provided', 'Name']
        if config.get('column_factory'):
            headings.append('Factory')
        if config.get('column_file'):
            headings.append('File')
        if config.get('column_line'):
            headings.append('Line')

        options = {
            'headings': headings,
            'rows': [],
            }

        for adapter in adapters:
            row = {'data': [],
                   'actions': ''}

            path, line = adapter.get_file_and_line()
            row['data'] = [
                utils.get_dotted_name(adapter.provided),
                adapter.name,
                ]

            if config.get('column_factory'):
                row['data'].append(str(adapter.factory))
            if config.get('column_file'):
                row['data'].append(path)
            if config.get('column_line'):
                row['data'].append(line)

            row['actions'] = '<input type="button" class="open" value="open" />' + \
                '<input type="hidden" name="path" value="%s" />' % path + \
                '<input type="hidden" name="line" value="%s" />' % line

            options['rows'].append(row)

        return self.results(**options)

