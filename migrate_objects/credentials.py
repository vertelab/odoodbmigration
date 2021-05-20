#!/usr/bin/env python3

# this file is included in .gitignore

# usage:
# from credentials import credentials
# credentials['frigg']['password']

credentials = {
    'frigg' : {
        'user' : 'admin',
        'password' : '',
        'local_ip' : '192.168.2.40',
    },
    
    'heimdal' : {
        'user' : 'admin',
        'password' : '',
        'local_ip' : 'localhost',
    },
}
