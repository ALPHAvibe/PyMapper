# PyMapper

PyMapper is a python utility that stores the property mapping rules for a source and destination.
PyMapper source and destination can be a dictionary or object and is all inclusive by default.
You must specify what properties to ignore and can customize any destination property with a function.

Example:
```python
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

    def increment_id(src, dest):
        dest['id'] = src['id'] + 1

    mapper = PyMapper()\
            .ignore(lambda d: d['first_name'])\
            .property_set(lambda s: s['email'], lambda d: d['personal_email'])\
            .after(increment_id)
```
##Set default object destination for list property:
```python
    # PhoneNumber class is set as the default destination mapping object for the list
    mapper.list_set_class(lambda d: d.phone_numbers, PhoneNumber())
```
## Upcoming Features
- Set PyMapper for target destination property
