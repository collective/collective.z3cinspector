from zope.interface import Interface


class IAjaxAPI(Interface):
    """Public API exposed through ajax api view.
    """

    def adapter_names():
        """Returns a list of adapter names.
        """

    def adapter_provided_names():
        """Returns a list of adapter provided interface names as string.
        """

    def utility_names():
        """Returns a list of utility names.
        """

    def utility_provided_names():
        """Returns a list of utility provided interface names as string.
        """

    def list_components():
        """Returns a list of components matching the criterias passed as
        GET or POST to the request.

        Criterias:
        - adapter_name
        - adapter_provided_name
        - utility_name
        - utility_provided_name

        The format can be changed by passing ``format`` in the request.
        Possible formats: ``as_dict`` (json), ``as_text``.
        """
