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

# delete all records in model
def unlink(model):
    print('unlinking ' + model + ' ... ', end="", flush=True)
    try:
        target.env[model].browse(target.env[model].search([])).unlink()
        print('DONE')
    except:
        print("EMPTY SET or ERROR")

def create_xml_id(name, tgt_id, src_id):
    xml_id = '__ma_import__.%s_%s' % (name.replace('.', '_'), src_id)
    values = {
            'module': xml_id.split('.')[0],
            'name': xml_id.split('.')[1],
            'model': name,
            'res_id': tgt_id,
        }

    try:
        target.env['ir.model.data'].create(values)
    except:
        print('ERROR: external id already exists:', xml_id)

# Gets target record from source id using external ids
# EX: get_target_record_from_id('product.attribute', 3422)
def get_target_record_from_id(model, src_id):
    try:
        return target.env.ref('__ma_import__.%s_%s' % (model.replace('.', '_'), str(src_id)))
    except:
        return -1

def create_record_and_xml_id(model, fields, src_id):
    if get_target_record_from_id(model, src_id) == -1:
        target_record_id = target.env[model].create(fields)
        create_xml_id(model, target_record_id, src_id)
        print("Created new", model, "and ext. id from source id", src_id)
    else:
        print("Did not create new", model, "from source id " + str(src_id) + ". An external id already exists.")
    
# attribute fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
attribute_fields = {
    'name': 'name',
    'type': 'display_type',
}

# attribute value fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
attribute_value_fields = {
    'name': 'name',
}

# attribute line fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
attribute_line_fields = {
    'id' : 'id',
    'display_name' : 'display_name',
    'active' : 'active',
}

# pricelist fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
pricelist_fields = {
    'name' : 'name',
    'code': 'code',
    'display_name': 'display_name',
}

# pricelist item fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
pricelist_item_fields = {
    'price_discount': 'price_discount',
    'price_round': 'price_round',
    'price_discount': 'price_discount',
    'price_min_margin': 'price_min_margin',
    'price_max_margin': 'price_max_margin',
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

for source_template_id in source.env['product.template'].search([]):
    source_template = source.env['product.template'].read(source_template_id, list(template_fields.keys()))
    fields = { template_fields[key] : source_template[key] for key in template_fields.keys() }
    create_record_and_xml_id('product.template', fields, source_template_id)
print()
        
for source_variant_id in source.env['product.product'].search([]):
    source_variant = source.env['product.product'].read(source_variant_id, list(variant_fields.keys()))
    fields = { variant_fields[key] : source_variant[key] for key in variant_fields.keys() }
    create_record_and_xml_id('product.product', fields, source_variant_id)
print()

for source_category_id in source.env['product.public.category'].search([]):
    source_category = source.env['product.public.category'].read(source_category_id, list(category_fields.keys()))
    fields = { category_fields[key] : source_category[key] for key in category_fields.keys() } 
    create_record_and_xml_id('product.public.category', fields, source_variant_id)
print()

for source_pricelist_id in source.env['product.pricelist'].search([]):
    source_pricelist = source.env['product.pricelist'].read(source_pricelist_id, list(pricelist_fields.keys()))
    fields = { pricelist_fields[key] : source_pricelist[key] for key in pricelist_fields.keys() }
    create_record_and_xml_id('product.pricelist', fields, source_pricelist_id)
print()

for source_pricelist_item_id in source.env['product.pricelist.item'].search([]):
    source_pricelist_item = source.env['product.pricelist.item'].read(source_pricelist_item_id, list(pricelist_item_fields.keys()))
    fields = {pricelist_item_fields[key] : source_pricelist_item[key] for key in pricelist_item_fields.keys()}
    create_record_and_xml_id('product.pricelist.item', fields, source_pricelist_item_id)
print()

for source_attribute_id in source.env['product.attribute'].search([]):
    source_attribute = source.env['product.attribute'].read(source_attribute_id, list(attribute_fields.keys()))    
    fields = {target_f : source_attribute[source_f] for source_f, target_f in attribute_fields.items()}
    fields.update({'create_variant': 'no_variant'})
    create_record_and_xml_id('product.attribute', fields, source_attribute_id)
print()

for source_attribute_value_id in source.env['product.attribute.value'].search([]):
    source_attribute_value = source.env['product.attribute.value'].read(source_attribute_value_id, list(attribute_value_fields.keys()) + ['attribute_id'])
    source_attribute = source.env['product.attribute.value'].read(source_attribute_value['attribute_id'][0], ['id'])
    fields = { attribute_value_fields[key] : source_attribute_value[key] for key in attribute_value_fields.keys() }
    fields.update({'attribute_id': get_target_record_from_id('product.attribute', source_attribute['id']).id})
    try:
        create_record_and_xml_id('product.attribute.value', fields, source_attribute_value_id)
    except:
        print("ERROR: could not write product.attribute.value. Entry probably already exist.")
print()
