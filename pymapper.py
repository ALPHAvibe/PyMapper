import copy


class PyMapper(object):
    def __init__(self):
        self._ignore_props = set()
        self._prop_maps = {}
        self._list_class_maps = {}
        self._map_strategies['objobj'] = self._map_obj_obj
        self._map_strategies['dictobj'] = self._map_dict_obj
        self._map_strategies['objdict'] = self._map_obj_dict
        self._map_strategies['dictdict'] = self._map_dict_dict

    def ignore(self, dest_property):
        self._ignore_props.add(dest_property)

        return self

    def property_set(self, src, dest_prop_name):
        if isinstance(src, str):
            print(src)
            self._property_set_func(lambda s: getattr(s, src), dest_prop_name)
        elif callable(src):
            self._property_set_func(src, dest_prop_name)
        return self

    def _property_set_func(self, src_func, dest_prop_name):
        self.ignore(dest_prop_name)
        self._prop_maps[dest_prop_name] = src_func

        return self

    def list_set_class(self, dest_prop_list, obj):
        self._list_class_maps[dest_prop_list] = obj

        return self

    def map(self, src, dest, prepend=''):
        self._map_strategies[self._get_type(src) + self._get_type(dest)](src, dest, prepend)

        for k, v in dict((k, v) for k, v in self._prop_maps.items() if k.startswith(prepend) and '.' not in k[len(prepend):]).items():
            setattr(dest, k, v(src))

        return dest

    def map_list(self, src, dest, prepend='[x]'):
        print(dest)
        print(src)
        if isinstance(src, list) and isinstance(dest, list):
            length = len(src)
            for idx, s in src:
                if hasattr(s, '__dict__') and hasattr(dest[idx], '__dict__') and length > idx:
                    self.map(src[idx], dest[idx], prepend + '.')
                elif prepend in self._list_class_maps:
                    dest.append(copy.deepcopy(self._list_class_maps[prepend]))
                    self.map(src[idx], dest[idx], prepend + '.')
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

    def _map_obj_obj(self, src, dest, prepend=''):
        for a in dir(dest):
            if not a.startswith('_') and \
                    not a.startswith('_') and \
                    hasattr(src, a) and \
                    prepend + a not in self._ignore_props:
                if hasattr(getattr(dest, a), '__dict__') or isinstance(getattr(dest, a), dict):
                    self.map(getattr(src, a), getattr(dest, a), prepend + a + '.')
                elif isinstance(getattr(dest, a), list) and \
                        isinstance(getattr(src, a), list) and \
                        prepend + a + '[x]' not in self._ignore_props:
                    setattr(dest, a, self.map_list(getattr(src, a), getattr(dest, a), prepend + a + '[x].'))
                else:
                    setattr(dest, a, getattr(src, a))

        return dest

    def _map_dict_obj(self, src, dest, prepend=''):
        for a in dir(dest):
            if not a.startswith('_') and \
                    not callable(getattr(dest, a)) and \
                    a in src and \
                    prepend + a not in self._ignore_props:
                if hasattr(getattr(dest, a), '__dict__') or isinstance(getattr(dest, a), dict):
                    self.map(src[a], getattr(dest, a), prepend + a + '.')
                elif isinstance(getattr(dest, a), list) and \
                        isinstance(src[a], list) and \
                        prepend + a + '[x]' not in self._ignore_props:
                    setattr(dest, a, self.map_list(src[a], getattr(dest, a), prepend + a + '[x].'))
                else:
                    setattr(dest, a, src[a])

        return dest

    def _map_obj_dict(self, src, dest, prepend=''):
        for a in dest:
            if not a.startswith('_') and \
                    not callable(dest[a]) and \
                    hasattr(src, a) and \
                    prepend + a not in self._ignore_props:
                if hasattr(dest[a], '__dict__') or isinstance(dest[a], dict):
                    self.map(getattr(src, a), dest[a], prepend + a + '.')
                elif isinstance(dest[a], list) and \
                        isinstance(getattr(src, a), list) and \
                        prepend + a + '[x]' not in self._ignore_props:
                    dest[a] = self.map_list(getattr(src, a), dest[a], prepend + a + '[x].')
                else:
                    dest[a] = getattr(src, a)

        return dest

    def _map_dict_dict(self, src, dest, prepend=''):
        for a in dest:
            if not a.startswith('_') and \
                    not callable(dest[a]) and \
                    a in src and \
                    prepend + a not in self._ignore_props:
                if hasattr(dest[a], '__dict__') or isinstance(dest[a], dict):
                    self.map(src[a], dest[a], prepend + a + '.')
                elif isinstance(dest[a], list) and \
                        isinstance(src[a], list) and \
                        prepend + a + '[x]' not in self._ignore_props:
                    dest[a] = self.map_list(src[a], dest[a], prepend + a + '[x].')
                else:
                    dest[a] = src[a]

        return dest
