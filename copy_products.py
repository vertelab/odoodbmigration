#!/usr/bin/env python3

# 
# This script ports the following models from a source db to a target db: 
# * product.attribute
# * product.attribute.value
# * product.attribute.line
# * product.template
# * product.template.attribute.value
# * product.template.attribute.line
# * product.product 
# * product.public.category
# 
# Method:
# 1. cleans the target db of the existing models which are to be ported and ...
# 2. copies the models from the src db to the target db.
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
    print('unlinking ' + model + ' ... ', end="")
    try:
        target.env[model].browse(target.env[model].search([])).unlink()
    except:
        pass
    print('DONE')

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

# Structures to lookup the new target id from the old source id. 
# { old_id : new_id }
attributes_id = {}
templates_id = {}
categories_id = {}
variants_id = {}
attribute_values_id = {}

count_prod_attr = len(source.env['product.attribute'].search([]))
count_prod_attr_val = len(source.env['product.attribute.value'].search([]))
count_prod_tmpl = len(source.env['product.template'].search([]))
count_prod_attr_line = len(source.env['product.attribute.line'].search([]))
count_prod_var = len(source.env['product.product'].search([]))
count_prod_pub_categ = len(source.env['product.public.category'].search([]))

# UNLINKS
print('1. unlinking existing records ...')
unlink('product.attribute')
unlink('product.attribute.value')
unlink('product.attribute.value.line')
unlink('product.public.category')
unlink('product.template')
unlink('product.template.attribute.line')
unlink('product.template.attribute.value')
unlink('product.product')
print()

## TEMPORARY CODE
print('1.5. instantiating a subset of template and variants ...')
source_templates_id_XX = source.env['product.template'].search([])[:10]
source_variants_id_XX = []
for source_template_id in source_templates_id_XX:
    source_template = source.env['product.template'].read(source_template_id, ['id', 'product_variant_ids'])
    source_template_product_variant_ids = source_template['product_variant_ids']
    source_variants_id_XX += source_template_product_variant_ids
print()
#

print('2. copying product.attribute from source to target ...')
curr_count = 1
for source_attribute_id in source.env['product.attribute'].search([]):
    source_attribute = source.env['product.attribute'].read(source_attribute_id, list(attribute_fields.keys()))
    all_fields = {target_f : source_attribute[source_f] for source_f, target_f in attribute_fields.items()}
    all_fields.update({'create_variant': 'no_variant'})
    target_attribute_id = target.env['product.attribute'].create(all_fields)
    attributes_id[source_attribute_id] = target_attribute_id
    print("created product.attribute id", target_attribute_id, "(" + str(curr_count) + "/" + str(count_prod_attr) + ")", end='\r')
    curr_count += 1
print('\n')
    
print('3. copying product.attribute.value from source to target ...')
curr_count = 1
for source_attribute_value_id in source.env['product.attribute.value'].search([]):
    source_attribute_value = source.env['product.attribute.value'].read(source_attribute_value_id, list(attribute_value_fields.keys()) + ['attribute_id'] )
    all_fields = {attribute_value_fields[key] : source_attribute_value[key] for key in attribute_value_fields.keys()}
    source_attribute = source.env['product.attribute'].read(source_attribute_value['attribute_id'][0], ['id'])
    all_fields.update({'attribute_id': attributes_id[source_attribute['id']]})
    try:
        target_attribute_value_id = target.env['product.attribute.value'].create(all_fields)
        attribute_values_id[source_attribute_value_id] = target_attribute_value_id
        print("created product.attribute.value id", target_attribute_value_id, "(" + str(curr_count) + "/" + str(count_prod_attr_val) + ")", end='\r')
    except:
        print("ERROR: could not write product.attribute.value. Entry probably already exist.")
    curr_count += 1
print('\n')

print('4. copying product.template from source to target ...')
curr_count = 1
for source_template_id in source_templates_id_XX: #source.env['product.template'].search([]):
    source_template = source.env['product.template'].read(source_template_id, list(template_fields.keys()))
    target_template_id = target.env['product.template'].create({template_fields[key] : source_template[key] for key in template_fields.keys()})
    templates_id[source_template_id] = target_template_id
    #print("added", source_template_id, "->", target_template_id)
    print("created product.template id", target_template_id, "(" + str(curr_count) + "/" + str(count_prod_tmpl) + ")", end='\r')
    curr_count += 1
print('\n')

print('5. copying product.product from source to target ...')
curr_count = 1
for source_variant_id in source_variants_id_XX: #source.env['product.product'].search([]):
    source_variant = source.env['product.product'].read(source_variant_id, list(variant_fields.keys()) + ['product_tmpl_id'])
    target_variant_id = target.env['product.product'].create({variant_fields[key] : source_variant[key] for key in variant_fields.keys()})
    variants_id[source_variant_id] = target_variant_id
    
    target_variant_template_id = target.env['product.product'].read(target_variant_id, ['product_tmpl_id'])[0]['product_tmpl_id'][0]
    templates_id[source_variant['product_tmpl_id'][0]] = target_variant_template_id
    #print("added", source_variant['product_tmpl_id'][0], "->", target_variant_template_id)
    print('created product.product', target_variant_id, "(" + str(curr_count) + "/" + str(count_prod_var) + ")", end='\r')
    curr_count += 1
print('\n')

print('6. copying product.attribute.line from source to target ...')
curr_count = 1
for source_template_id in source_templates_id_XX:
    source_template = source.env['product.template'].read(source_template_id, ['attribute_line_ids'])
    
    for source_attribute_line_id in source_template['attribute_line_ids']:
        source_attribute_line = source.env['product.attribute.line'].read(source_attribute_line_id, ['attribute_id', 'value_ids'])
        source_attribute_line_attribute_id = source.env['product.attribute'].read(source_attribute_line['attribute_id'][0], ['id'])['id']

        all_fields = { 'product_tmpl_id': templates_id[source_template_id], 'attribute_id' : attributes_id[source_attribute_line_attribute_id], 'value_ids': [ attribute_values_id[attr] for attr in source_attribute_line['value_ids'] ]}
        target_template_attribute_line_id = target.env['product.template.attribute.line'].create(all_fields)
        
        print("created product.template.attribute.line id", target_template_attribute_line_id, "on product id", source_template_id, "(" + str(curr_count) + "/" + str(count_prod_attr_line) + ")", end='\r')
        curr_count += 1
print('\n')

print('7. linking product.product to product.template ...')
curr_count = 1
for source_template_id in source_templates_id_XX: #source.env['product.template'].search([]):
    source_template = source.env['product.template'].read(source_template_id, list(template_fields.keys()) + ['product_variant_ids'])
    target_template_variants = [ variants_id[var] for var in source_template['product_variant_ids'] ]
    target_template = target.env['product.template'].browse(templates_id[source_template['id']])
    target_template.product_variant_ids = [(6, 0, target_template_variants)]
    print('created variants of', templates_id[source_template_id], "(" + str(curr_count) + "/" + str(count_prod_tmpl) + ")", end='\r')
    curr_count += 1
print('\n')

print('8. copying categories from source to target ...')
curr_count = 1    
for source_category_id in source.env['product.public.category'].search([]):
    source_category = source.env['product.public.category'].read(source_category_id, list(category_fields.keys()))
    target_category = target.env['product.public.category'].create({category_fields[key] : source_category[key] for key in category_fields.keys()})
    categories_id[source_category_id] = target_category
    print('created product.public.category', target_category, "(" + str(curr_count) + "/" + str(count_prod_pub_categ) + ")", end='\r')
    curr_count += 1
print('\n')

print('9. adding categories to target templates ...')
curr_count = 1    
for source_template_id in source_templates_id_XX: #source.env['product.template'].search([]):
    source_template = source.env['product.template'].read(source_template_id, list(template_fields.keys()) + ['public_categ_ids'])
    target_template = target.env['product.template'].browse(templates_id[source_template_id])[0]
    target_template.public_categ_ids = [(6, 0, [categories_id[category] for category in source_template['public_categ_ids']])]
    print('added category to product.template', target_template.name, "(" + str(curr_count) + "/" + str(count_prod_tmpl) + ")", end='\r')
    curr_count += 1
print('\n')

print('10. adding parent_id to categories ...')
curr_count = 1    
for source_category_id in source.env['product.public.category'].search([]):
    source_category = source.env['product.public.category'].browse(source_category_id)
    target_category = target.env['product.public.category'].browse(categories_id[source_category_id])[0]
    if source_category.parent_id:
        target_category.write({'parent_id' : categories_id[source_category.parent_id.id]})
    print('added parent_id to category', target_category.name, "(" + str(curr_count) + "/" + str(count_prod_pub_categ) + ")", end='\r')
    curr_count += 1
print('\n')
