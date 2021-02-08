#!/usr/bin/env python3

#
# This script ports product.template, product.product and product.public.category.
# 1. cleans a target db of the existing models which are to be ported and ...
# 2. copies the models from a src db to target db.
# 
# Used in Maria Åkerberg's porting from Odoo 8 to Odoo 14
# 

import argparse
import json
import logging
import sys

try:
    import odoorpc
except ImportError:
    raise Warning('odoorpc library missing. Please install the library. Eg: pip3 install odoorpc')

source_params = {
            "host" : "localhost",
            "port" : 5080,
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

# variant fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
pricelist_fields = {
    'name' : 'name',
    'code': 'code',
    'display_name': 'display_name',
    # 'country_group_ids': 'country_group_ids',
}

item_fields = {
    'product_id': 'product_id',
    'compute_price': 'compute_price',
    'base': 'base',
    'price_discount': 'price_discount'

    # 'country_group_ids': 'country_group_ids',
}



# delete all records in model
def unlink(model):
    print('unlinking ' + model + ' ...')
    try:
        target.env[model].browse(target.env[model].search([])).unlink()
    except:
        print(model + ' already unlinked')

unlink('product.pricelist')

# CATEGORIES
print('copying pricelist from source to target ..')
for source_pricelist_id in source.env['product.pricelist'].search([]):
    source_pricelist = source.env['product.pricelist'].browse(source_pricelist_id)
    target_pricelist = target.env['product.pricelist'].create({pricelist_fields[key] : source_pricelist[key] for key in pricelist_fields.keys()})



#===============================================================

for source_pricelist_item in source.env['product.pricelist.item'].search([]):
    target_pricelist.item_ids = source_pricelist_item.product_id 



    print('created pricelist', target_pricelist)
