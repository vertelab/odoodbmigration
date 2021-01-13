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
            "db"   : "maria_portering",
            "user" : "admin",
            "password"  : "admin"
        }

# 'source_field_name' : 'target_field_name'
fields = {'name', 'name',
    'active' : 'active',
    'list_price', 'list_price',
    'description', 'description',
    'description_sale', 'description_sale',
    'default_code', 'default_code',
    'image', 'image_1920',
}

# fields = [
#               'active','description','description_sale','image',
#               'default_code','name','list_price',
#               'standard_price',
#               'website_description',
#               'website_published','public_desc', 'reseller_desc']

source = odoorpc.ODOO(host=source_params["host"],port=source_params["port"])
source.login(source_params["db"],login=source_params["user"],password=source_params["password"])

target = odoorpc.ODOO(host=target_params["host"],port=target_params["port"])
target.login(target_params["db"],login=target_params["user"],password=target_params["password"])

print('unlinking existsing products ...')
for target_id in target.env['product.template'].search([]):
  target.env['product.template'].browse(target_id).unlink()

print('transferring products from source ...')
for source_id in source.env['product.template'].search([]):
    source_product = source.env['product.template'].read(source_id, fields)
    target.env['product.template'].create({fields[key] : source_product[key] for key in fields.keys()})
