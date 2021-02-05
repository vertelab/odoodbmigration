#!/usr/bin/env python3

##
# This script creates the following models in a target database and sets external ids based on a source database.
# * product.attribute
# * product.attribute.value
# * product.attribute.line
# * product.template
# * product.template.attribute.value
# * product.template.attribute.line
# * product.product 
# * product.public.category
#
# this allows us to later reference the old ids in the source database and write new data to the models as time goes on.
#
# Used in Maria Åkerberg's porting from Odoo 8 to Odoo 14
##

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

def create_xml_id(object, src_id):
    xml_id = '__ma_import__.%s_%s' % (object._name.replace('.', '_'), src_id)
    values = {
            'module': xml_id.split('.')[0],
            'name': xml_id.split('.')[1],
            'model': object._name,
            'res_id': object.id,
        }

    target.env['ir.model.data'].create(values)

# delete all records in model
def unlink(model):
    print('unlinking ' + model + ' ... ', end="", flush=True)
    try:
        target.env[model].browse(target.env[model].search([])).unlink()
        print('DONE')
    except:
        print("EMPTY SET or ERROR")

"""
if target.env['ir.model.data'].xmlid_to_res_id(xml_id):
    target.env['ir.model.data'].browse(
        target.env['ir.model.data'].search(
            [('module', '=', values['module']), ('name', '=', values['name']))).write(values)
else:
    target.env['ir.model.data'].create(values)
"""

# attribute fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
attribute_fields = {
    'name': 'name',
    'type': 'display_type',
}

# attribute fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
attribute_value_fields = {
    'name': 'name',
}

attribute_line_fields = {
    'id' : 'id',
    'display_name' : 'display_name',
    'active' : 'active',
}

# variant fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
variant_fields = {
    'name' : 'name',
    'sale_ok' : 'sale_ok', 
    'description' : 'description', 
    'purchase_ok': 'purchase_ok',
    'list_price': 'list_price',
    'description_sale': 'description_sale',
    'default_code': 'default_code',
    'image_medium' : 'image_1920',
}

# template fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
template_fields = {
    'name' : 'name',
    'sale_ok' : 'sale_ok', 
    'description' : 'description', 
    'purchase_ok': 'purchase_ok',
    'list_price': 'list_price',
    'standard_price' : 'standard_price',
    'description_sale': 'description_sale',
    'default_code': 'default_code',
    'image_medium' : 'image_1920',
    'website_published': 'website_published',
}
# category fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
category_fields = {
    'name' : 'name', 
    'display_name' : 'display_name',
}

count_prod_attr = len(source.env['product.attribute'].search([]))
count_prod_attr_val = len(source.env['product.attribute.value'].search([]))
count_prod_tmpl = len(source_templates_id_XX)
count_prod_attr_line = len(source.env['product.attribute.line'].search([]))
count_prod_var = len(source_variants_id_XX)
count_prod_pub_categ = len(source.env['product.public.category'].search([]))

print('1. unlinking existing records ...')
unlink('product.template')
unlink('product.attribute')
unlink('product.attribute.value')
unlink('product.public.category')
unlink('product.template.attribute.line')
unlink('product.template.attribute.value')
unlink('product.product')
print()

## TODO: create each model just like in copy_products.py, but use func "create_xml_id" to create an ext. id.
##       this script is then supposed to be run only once ever to set these ext. ids.
##       then rewrite copy_products.py so that it ADDS fields to each model, never create them.

"""
for model in models:
    for source_model_id in source.env[model].search([]):
        target.env['ir.model.data'].create({
            'module': '__ma_import__',
            'name': model.replace('.', '_') + str(source_model_id),
            'model': model,
            'res_id': source_model_id,
        }
"""

# target.env.ref('__ma_import__.product_attribute_123')


