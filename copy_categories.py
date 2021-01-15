#
# This script 
# 1. cleans a target db of it's product.public.category's and ...
# 2. fills the target db with all product.public.category's in a src db.
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


source = odoorpc.ODOO(host=source_params["host"],port=source_params["port"])
source.login(source_params["db"],login=source_params["user"],password=source_params["password"])

target = odoorpc.ODOO(host=target_params["host"],port=target_params["port"])
target.login(target_params["db"],login=target_params["user"],password=target_params["password"])


print('unlinking existsing category ...')
for target_id in target.env['product.public.category'].search([]):
    target.env['product.public.category'].browse(target_id).unlink()


for source_product_id in source.env['product.template'].search([]):
    source_product = source.env['product.template'].browse(source_product_id)
    target_product_id = target.env['product.template'].search([('old_id', '=', source_product_id)])[0]
    target_product = target.env['product.template'].browse(target_product_id)

    for category in source_product.public_categ_ids:

        target_category = target.env['product.public.category'].search([('name','=',category.name)])

        if len(target_category) == 0:
            target_category = target.env['product.public.category'].create({'name' : category.name, 'display_name' : category.display_name})

        target_category = target.env['product.public.category'].search([('name','=',category.name)])

        target_product.public_categ_ids += target_category

