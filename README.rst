Introduction
============

The zope3 component registry inspector is used for inspecting adapters
and utilities registered in the z3 component registry. It provides a view
registred on the app level for searching and inspecting the registry.


Features
========

* Searching for utilities
* Searching for adapters
* Searching interfaces and names using auto-complete widget
* Open factory source file with your favourite editor (if the Zope is installed on localhost)
* Customize file opening command
* Access tabs with hotkeys (Ctrl+u, Ctrl+a, Ctrl+c)


Installation
============

Install it using buildout with Plone > 4.0::

    [buildout]
    ...

    [instance]
    ...
    eggs +=
        collective.z3cinspector


Install it using buildout with Plone < 4.0::

    [buildout]
    ...

    [instance]
    ...
    eggs +=
        collective.z3cinspector
    zcml +=
        collective.z3cinspector


Usage
=====

While being logged into the ZMI as a Manager user goto /@@inspect on your Zope
application root via a browser. If your Zope is configured to listen on port
8080 on localhost this is::

    http://localhost:8080/@@inspect



Configuration
=============

The configuration is stored in the file `~/.collective.z3cinspector.config`. The
options are configurable through the @@inspect view. This way you only have to set
your preferred configuration once - and it will be configured in every zope instance
on your machine.

When clicking on the "open" button in the results listing, your Editor will be
opened with the file containing the factory definition. You may wan't to configure
how the Editor is opened. There are some pre-configured Editors: `Emacs`, `MacVim`
and `TextMate`, the default to open the file is using the `open` command. The path
and the line number (option) is substituted (python).

Example command::

    /path/to/your/editor %(path)s -l %(line)s


JSON-API
========

There is a JSON api for easy integration in editors.
The view ``@@inspector-ajax`` has following (traversable) methods:

``adapter_names``
    Returns a list of adapter names.

``adapter_provided_names``
    Returns a list of adapter provided interface names as string.

``utility_names``
    Returns a list of utility names.

``utility_provided_names``
    Returns a list of utility provided interface names as string.

``list_components``
    Returns a list of components matching the criterias passed as
    GET or POST to the request.

    Criterias:

    - adapter_name
    - adapter_provided_name
    - utility_name
    - utility_provided_name

    The format can be changed by passing ``format`` in the request.
    Possible formats: ``as_dict`` (json), ``as_text``.


License
=======

"THE BEER-WARE LICENSE" (Revision 42):

jone_ wrote this script. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return.


.. _`jone`: http://github.com/jone
