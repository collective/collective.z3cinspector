from Products.Five import BrowserView
from datetime import datetime


class InspectView(BrowserView):
    """View used for inspecting the zope3 component registry.
    """

    def get_js_url(self):
        base_url = '/++resource++collective.z3cinspector-inspector.js'
        return base_url + '?x=' + str(datetime.now())

    def get_css_url(self):
        base_url = '/++resource++collective.z3cinspector-inspector.css'
        return base_url + '?x=' + str(datetime.now())
