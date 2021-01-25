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

target.config['auto_commit'] = True

# delete all records in model
def unlink(model):
    print('unlinking ' + model + ' ...')
    try:
        target.env[model].browse(target.env[model].search([])).unlink()
    except:
        print(model + ' already unlinked')

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
    #'id': 'old_id',
}

# template fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
template_fields = {
    'name' : 'name',
    'sale_ok' : 'sale_ok', 
    'description' : 'description', 
    'purchase_ok': 'purchase_ok',
    'list_price': 'list_price',
    'description_sale': 'description_sale',
    'default_code': 'default_code',
    'image_medium' : 'image_1920',
    'website_published': 'website_published',
    #'id': 'old_id',
}

# category fields to copy from source to target
# { 'source_field_name' : 'target_field_name' }
category_fields = {
    'name' : 'name', 
    'display_name' : 'display_name',
}

# Structures to lookup the new target id from the old source id. { old_id : new_id }
templates_id = {}
categories_id = {}
variants_id = {}

# UNLINKS
unlink('product.public.category')
unlink('product.template')
unlink('product.product')

##### EXAMPLE OF THE PROBLEM START
# we fetch two products from the source database and try to add one of them as a variant of the other.
source_variant_1 = source.env['product.product'].browse(source.env['product.product'].search([])[0])
source_variant_2 = source.env['product.product'].browse(source.env['product.product'].search([])[1])
    
target_variant_id_1 = target.env['product.product'].create({variant_fields[key] : source_variant_1[key] for key in variant_fields.keys()})
target_variant_id_2 = target.env['product.product'].create({variant_fields[key] : source_variant_2[key] for key in variant_fields.keys()})

target_variant = target.env['product.product'].browse(target_variant_id_1)

# this line violates unique constraint:
target_variant.product_variant_ids = [(6, 0, target_variant_id_2)]

exit()
##### EXAMPLE END

# VARIANTS
print('copying variants from source to target ...')
for source_variant_id in source.env['product.product'].search([]):
    source_variant = source.env['product.product'].browse(source_variant_id)
    target_variant_id = target.env['product.product'].create({variant_fields[key] : source_variant[key] for key in variant_fields.keys()})
    variants_id[source_variant_id] = target_variant_id
    print('created product.product', target_variant_id)

# TEMPLATES
print('copying templates from source to target ...')
for source_template_id in source.env['product.template'].search([]):
    source_template = source.env['product.template'].browse(source_template_id)
    source_template_variants = source_template.product_variant_ids.ids
    target_template_variants = [ variants_id[var] for var in source_template_variants ]
    target_template = target.env['product.template'].browse(variants_id[source_template.id])
    target_template.product_variant_ids = [(6, 0, target_template_variants)]
    print('created product.template', target_template.id)

# CATEGORIES
print('copying categories from source to target ...')
for source_category_id in source.env['product.public.category'].search([]):
    source_category = source.env['product.public.category'].browse(source_category_id)
    target_category = target.env['product.public.category'].create({category_fields[key] : source_category[key] for key in category_fields.keys()})
    categories_id[source_category_id] = target_category
    print('created product.public.category', target_category)

print('adding categories to target templates ...')
for source_template_id in source.env['product.template'].search([]):
    source_template = source.env['product.template'].browse(source_template_id)
    target_template = target.env['product.template'].browse(templates_id[source_template_id])[0]
    # get the source template categories and write them to target
    target_template.public_categ_ids = [(6, 0, [categories_id[category] for category in source_template.public_categ_ids.ids])]
    print('added category to product.template', target_template.name)

print('adding parent_id to categories ...')
for source_category_id in source.env['product.public.category'].search([]):
    source_category = source.env['product.public.category'].browse(source_category_id)
    target_category = target.env['product.public.category'].browse(categories_id[source_category_id])[0]
    # get source category parents and write them to target
    target_category.parent_id = [(6, 0, [categories_id[parent] for parent in source_category.parent_id.ids])]
    print('added parent_id to categroy', target_category.name)
