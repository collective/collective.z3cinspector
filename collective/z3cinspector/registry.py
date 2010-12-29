from collective.z3cinspector.utils import get_dotted_name
import inspect


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

        if inspect.isclass(self.factory):
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

        try:
            return inspect.getsourcefile(klass), \
                inspect.getsourcelines(klass)[1]
        except (IOError, TypeError), e:
            return str(e) + ':' + str(self.factory), ''

    @classmethod
    def from_registry(cls, dict_, path=[]):
        """Create multiple adapters from registry dicts.
        `path` is a list of already walked-trough keys.
        """
        adapters = []
        descriminators = len(path) and path[:] or []
        provided = len(descriminators) and descriminators.pop(0) or None

        for key, value in dict_.items():
            if isinstance(value, dict):
                # step into next level
                adapters.extend(cls.from_registry(value, path + [key]))

            else:
                # most inner level reached
                if not provided:
                    raise RuntimeError('Expected a provided interface.')
                adapters.append(cls(
                        provided=provided,
                        name=key,
                        descriminators=descriminators,
                        factory=value))

        return adapters


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

        provided = []

        if scope > -1:
            provided.extend(self.registry._adapters[scope].keys())

        else:
            for ascope, adapters in enumerate(self.registry._adapters):
                provided.extend(adapters.keys())

        # uniquify
        provided = list(set(provided))

        # convert to dotted names
        for iface in provided:
            yield get_dotted_name(iface)

    def get_adapters_by_provided_interface(self, provided, scope=-1):
        """All adapters which provide a specific interface.
        """

        if scope > -1:
            all = self.registry._adapters[scope]
            if provided in all:
                return Adapter.from_registry(all[provided], [provided])

        else:
            adapters = []
            for all in self.registry._adapter:
                if provided in all:
                    adapters.extend(list(Adapter.from_registry(
                                all[provided], [provided])))

            return adapters

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

            return names

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
            path = [provided] + descriminators + [name]
            results = _match_path(
                path, self.registry._adapters[len(descriminators)])
            return Adapter.from_registry(results)

        else:
            results = {}
            for scope, all in enumerate(self.registry._adapters):
                path = [provided] + [None for i in range(scope)] + [name]
                subdict = _match_path(path, all)
                if subdict:
                    results.update(subdict)

            return Adapter.from_registry(results)
