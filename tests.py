import unittest
from py_mapper import *


class Child(object):
    def __init__(self):
        self.id = 0

class Foo(object):
    def __init__(self):
        self.id = 0
        self.meta = MetaFoo()
        self.children = []


class MetaFoo(object):
    def __init__(self):
        self.email = ''
        self.first_name = ''
        self.last_name = ''
        self.full_name = ''


class Tests(unittest.TestCase):

    def test_ignore_works(self):
        src = {
            'id': 1,
            'meta': {
                'email': 'foo@bar.com',
                'full_name': 'Foo Bar'
            }
        }

        dest = {
            'id': 0,
            'meta': {
                'email': '',
                'full_name': ''
            }
        }

        PyMapper().ignore(lambda d: d['meta']['full_name']).map(src, dest)

        self.assertEqual(dest['meta']['full_name'], '')

    def test_property_set_works(self):
        src = Foo()
        src.id = 1
        src.meta.email = 'foo@bar.com'
        src.meta.first_name = 'foo'
        src.meta.last_name = 'bar'

        dest = Foo()

        PyMapper()\
            .property_set(lambda s: s.meta.first_name + ' ' + s.meta.last_name, lambda d: d.meta.full_name)\
            .map(src, dest)

        self.assertEqual(src.meta.first_name + ' ' + src.meta.last_name, dest.meta.full_name)

    def test_dict_dict_map(self):
        src = {
            'id': 1,
            'meta': {
                'email': 'foo@bar.com',
                'full_name': 'Foo Bar'
            }
        }

        dest = {
            'id': 0,
            'meta': {
                'email': '',
                'full_name': ''
            }
        }

        PyMapper().map(src, dest)

        self.assertEqual(src['id'], dest['id'])
        self.assertEqual(src['meta']['email'], dest['meta']['email'])
        self.assertEqual(src['meta']['full_name'], dest['meta']['full_name'])

    def test_obj_dict_map(self):
        src = Foo()
        src.id = 1
        src.meta.email = 'foo@bar.com'
        src.meta.full_name = 'foo_name'

        dest = {
            'id': 0,
            'meta': {
                'email': '',
                'full_name': ''
            }
        }

        PyMapper().map(src, dest)

        self.assertEqual(src.id, dest['id'])
        self.assertEqual(src.meta.email, dest['meta']['email'])
        self.assertEqual(src.meta.full_name, dest['meta']['full_name'])

    def test_obj_obj_map(self):
        src = Foo()
        src.id = 1
        src.meta.email = 'foo@bar.com'
        src.meta.full_name = 'foo_name'

        dest = Foo()

        PyMapper().map(src, dest)

        self.assertEqual(src.id, dest.id)
        self.assertEqual(src.meta.email, dest.meta.email)
        self.assertEqual(src.meta.full_name, dest.meta.full_name)

    def test_list_map(self):
        child1 = Child()
        child1.id = 2

        src = Foo()
        src.id = 1
        src.meta.email = 'foo@bar.com'
        src.meta.full_name = 'foo_name'
        src.children.append(child1)

        dest = Foo()

        PyMapper()\
            .list_obj(Child(), lambda d: d.children[0])\
            .map(src, dest)

        self.assertEqual(src.id, dest.id)
        self.assertEqual(src.meta.email, dest.meta.email)
        self.assertEqual(src.meta.full_name, dest.meta.full_name)
        self.assertEqual(len(src.children), len(dest.children))
        self.assertTrue(dest.children[0].id == 2)

if __name__ == '__main__':
    unittest.main(exit=False)
