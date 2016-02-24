import copy
import inspect


class PyMapper(object):
    def __init__(self):
        self._ignore_props = set()
        self._prop_maps = {}
        self._list_obj = {}
        self._after_map_func = None
        self._map_strategies = dict()
        self._map_strategies['obj_obj'] = self._map_obj_obj
        self._map_strategies['dict_obj'] = self._map_dict_obj
        self._map_strategies['obj_dict'] = self._map_obj_dict
        self._map_strategies['dict_dict'] = self._map_dict_dict

    def ignore(self, dest_func):
        inspected = inspect.getsource(dest_func)
        key = inspected.split('d: ')[1].split(')')[0].strip()
        self._ignore_props.add(key)

        return self

    def property_set(self, src_func, dest_func):
        inspected = inspect.getsource(dest_func)
        key = inspected.split('d: ')[1].split(')')[0].strip()
        self._ignore_props.add(key)
        self._prop_maps[key] = {'src_func': src_func, 'value': None}

        return self

    def list_set_class(self, dest_func, obj):
        inspected = inspect.getsource(dest_func)
        key = inspected.split('d: ')[1].split(')')[0].strip()
        self._list_obj[key] = obj

        return self

    def after(self, func):
        self._after_map_func = func

        return self

    def map(self, src, dest):
        prepend = 'd' if isinstance(dest, dict) else 'd.'
        prop_maps_copy = self._prop_maps.copy()
        #save values
        for src_val in prop_maps_copy.values():
            src_val['value'] = src_val['src_func'](src)
        dest = self._map(src, dest, prop_maps_copy, prepend)
        # execute after map
        if self._after_map_func is not None:
            dest = self._after_map_func(src, dest)

        return dest

    def _map(self, src, dest, prop_maps, prepend=''):
        self._map_strategies[self._get_type(src) + '_' + self._get_type(dest)](src, dest, prop_maps, prepend)

        return dest

    def _map_list(self, src, dest, prepend=''):
        if isinstance(src, list) and isinstance(dest, list):
            length = len(src)
            for idx, s in src:
                if hasattr(s, '__dict__') and hasattr(dest[idx], '__dict__') and length > idx:
                    self._map(src[idx], dest[idx], prepend + '.')
                elif prepend in self._list_obj:
                    dest.append(copy.deepcopy(self._list_obj[prepend]))
                    self._map(src[idx], dest[idx], prepend + '.')
                else:
                    dest.append(src[idx])
        else:
            raise ValueError

    def _get_type(self, arg):
        if hasattr(arg, '__dict__'):
            return 'obj'
        if isinstance(arg, dict):
            return 'dict'
        return ''

    def _map_obj_obj(self, src, dest, prop_maps,  prepend=''):
        for a in dir(dest):
            if not a.startswith('_') and \
                    not a.startswith('_') and \
                    hasattr(src, a) and \
                    prepend + a not in self._ignore_props and\
                    prepend + a not in prop_maps:
                if hasattr(getattr(dest, a), '__dict__'):
                    self._map(getattr(src, a), getattr(dest, a), prop_maps, prepend + a + '.')
                elif isinstance(getattr(dest, a), dict):
                    self._map(getattr(src, a), getattr(dest, a), prop_maps, "{0}['{1}']".format(prepend, a).strip())
                elif isinstance(getattr(dest, a), list) and \
                        isinstance(getattr(src, a), list) and \
                        prepend + a + '[x]' not in self._ignore_props:
                    setattr(dest, a, self._map_list(getattr(src, a), getattr(dest, a), prepend + a + '[0].'))
                else:
                    setattr(dest, a, getattr(src, a))

            if prepend + a in prop_maps:
                    setattr(dest, a, prop_maps[prepend + a]['value'])

        return dest

    def _map_dict_obj(self, src, dest, prop_maps, prepend=''):
        for a in dir(dest):
            if not a.startswith('_') and \
                    not callable(getattr(dest, a)) and \
                    a in src and \
                    prepend + a not in self._ignore_props and\
                    prepend + a not in prop_maps:
                if hasattr(getattr(dest, a), '__dict__') :
                    self._map(src[a], getattr(dest, a), prop_maps, prepend + a + '.')
                elif isinstance(getattr(dest, a), dict):
                    self._map(src[a], getattr(dest, a), prop_maps, "{0}['{1}']".format(prepend, a).strip())
                elif isinstance(getattr(dest, a), list) and \
                        isinstance(src[a], list) and \
                        prepend + a + '[x]' not in self._ignore_props:
                    setattr(dest, a, self._map_list(src[a], getattr(dest, a), prepend + a + '[0].'))
                else:
                    setattr(dest, a, src[a])

            if prepend + a in prop_maps:
                    setattr(dest, a, prop_maps[prepend + a]['value'])

        return dest

    def _map_obj_dict(self, src, dest, prop_maps, prepend=''):
        for a in dest:
            prepend_dict = "{0}['{1}']".format(prepend, a).strip()

            if not a.startswith('_') and \
                    not a.startswith('_') and \
                    hasattr(src, a) and \
                    prepend_dict not in self._ignore_props and\
                    prepend_dict not in prop_maps:
                if hasattr(dest[a], '__dict__'):
                    self._map(getattr(src, a), dest[a], prop_maps, prepend + a + '.')
                elif isinstance(dest[a], dict):
                    self._map(getattr(src, a), dest[a], prop_maps, prepend_dict)
                elif isinstance(dest[a], list) and \
                        isinstance(getattr(src, a), list) and \
                        prepend + a + '[x]' not in self._ignore_props:
                    dest[a] = self._map_list(getattr(src, a), dest[a], prepend + a + '[0].')
                else:
                    dest[a] = getattr(src, a)

            if prepend_dict in prop_maps:
                dest[a] = prop_maps[prepend + "['%s']" % a]['value']

        return dest

    def _map_dict_dict(self, src, dest, prop_maps, prepend=''):
        for a in dest:
            prepend_dict = "{0}['{1}']".format(prepend, a).strip()

            if a in src and \
                    prepend_dict not in self._ignore_props and\
                    prepend_dict not in prop_maps:
                if hasattr(dest[a], '__dict__'):
                    self._map(src[a], dest[a], prop_maps, prepend + a + '.')
                elif isinstance(dest[a], dict):
                    self._map(src[a], dest[a], prop_maps, prepend_dict)
                elif isinstance(dest[a], list) and \
                        isinstance(src[a], list) and \
                        prepend + a + '[x]' not in self._ignore_props:
                    dest[a] = self._map_list(src[a], dest[a], prepend + a + '[0].')
                else:
                    dest[a] = src[a]

            if prepend_dict in prop_maps:
                dest[a] = prop_maps[prepend + "['%s']" % a]['value']

        return dest
