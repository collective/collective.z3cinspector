from collective.z3cinspector import utils
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class TableRenderer(object):

    results = ViewPageTemplateFile('templates/results.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, adapters, show_descriminators=False):

        options = {
            'headings': ['Provided', 'Name', 'Factory', 'File', 'Line'],
            'rows': [],
            }

        for adapter in adapters:
            row = {'data': [],
                   'actions': ''}

            path, line = adapter.get_file_and_line()
            row['data'] = [
                utils.get_dotted_name(adapter.provided),
                adapter.name,
                str(adapter.factory),
                path,
                line,
                ]

            row['actions'] = '<input type="button" class="open" value="open" />' + \
                '<input type="hidden" name="path" value="%s" />' % path + \
                '<input type="hidden" name="line" value="%s" />' % line

            options['rows'].append(row)

        return self.results(**options)

