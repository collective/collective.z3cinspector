def get_dotted_name(iface):
    return '.'.join((iface.__module__, iface.__name__))
