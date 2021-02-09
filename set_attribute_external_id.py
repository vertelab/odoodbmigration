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
            "db"   : "maria_nodemo2",
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
    'attribute_id'
}

attribute_line_fields = {
    'id' : 'id',
    'display_name' : 'display_name',
    'active' : 'active',
}


print('1. unlinking existing records ...')
unlink('product.template')
unlink('product.attribute')
unlink('product.attribute.value')
unlink('product.template.attribute.line')
unlink('product.template.attribute.value')

print()


for source_attribute_id in source.env['product.attribute'].search([])[:10]:
    source_attribute = source.env['product.attribute'].read(source_attribute_id, list(attribute_fields.keys()))
    target_attribute_id = target.env['product.attribute'].create({attribute_fields[key] : source_attribute[key] for key in attribute_fields.keys()})
    target_attribute = target.env['product.attribute'].browse(target_attribute_id)

    create_xml_id(target_attribute, source_attribute_id)


for source_attribute_value_id in source.env['product.attribute.value'].search([])[:10]:
    source_attribute_value = source.env['product.attribute.value'].read(source_attribute_value_id, list(attribute_value_fields.keys()))
    target_attribute_value_id = target.env['product.attribute.value'].create({attribute_value_fields[key] : source_attribute_value[key] for key in attribute_value_fields.keys()})
    target_attribute_value = target.env['product.attribute.value'].browse(target_attribute_value_id)

    create_xml_id(target_attribute_value, source_attribute_value_id)

for source_template_attribute_line_id in source.env['product.template.attribute.line'].search([])[:10]:
    source_template_attribute_line = source.env['product.template.attribute.line'].read(source_template_attribute_line, list(attribute_line_fields.keys()))
    target_template_attribute_line_id = target.env['product.template.attribute.line'].create({attribute_line_fields[key] : source_template_attribute_line[key] for key in attribute_line_fields.keys()})
    target_template_attribute_line = target.env['product.template.attribute.line'].browse(target_template_attribute_line_id)

    create_xml_id(target_template_attribute_line, source_template_attribute_line_id)


for source_template_attribute_value_id in source.env['product.template.attribute.value'].search([])[:10]:
    source_template_attribute_value = source.env['product.template.attribute.value'].read(source_template_attribute_line, list(attribute_line_fields.keys()))
    target_template_attribute_value_id = target.env['product.template.attribute.value'].create({attribute_line_fields[key] : source_template_attribute_line[key] for key in attribute_line_fields.keys()})
    target_template_attribute_value = target.env['product.template.attribute.value'].browse(target_template_attribute_line_id)

    create_xml_id(target_template_attribute_value, source_template_attribute_value_id)












