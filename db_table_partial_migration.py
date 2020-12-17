#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 15:26:30 2020

Sample usage:
=============

./db_table_partial_migration.py -s {...} -t {...} -m product.template -f  ...

{...} is a JSON str such as:
    {"host":"localhost","port":"8069","db":"demo","user":"admin","password":""}
... is a comma-separated string of all fields of the model to use:
    id,name,description, etc

{"host":"localhost","port":"8069","db":"demo","user":"admin","password":""}
product.template
'active,description,description_sale,image,default_code,name,list_price,standard_price,website_description,website_published,website_short_description'


@author: Simon Rundstedt, Anders Wallenquist
"""
#%% ---------------------------------------------------------------------------
import argparse
import json
import logging
import sys
try:
    import odoorpc
except ImportError:
    raise Warning('odoorpc library missing. Please install the library. Eg: pip3 install odoorpc')
#%% ---------------------------------------------------------------------------
# Helpers
CONN_PARAM_FIELDS = ["host","port","db","user","password"]
def json2dbconn(jsonstr):
    '''
    '''
    ret = json.loads(jsonstr)
    for f in CONN_PARAM_FIELDS:
        if f not in ret:
            _logger.error("Not all connection details defined.")
            # TODO: Raise error, try to recover, and/or crash the program.
    return ret
#%% ---------------------------------------------------------------------------
# Defaults
_logger = logging.getLogger(__name__)

source_params = {
            "host" : "localhost",
            "port" : 8069,
            "db"   : "demo",
            "user" : "admin",
            "password"  : ""        
        }

model = "product.template"
fields = [
      'active','description','description_sale','image',
      'default_code','name','list_price',
      'standard_price',
      'website_description',
      'website_published','website_short_description']

target_params = {
            "host" : "localhost",
            "port" : 8069,
            "db"   : "demo",
            "user" : "admin",
            "password"  : ""        
        }

#%% ---------------------------------------------------------------------------

if __name__ == '__main__':
    _logger.info("Program is __main__")
    _logger.info("Parsing system arguments")
    parser = argparse.ArgumentParser(description="Migrate Odoo DB-data.")
    parser.add_argument(
                '-s','--source',
                dest="source_db",
                required=True,
                help="Connection details for source DB."
            )
    parser.add_argument(
            '-t','--target',
            dest="target_db",
            required=True,
            help="Connection details for target DB."
        )
    parser.add_argument(
            '-m','--model',
            dest="db_model",
            required=True,
            help="Model to transfer"
        )
    parser.add_argument(
            '-f','--fields',
            dest="model_fields",
            required=True,
            help="Fields to transfer."
        )
    ns = parser.parse_args()
    source_params = json2dbconn(ns.source_db)
    target_params = json2dbconn(ns.target_db)
    model         = ns.db_model
    fields        = ns.model_fields.split(",") 

exit() # TODO : Remove
#%% ---------------------------------------------------------------------------
# Program functions

def export_filter(val):
    '''
    Filter and clean Odoo get(...) output for write into
    other DB.
    '''
    if type(val) == list:
        # If list assume the values are db id's (int) and
        # remove any other values
        return list(filter(lambda X: type(X) == int, val))
    else:
        return val

def migrate_data(source_conn, target_conn, model, fields):
    '''
    Migrate selected fields of model from source to target database.
    
    Parameters
    ==========
    source : 
        Open connection to source database
    target : 
        Open connection to target database
    model : str
        Name of model to migrate
    fields :
        Fields of the model to migrate
    '''    
    nfields = fields + ['old_id']
    parents=[]
    for id in source.env[model].search([]):
        print("Updating voucher with id %s" % id)
        product = source.env[model].read(id, fields)
        nid = target.env[model].search([('old_id','=',id)])
        if len(nid) > 0:
            target.env[model].write(nid, {key:product[key] for key in fields if key not in ['parent_id','image']})
        else:
            # ~ partner['old_id'] = id
            nid = target.env[model].create({key:product.get(key) for key in nfields if key not in ['parent_id','image']})
            target.env[model].write(nid, {'image_1920': product['image']})
            
#%% ---------------------------------------------------------------------------
# Program proper
source = odoorpc.ODOO(host=source_params["host"],port=source_params["port"])
source.login(source_params["db"],login=source_params["user"],password=source_params["password"])
# nparams = odoorpc.session.get('cw')
#target = odoorpc.ODOO(nparams.get('host'),port=nparams.get('port'))
#target.login(nparams.get('database'),nparams.get('user'),nparams.get('passwd'))
target = odoorpc.ODOO(host=target_params["host"],port=target_params["port"])
target.login(target_params["db"],login=target_params["user"],password=target_params["password"])

migrate_data(source, target, model, fields)