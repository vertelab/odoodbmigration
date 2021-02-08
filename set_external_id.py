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
            "db"   : "maria_nodemo3",
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

    # target.env['ir.model.data'].create(values)
    # print('hej hej %s' % target.env.ref(xml_id))
    # if target.env.ref(xml_id):
        # print(target.env.ref(xml_id) % ' %s already exist')

    # # target.env.ref('__ma_import__.product_attribute_123')
    # exit()

    try:
        target.env['ir.model.data'].create(values)
        print('created %s' % xml_id)

    except:
        print('could not create %s' % xml_id)



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

pricelist_fields = {
    'name' : 'name',
    'code': 'code',
    'display_name': 'display_name',
    # 'country_group_ids': 'country_group_ids',
}

pricelist_item_fields = {
    # 'product_id': 'product_id',
    'price_discount': 'price_discount',
    'price_round': 'price_round',
    'price_discount': 'price_discount',
    'price_min_margin': 'price_min_margin',
    'price_max_margin': 'price_max_margin',
    # 'country_group_ids': 'country_group_ids',
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

print('1. unlinking existing records ...')
unlink('product.template')
unlink('product.attribute')
unlink('product.attribute.value')
unlink('product.public.category')
unlink('product.template.attribute.line')
unlink('product.template.attribute.value')
unlink('product.product')
unlink('product.pricelist')
unlink('product.pricelist.item')
print()

## TODO: create each model just like in copy_products.py, but use func "create_xml_id" to create an ext. id.
##       this script is then supposed to be run only once ever to set these ext. ids.
##       then rewrite copy_products.py so that it ADDS fields to each model, never create them.


#target.env.ref('__ma_import__.product_attribute_123')


for source_template_id in source.env['product.template'].search([])[:10]:
    source_template = source.env['product.template'].read(source_template_id, list(template_fields.keys()))
    target_template_id = target.env['product.template'].create({template_fields[key] : source_template[key] for key in template_fields.keys()})
    target_template = target.env['product.template'].browse(target_template_id)

    create_xml_id(target_template, source_template_id)


for source_variant_id in source.env['product.product'].search([])[:10]:
    source_variant = source.env['product.product'].read(source_variant_id, list(variant_fields.keys()))
    target_variant_id = target.env['product.product'].create({variant_fields[key] : source_variant[key] for key in variant_fields.keys()})
    target_variant = target.env['product.product'].browse(target_variant_id)

    create_xml_id(target_variant, source_variant_id)


for source_category_id in source.env['product.public.category'].search([])[:10]:
    source_category = source.env['product.public.category'].read(source_category_id, list(category_fields.keys()))
    target_category_id = target.env['product.public.category'].create({category_fields[key] : source_category[key] for key in category_fields.keys()})
    target_category = target.env['product.public.category'].browse(target_category_id)

    create_xml_id(target_category, source_category_id)


for source_pricelist_id in source.env['product.pricelist'].search([])[:10]:
    source_pricelist = source.env['product.pricelist'].read(source_pricelist_id, list(pricelist_fields.keys()))
    target_pricelist_id = target.env['product.pricelist'].create({pricelist_fields[key] : source_pricelist[key] for key in pricelist_fields.keys()})
    target_pricelist = target.env['product.pricelist'].browse(target_pricelist_id)

    create_xml_id(target_pricelist, source_pricelist_id)


for source_pricelist_item_id in source.env['product.pricelist.item'].search([])[:10]:
    source_pricelist_item = source.env['product.pricelist.item'].read(source_pricelist_item_id, list(pricelist_item_fields.keys()))
    target_pricelist_item_id = target.env['product.pricelist.item'].create({pricelist_item_fields[key] : source_pricelist_item[key] for key in pricelist_item_fields.keys()})
    target_pricelist_item = target.env['product.pricelist.item'].browse(target_pricelist_item_id)

    create_xml_id(target_pricelist_item, source_pricelist_item_id)








