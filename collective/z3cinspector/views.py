from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.z3cinspector.registry import RegistryInspector
from collective.z3cinspector.utils import get_dotted_name
from datetime import datetime
from zope.component import getSiteManager
from zope.dottedname.resolve import resolve
import re


class InspectView(BrowserView):
    """View used for inspecting the zope3 component registry.
    """

    def get_js_url(self):
        base_url = '/++resource++collective.z3cinspector-inspector.js'
        return base_url + '?x=' + str(datetime.now())

    def get_css_url(self):
        base_url = '/++resource++collective.z3cinspector-inspector.css'
        return base_url + '?x=' + str(datetime.now())


class SearchBase(BrowserView):
    """Base search class.
    """

    results = ViewPageTemplateFile('templates/results.pt')

    def _compare(self, query, value):
        """ Compares each word in the query string seperate.
        """

        if not value:
            return False

        xpr = re.compile('[\s\.]')
        query = xpr.split(query.lower())
        value = value.lower()

        for word in query:
            if len(word)>0 and word not in value:
                return False
        return True


class SearchUtility(SearchBase):
    """Utility searching ajax stuff.
    """

    def search_interface(self):
        """Search an interface dotted name with autocomplete.
        """
        inspector = RegistryInspector(getSiteManager().utilities)
        query = self.request.get('q')
        names = inspector.get_provided_names(0)
        results = filter(lambda value: self._compare(query, value),
                         names)
        return '\n'.join(results)

    def search_name(self):
        """Search the name of a utility.
        """
        inspector = RegistryInspector(getSiteManager().utilities)

        iface_name = self.request.get('iface', None)
        query = self.request.get('q')
        if iface_name:
            provided = resolve(iface_name)
        else:
            provided = None

        names = inspector.get_names(provided, 0)
        results = filter(lambda value: self._compare(query, value),
                         names)
        return '\n'.join(results)

    def search_results(self):
        """Search the registry.
        """
        inspector = RegistryInspector(getSiteManager().utilities)

        iface_name = self.request.get('interface')
        if iface_name:
            provided = resolve(iface_name)
        else:
            provided = None
        name = self.request.get('name')

        adapters = inspector.get_adapters(provided, (), name)

        options = {
            'headings': ['Provided', 'Name', 'Factory', 'File', 'Line'],
            'rows': [],
            }

        for adapter in adapters:
            path, line = adapter.get_file_and_line()
            options['rows'].append([
                    get_dotted_name(adapter.provided),
                    adapter.name,
                    str(adapter.factory),
                    path,
                    line,
                    ])

        return self.results(**options)
