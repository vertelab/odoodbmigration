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
        print('created', xml_id)
    except:
        print('external id already exists:', xml_id)

# get_target_record_from_external_source_id
#get_target_record_from_id('product.attribute', 3422)
def get_target_record_from_id(model, src_id):
    try:
        return target.env.ref('__ma_import__.%s_%s' % (model.replace('.', '_'), str(src_id)))
    except:
        return -1

# delete all records in model
def unlink(model):
    print('unlinking ' + model + ' ... ', end="", flush=True)
    try:
        target.env[model].browse(target.env[model].search([])).unlink()
        print('DONE')
    except:
        print("EMPTY SET or ERROR")

# attribute fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
attribute_fields = {
    'name': 'name',
    # 'type': 'display_type',
}

# attribute fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
attribute_value_fields = {
    'name': 'name',
    'attribute_id': 'attribute_id',
}

attribute_line_fields = {
    'id' : 'id',
    'display_name' : 'display_name',
    'active' : 'active',
    'attribute_id' : 'attribute_id',
    'product_tmpl_id': 'product_tmpl_id'
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

for source_template_id in source.env['product.template'].search([]):
    source_template = source.env['product.template'].read(source_template_id, list(template_fields.keys()))
    if get_target_record_from_id(source_template_id) == -1:
        target_template_id = target.env['product.template'].create({template_fields[key] : source_template[key] for key in template_fields.keys()})
        create_xml_id('product.template', target_template_id, source_template_id)
print('\n')
        
for source_variant_id in source.env['product.product'].search([]):
    source_variant = source.env['product.product'].read(source_variant_id, list(variant_fields.keys()))
    if get_target_record_from_id(source_variant_id) == -1:
        target_variant_id = target.env['product.product'].create({variant_fields[key] : source_variant[key] for key in variant_fields.keys()})
        create_xml_id('product.product', target_variant_id, source_variant_id)
print('\n')

for source_category_id in source.env['product.public.category'].search([]):
    source_category = source.env['product.public.category'].read(source_category_id, list(category_fields.keys()))
    if get_target_record_from_id(source_category_id) == -1:
        target_category_id = target.env['product.public.category'].create({category_fields[key] : source_category[key] for key in category_fields.keys()})
        create_xml_id('product.public.category', target_category_id, source_category_id)
print('\n')

for source_pricelist_id in source.env['product.pricelist'].search([]):
    source_pricelist = source.env['product.pricelist'].read(source_pricelist_id, list(pricelist_fields.keys()))
    if get_target_record_from_id(source_pricelist_id) == -1:
        target_pricelist_id = target.env['product.pricelist'].create({pricelist_fields[key] : source_pricelist[key] for key in pricelist_fields.keys()})
        create_xml_id('product.pricelist', target_pricelist_id, source_pricelist_id)
print('\n')

for source_pricelist_item_id in source.env['product.pricelist.item'].search([]):
    source_pricelist_item = source.env['product.pricelist.item'].read(source_pricelist_item_id, list(pricelist_item_fields.keys()))
    if get_target_record_from_id(source_pricelist_item_id) == -1:
        target_pricelist_item_id = target.env['product.pricelist.item'].create({pricelist_item_fields[key] : source_pricelist_item[key] for key in pricelist_item_fields.keys()})
        create_xml_id('product.pricelist.item', target_pricelist_item_id, source_pricelist_item_id)
print('\n')

for source_attribute_id in source.env['product.attribute'].search([]):
    source_attribute = source.env['product.attribute'].read(source_attribute_id, list(attribute_fields.keys()))    
    all_fields = {target_f : source_attribute[source_f] for source_f, target_f in attribute_fields.items()}
    all_fields.update({'create_variant': 'no_variant'})
    if get_target_record_from_id(source_attribute_id) == -1:
        target_attribute_id = target.env['product.attribute'].create(all_fields)
        create_xml_id('product.attribute', target_attribute_id, source_attribute_id)
print('\n')

for source_attribute_value_id in source.env['product.attribute.value'].search([]):
    source_attribute_value = source.env['product.attribute.value'].read(attribute_value_fields)
    source_attribute = source.env['product.attribute.value'].read(source_attribute_value['attribute_id'][0], ['id'])
    
    all_fields = {attribute_fields[key] : source_attribute_value[key] for key in attribute_fields.keys()}
    all_fields.update({'attribute_id': target.env.ref(target_attribute)})
    
    try:
        if get_target_record_from_id(source_attribute_value_id) == -1:
            target_attribute_value_id = target.env['product.attribute.value'].create(all_fields)
            create_xml_id('product.attribute.value', target_attribute_value_id, source_attribute_id)
    except:
        print("ERROR: could not write product.attribute.value. Entry probably already exist.")
print('\n')
