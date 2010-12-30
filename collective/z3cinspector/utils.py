import re
from zope.dottedname.resolve import resolve as zope_resolve
from zope.interface.declarations import Implements
from zope.interface.declarations import implementedBy


def get_dotted_name(iface):
    if isinstance(iface, Implements):
        return 'implementedBy: %s' % iface.__name__
    else:
        return '.'.join((iface.__module__, iface.__name__))


def compare(query, value):
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


def resolve(path):
    """Resolve a path.
    """
    if not path:
        return None

    if path.startswith('implementedBy: '):
        foo, path = path.split('implementedBy: ')
        implementer = zope_resolve(path)
        return implementedBy(implementer)

    try:
        return zope_resolve(path)

    except ImportError:
        if path.startswith('zope.interface.declarations.'):
            path = path[len('zope.interface.declarations.'):]
            return zope_resolve(path)

        else:
            raise
