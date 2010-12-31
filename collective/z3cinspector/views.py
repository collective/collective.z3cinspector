from Products.Five import BrowserView
from collective.z3cinspector import utils
from collective.z3cinspector.config import Config
from collective.z3cinspector.registry import RegistryInspector
from collective.z3cinspector.table import TableRenderer
from collective.z3cinspector.utils import resolve
from datetime import datetime
from zope.component import getSiteManager
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

    def get_adpater_depth_range(self):
        """Maximum amount of adapter descriminators.
        """
        return range(1, len(getSiteManager().adapters._adapters) + 1)



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
        results = utils.ac_search(query, names)
        return '\n'.join(results)

    def search_name(self):
        """Search the name of a utility.
        """
        inspector = RegistryInspector(getSiteManager().utilities)

        iface_name = self.request.get('iface', None)
        query = self.request.get('q')
        provided = resolve(iface_name)

        names = inspector.get_names(provided, 0)
        results = utils.ac_search(query, names)
        return '\n'.join(results)

    def search_results(self):
        """Search the registry.
        """
        inspector = RegistryInspector(getSiteManager().utilities)

        iface_name = self.request.get('interface')
        provided = resolve(iface_name)
        name = self.request.get('name')

        adapters = inspector.get_adapters(provided, (), name)

        renderer = TableRenderer(self.context, self.request)
        return renderer(adapters, show_descriminators=False)


class SearchAdapter(BrowserView):
    """Adapter searching ajax stuff.
    """

    def search_interface(self):
        """Search an interface dotted name with autocomplete.
        """
        inspector = RegistryInspector(getSiteManager().adapters)
        query = self.request.get('q')
        names = inspector.get_provided_names(-1)
        results = utils.ac_search(query, names)
        return '\n'.join(results)

    def search_name(self):
        """Search the name of a adapter.
        """
        inspector = RegistryInspector(getSiteManager().adapters)

        iface_name = self.request.get('iface', None)
        query = self.request.get('q')
        provided = resolve(iface_name)

        names = inspector.get_names(provided, -1)
        results = utils.ac_search(query, names)
        return '\n'.join(results)

    def search_for(self):
        """Search for interface name.
        """
        inspector = RegistryInspector(getSiteManager().adapters)

        iface_name = self.request.get('iface', None)
        provided = resolve(iface_name)
        name = self.request.get('name')
        level = int(self.request.get('level'))
        query = self.request.get('q')

        names = inspector.get_keys_at_level(level, provided, name)
        results = utils.ac_search(query, names)
        return '\n'.join(results)

    def search_results(self):
        """Search the registry.
        """
        inspector = RegistryInspector(getSiteManager().adapters)

        iface_name = self.request.get('interface')
        provided = resolve(iface_name)
        name = self.request.get('name')

        descriminators = []
        desc_keys = filter(lambda x: x.startswith('descriminator:'),
                           self.request.form.keys())
        desc_keys.sort()
        any_positive = False
        for key in desc_keys:
            value = self.request.form.get(key, None)
            if value:
                descriminators.append(resolve(value))
                any_positive = True
            else:
                descriminators.append(None)

        if not any_positive:
            descriminators = ()

        adapters = inspector.get_adapters(provided, descriminators, name)

        renderer = TableRenderer(self.context, self.request)
        return renderer(adapters, show_descriminators=True)
