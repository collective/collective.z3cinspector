from Products.Five import BrowserView
from collective.z3cinspector.config import Config
from collective.z3cinspector.table import TableRenderer
from collective.z3cinspector.registry import RegistryInspector
from collective.z3cinspector import utils
from datetime import datetime
from zope.component import getSiteManager
from zope.dottedname.resolve import resolve
import os


class InspectView(BrowserView):
    """View used for inspecting the zope3 component registry.
    """

    def get_js_url(self):
        base_url = '/++resource++collective.z3cinspector-inspector.js'
        return base_url + '?x=' + str(datetime.now())

    def get_css_url(self):
        base_url = '/++resource++collective.z3cinspector-inspector.css'
        return base_url + '?x=' + str(datetime.now())

    def get_config(self):
        return Config()._config


class SaveConfigView(BrowserView):
    """Save the configuration.
    """

    def __call__(self):
        """Save the configuration with ajax.
        """
        config = Config()
        for key, value in self.request.form.items():
            config.set(key, value)


class OpenView(BrowserView):
    """View for opening a source file in the editor. Only use this when
    running zope on your local machine.
    """

    def __call__(self):
        path = self.request.get('path')
        line = self.request.get('line')
        params = {'path': path,
                  'line': line}

        # read the config file, if existing
        config = Config()
        command = config.get('open_command') % params
        os.system(command)


class SearchUtility(BrowserView):
    """Utility searching ajax stuff.
    """

    def search_interface(self):
        """Search an interface dotted name with autocomplete.
        """
        inspector = RegistryInspector(getSiteManager().utilities)
        query = self.request.get('q')
        names = inspector.get_provided_names(0)
        results = filter(lambda value: utils.compare(query, value),
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
        results = filter(lambda value: utils.compare(query, value),
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

        renderer = TableRenderer(self.context, self.request)
        return renderer(adapters, show_descriminators=False)
