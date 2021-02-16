#!/usr/bin/env python3

import argparse
import json
import logging
import sys
try:
    import odoorpc
except ImportError:
    raise Warning('odoorpc library missing. Please install the library. Eg: pip3 install odoorpc')

from credentials import credentials

# SETTINGS
source_params = {
            "host" : "localhost",
            "port" : 6080,
            "db"   : "dermanord",
            "user" : credentials['frigg']['user'],
            "password"  : credentials['frigg']['password']
        }

target_params = {
            "host" : "81.170.214.150",
            "port" : 8069,
            "db"   : "maria_utv",
            "user" : "admin",
            "password"  : "admin"
        }

# CONNECTION
source = odoorpc.ODOO(host=source_params["host"],port=source_params["port"])
source.login(source_params["db"],login=source_params["user"],password=source_params["password"])

target = odoorpc.ODOO(host=target_params["host"],port=target_params["port"])
target.login(target_params["db"],login=target_params["user"],password=target_params["password"])

# HELPER FUNCTIONS
# delete all records in model, e.x. unlink('product.template')
def unlink(model):
    print('unlinking ' + model + ' ... ', end="", flush=True)
    try:
        target.env[model].browse(target.env[model].search([])).unlink()
        print('DONE')
    except:
        print("EMPTY SET or ERROR")

# create external id for model, e.x. create_xml_id('product.template', 89122, 5021)
def create_xml_id(model, tgt_id, src_id):
    xml_id = '__ma_import__.%s_%s' % (model.replace('.', '_'), src_id)
    values = {
            'module': xml_id.split('.')[0],
            'name': xml_id.split('.')[1],
            'model': model,
            'res_id': tgt_id,
        }

    target.env['ir.model.data'].create(values)

# gets target record from source id using external id, e.x. get_target_record_from_id('product.attribute', 3422)
def get_target_record_from_id(model, src_id):
    try:
        return target.env.ref('__ma_import__.%s_%s' % (model.replace('.', '_'), str(src_id)))
    except:
        return 0

# create a record with dict fields as values, and creates an ext. id to src_id
def create_record_and_xml_id(model, fields, src_id):
    if get_target_record_from_id(model, src_id) == 0:
        target_record_id = target.env[model].create(fields)
        try:
            pass
        except:
            print('ERROR: target.env[' + model + '].create failed')
            return
            
        try:
            create_xml_id(model, target_record_id, src_id)
            print('Created new ' + model + ' and ext. id from source id ' + str(src_id))
        except:
            print('ERROR: create_xml_id(' + model + ', ' + str(target_record_id) + ', ' + str(src_id) + ') failed. Does the id already exist?')
    else:
        tgt_id = get_target_record_from_id(model, src_id).id
        print('INFO: skipping creation, an external id already exist for ' + model + '(' + str(tgt_id) + ')')
