import re


def get_dotted_name(iface):
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
