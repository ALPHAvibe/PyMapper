import inspect

from py_mapper import *


def main():
    src = {
            'email': 'foo@bar.com',
            'first_name': 'foo bar',
            'phone_numbers': ['5556667777']
        }

    dest = {
            'personal_email': '',
            'first_name': '',
            'phone_numbers': None
        }

    mapper = PyMapper()\
            .ignore(lambda d: d['first_name'])\
            .property_set(lambda s: s['email'], lambda d: d['personal_email'])\

    mapper.map(src, dest)

    print(dest)

if __name__ == "__main__":
    main()
