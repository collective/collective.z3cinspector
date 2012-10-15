from collective.z3cinspector.utils import get_dotted_name
import inspect
import sys
import types


class Adapter(object):
    """Adapter representation for easy usage.
    """

    def __init__(self, provided, name, descriminators, factory):
        self.provided = provided
        self.name = name
        self.descriminators = descriminators
        self.factory = factory

    def get_file_and_line(self):
        """Returns the filepath and linenumber of where the factory
        is defined.
        """

        try:
            module = self.factory.__module__
        except AttributeError:
            module = ''

        meta_modules = (
            'Products.Five.metaclass',
            'Products.Five.viewlet.metaconfigure',
            'Products.Five.viewlet.viewlet')

        if module in meta_modules:
            # We have a metaclass, e.g. a BrowserView with registered
            # template. We need to have the actual view-class which is
            # the first superclass.
            try:
                klass = inspect.getmro(self.factory)[1]
            except (AttributeError, IndexError):
                # no superclasses
                klass = self.factory.__class__

        elif inspect.isclass(self.factory):
            klass = self.factory
        elif inspect.isfunction(self.factory):
            klass = self.factory
        elif inspect.ismethod(self.factory):
            klass = self.factory
        else:
            klass = self.factory.__class__

        try:
            inspect.getsource(klass)
        except IOError:
            pass
        except TypeError:
            klass = self.factory.__class__
        except:
            return str(sys.exc_info()[1]) + ': ' + str(self.factory), '-'

        try:
            return inspect.getsourcefile(klass), \
                inspect.getsourcelines(klass)[1]
        except:
            return str(sys.exc_info()[1]) + ': ' + str(self.factory), '-'

    @classmethod
    def from_registry(cls, dict_, path=[]):
        """Create multiple adapters from registry dicts.
        `path` is a list of already walked-trough keys.
        """
        adapters = []

        for key, value in dict_.items():
            if isinstance(value, dict):
                # step into next level
                adapters.extend(cls.from_registry(value, path + [key]))

            else:
                # most inner level reached
                if not path:
                    raise RuntimeError('Expected a provided interface.')
                provided = path[-1]
                descriminators = path[:-1]
                adapters.append(cls(
                        provided=provided,
                        name=key,
                        descriminators=descriminators,
                        factory=value))

        return adapters

    def as_dict(self):
        path, line = self.get_file_and_line()
        return {'name': self.name,
                'provided': get_dotted_name(self.provided),
                'descriminators': [get_dotted_name(iface)
                                   for iface in self.descriminators],
                'factory': str(self.factory),
                'path': path,
                'line': line,
                }

    def as_text(self):
        path, line = self.get_file_and_line()

        data = [':'.join((path, str(line))),
                'Name:      %s' % self.name,
                'Provides:  %s' % get_dotted_name(self.provided),
                ]

        for num, iface in enumerate(self.descriminators):
            data.append('Adapts %i:  %s' % (num, get_dotted_name(iface)))

        data.append('Factory:   %s' % str(self.factory))

        return '\n'.join(data)


class RegistryInspector(object):
    """Access the component registry.

    The "scope" is the amount of descriminators. A utility has usually
    a scope of 0, a normal adapter has 1 and a multi-adapter has 2 or
    more. If the scope is -1, all scopes are used.
    """

    def __init__(self, registry):
        self.registry = registry

    def get_provided_names(self, scope=-1):
        """Returns a list of interface names of provided interfaces.
        """

        def _inner_keys(dict_):
            # The keys of the most inner dicts are the names of the
            # adapters (or utilities) - we need to have the dotted
            # names of the dicts one level above.
            keys = []
            for key, value in dict_.items():
                if isinstance(key, types.StringTypes):
                    return -1
                sub = _inner_keys(value)
                if sub == -1:
                    keys.append(get_dotted_name(key))

                else:
                    keys.extend(sub)
            return keys

        names = []
        if scope > -1:
            names = _inner_keys(self.registry._adapters[scope])

        else:
            names = []
            for all in self.registry._adapters:
                names.extend(_inner_keys(all))

        names = list(set(names))
        names.sort()
        return names


    def get_names(self, provided=None, scope=-1):
        """Return all known names. The `provided` interface is optional.
        """

        def _inner_keys(dict_):
            # we need to get the keys of the most inner dicts.
            keys = []
            for key, value in dict_.items():
                if isinstance(value, dict):
                    keys.extend(_inner_keys(value))
                else:
                    keys.append(key)
            return keys

        if scope > -1:
            all = self.registry._adapters[scope]
            if not provided:
                return _inner_keys(all)
            elif provided in all:
                return _inner_keys(all[provided])
            else:
                return []

        else:
            names = []
            for all in self.registry._adapters:
                if not provided:
                    names.extend(_inner_keys(all))
                elif provided in all:
                    names.extend(_inner_keys(all[provided]))

            return set(names)

    def get_keys_at_level(self, level, provided=None, name=None):
        """Returns all keys at a specific level
        """

        def _get_keys(dict_, path=[]):
            # walk into the dicts till to the end. The last key
            # in the path is the name, the second last is the
            # provided interface.
            keys = []
            for key, value in dict_.items():
                if isinstance(value, dict):
                    # continue walking
                    keys.extend(_get_keys(value, path + [key]))

                else:
                    if name and name != key:
                        # name does not match
                        continue
                    if provided and provided != path[-1]:
                        # provided does not match
                        continue
                    keys.append(path[level])

            return keys

        keys = []
        for all in self.registry._adapters:
            keys.extend(_get_keys(all))

        keys = list(set(keys))
        keys = [get_dotted_name(key) for key in keys]
        keys.sort()

        return keys

    def get_adapters(self, provided=None, descriminators=None, name=None):
        """All adapters which mach the given criterions.
        `scope` is the amount of descriminators.
        """

        def _match_path(path, dict_):
            if not len(path):
                return dict_

            results = {}
            next = path[0]

            if next and next in dict_:
                subdict = _match_path(path[1:], dict_.get(next))
                if subdict:
                    results[next] = subdict
                return results

            if next:
                return None

            for key, value in dict_.items():
                subdict = _match_path(path[1:], value)
                if subdict:
                    results[key] = subdict

            return results

        if descriminators:
            results = {}
            for scope, all in enumerate(self.registry._adapters):
                path = descriminators[:scope] + [provided, name]
                subdict = _match_path(path, all)
                if subdict:
                    results.update(subdict)

            return Adapter.from_registry(results)

        else:
            results = {}
            for scope, all in enumerate(self.registry._adapters):
                path = [None for i in range(scope)] + [provided, name]
                subdict = _match_path(path, all)
                if subdict:
                    results.update(subdict)

            return Adapter.from_registry(results)
