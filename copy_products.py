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
            "port" : 6080,
            "db"   : "dermanord",
            "user" : "admin",
            "password"  : "InwX11Je3DtifHHb"        
        }

target_params = {
            "host" : "81.170.214.150",
            "port" : 8069,
            "db"   : "maria_demo",
            "user" : "admin",
            "password"  : "admin"
        }

source = odoorpc.ODOO(host=source_params["host"],port=source_params["port"])
source.login(source_params["db"],login=source_params["user"],password=source_params["password"])

target = odoorpc.ODOO(host=target_params["host"],port=target_params["port"])
target.login(target_params["db"],login=target_params["user"],password=target_params["password"])

# variant fields to copy from source to target
# 'source_field_name' : 'target_field_name'
variant_fields = {
    'name' : 'name',
    'sale_ok' : 'sale_ok', 
    'description' : 'description', 
    'purchase_ok': 'purchase_ok',
    'list_price': 'list_price',
    'description_sale': 'description_sale',
    'default_code': 'default_code',
    'image_medium' : 'image_1920',
    'id' : 'old_id',
}

# template fields to copy from source to target
# 'source_field_name' : 'target_field_name'
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
    'id' : 'old_id',
}

# category fields to copy from source to target
# 'source_field_name' : 'target_field_name'
category_fields = {
    'name' : 'name', 
    'display_name' : 'display_name',
}

# Structures to lookup the new target id from the old source id.
# old_id : new_id
templates_id = {}
variants_id = {}
categories_id = {}

# UNLINKS
print('unlinking existing categories ...')
target.env['product.public.category'].browse(target.env['product.public.category'].search([])).unlink()

print('unlinking existing templates ...')
target.env['product.template'].browse(target.env['product.template'].search([])).unlink()

print('unlinking existing variants ...')
target.env['product.product'].browse(target.env['product.product'].search([])).unlink()

# TEMPLATES
print('copying templates from source to target ...')
for source_id in source.env['product.template'].search([]):
    source_template = source.env['product.template'].read(source_id, template_fields)
    target_template = target.env['product.template'].create({template_fields[key] : source_template[key] for key in template_fields.keys()})
    templates_id[source_id] = target_template
    print("created product.template id", target_template)

# VARIANTS
print('copying variants from source to target ...')
for source_id in source.env['product.product'].search([]):
    source_variant = source.env['product.product'].read(source_id, variant_fields)
    target_variant = target.env['product.product'].create({variant_fields[key] : source_variant[key] for key in variant_fields.keys()})
    variants_id[source_id] = target_variant
    print("created product.product id", target_variant)

print('adding variants to templates ...')
for source_id in source.env['product.template'].search([]):
    source_template = source.env['product.template'].browse(source_id)
    # loop thourgh source template variants and copy them to target
    for source_template_variant in source_template.product_variant_ids.ids:
        target_template = target.env['product.template'].browse(templates_id[source_id])
        target_template.product_variant_ids += variants_id[source_id]
        print("added variant to", target_template.id)

# CATEGORIES
print('copying categories from source to target ...')
for source_category_id in source.env['product.public.category'].search([]):
    source_category = source.env['product.public.category'].browse(source_category_id, category_fields)
    target_category = target.env['product.public.category'].create({category_fields[key] : source_category[key] for key in category_fields.keys()})
    categories_id[source_category_id] = target_category
    print('created category', target_category)

print('adding categories to target templates ...')
for source_template_id in source.env['product.template'].search([]):
    source_template = source.env['product.template'].browse(source_template_id)
    # loop through the templates categories and copy them to target
    for category in source_template.public_categ_ids:
        target_category_id = category_id[category.id]
        target_template = target.env['product.template'].browse(templates_id[source_template_id])
        target_template.public_categ_ids += target_category_id
        print('added category to template', target_template.id)

print('adding parent_id to categories ...')
for source_category_id in source.env['product.public.category'].search([]):
    source_category = source.env['product.public.category'].browse(source_category_id)
    target_category = target.env['product.public.category'].browse(categories_id[source_category_id])
    target_category.parent_id += categories_id[source_category.parent_id]
    print('added parent_id to', target_category.id)
