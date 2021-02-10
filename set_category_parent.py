#!/usr/bin/env python3

import argparse
import json
import logging
import sys
try:
    import odoorpc
except ImportError:
    raise Warning('odoorpc library missing. Please install the library. Eg: pip3 install odoorpc')

# SETTINGS
source_params = {
            "host" : "localhost",
            "port" : 6080,
            "db"   : "dermanord",
            "user" : "admin",
            "password"  : "InwX11Je3DtifHHb"        
        }

target_params = {
            "host" : "81.170.214.150",
            "port" : 8069,
            "db"   : "maria_nodemo",
            "user" : "admin",
            "password"  : "admin"
        }
        

source = odoorpc.ODOO(host=source_params["host"],port=source_params["port"])
source.login(source_params["db"],login=source_params["user"],password=source_params["password"])

target = odoorpc.ODOO(host=target_params["host"],port=target_params["port"])
target.login(target_params["db"],login=target_params["user"],password=target_params["password"])

# Gets target record from source id using external ids
# EX: get_target_record_from_id('product.attribute', 3422)
def get_target_record_from_id(model, src_id):
    try:
        return target.env.ref('__ma_import__.%s_%s' % (model.replace('.', '_'), str(src_id)))
    except:
        return -1

for source_category_id in source.env['product.public.category'].search([]):
    source_category = source.env['product.public.category'].read(source_category_id, ['id', 'parent_id'])
    source_category_parent_id = None if not source_category['parent_id'] else source_category['parent_id'][0]
    
    target_category = get_target_record_from_id('product.public.category', source_category['id'])
    
    if source_category_parent_id:
        target_parent_category_id = get_target_record_from_id('product.public.category', source_category_parent_id).id
        target_category.write({ 'parent_id' : target_parent_category_id })
        print("wrote", target_parent_category_id, "to parent_id of", target_category)
    else:
        print(target_category, "has no parent")
