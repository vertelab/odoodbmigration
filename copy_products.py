#
# This script 
# 1. cleans a target db of it's products.template's and ...
# 2. fills the target db with all products.template's in a src db.
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
            "db"   : "maria1",
            "user" : "admin",
            "password"  : "admin"
        }

# 'source_field_name' : 'target_field_name'
fields = {
'name' : 'name',
'sale_ok' : 'sale_ok', 
'description' : 'description', 
'purchase_ok': 'purchase_ok',
'list_price': 'list_price',
'description_sale': 'description_sale',
'default_code': 'default_code',
'image_medium' : 'image_1920',
'id': 'old_id',

}

source = odoorpc.ODOO(host=source_params["host"],port=source_params["port"])
source.login(source_params["db"],login=source_params["user"],password=source_params["password"])

target = odoorpc.ODOO(host=target_params["host"],port=target_params["port"])
target.login(target_params["db"],login=target_params["user"],password=target_params["password"])

print('unlinking existsing products ...')
for target_id in target.env['product.template'].search([]):
	target.env['product.template'].browse(target_id).unlink()

print('copying products from source ...')
for source_id in source.env['product.template'].search([]):
    source_product = source.env['product.template'].read(source_id, fields)
    target.env['product.template'].create({fields[key] : source_product[key] for key in fields.keys()})

