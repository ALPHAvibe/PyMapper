import inspect

from py_mapper import *


def main():
    src = {
            'id': 1,
            'email': 'foo@bar.com',
            'first_name': 'foo bar',
            'phone_numbers': ['5556667777']
        }

    dest = {
            'id': 0,
            'personal_email': '',
            'first_name': '',
            'phone_numbers': None
        }

    def increment_id(src, dest):
        dest['id'] = src['id'] + 1

    mapper = PyMapper()\
            .ignore(lambda d: d['first_name'])\
            .property_set(lambda s: s['email'], lambda d: d['personal_email'])\
            .after(increment_id)

    mapper.map(src, dest)

    print(dest)

if __name__ == "__main__":
    main()
