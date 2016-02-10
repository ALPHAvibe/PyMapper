# PyMapper

PyMapper is a python utility that stores the property mapping rules for a source and destination.
PyMapper source and destination can be a dictionary or object and is all inclusive by default.
You must specify what properties to ignore and can customize any destination property with a lambda function.

Example:

    src_user = User()
    src_user.email = 'xxxxxxx'
    src_user.first_name = 'xxxxxxx'
    src_user.nick_name = "xxxxxxx"


    dest_user = User()
    dest_user.email = 'ignore_me@http.cat'
    dest_user.first_name = 'change me'
    dest_user.nick_name = 'change me'

    mapper = PyMapper()
                .ignore('email')\
                # select source property to set into destination property
                .property_set('first_name', 'nick_name')\
                # create expression for destination property
                .property_set_lamda('full_name', lambda src: src.first_name + ' ' + src.last_name)

    dest_user = mapper.map(src_user, dest_user)


Key into nested object's/dictionary's property:

    # ignore state property in address object/dict property
    mapper.ignore('address.state')

Key into list:

    # ignore area_code property in phone_numbers list
    mapper.ignore('phone_numbers[x].area_code')

Set default object destination for list property:

    # PhoneNumber class is set as the default destination mapping object for the list
    mapper.list_set_class('phone_numbers[x]', PhoneNumber())

