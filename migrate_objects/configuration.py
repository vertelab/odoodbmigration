#!/usr/bin/env python3
import datetime
import argparse
import json
import logging
import sys
try:
    import odoorpc
except ImportError:
    raise Warning('odoorpc library missing. Please install the library. Eg: pip3 install odoorpc')

from PIL import Image

Image.MAX_IMAGE_PIXELS = 100000000000
print(1)
source = odoorpc.ODOO.load('source')
target = odoorpc.ODOO.load('target')
del source.env.context['lang']
target.env.context['lang'] = 'en_US'
print(2)
# HELPER FUNCTIONS
IMPORT_MODULE_STRING = '__import__'
''' Glossary
       domain = list of search criterias
           id = number
        model = ex. 'res.partner'
record_fields = what you get from source.env[model].read(record.id, fields)
  record_list = what you get from source.env[model].search([])
      records = what you get from source.env[model].browse(record_list)
       record = what you get from source.env[model].browse(record_list[index])
       source = source database
       target = target database
'''
print(3)
# delete all records in model, e.x. unlink('product.template')

def find_fields_in_core(model, modules, database):
    '''
    '''
    ids = database.env["ir.model.fields"].search([["model","=",model]])
    #print(ids)
    rs = database.env["ir.model.fields"].browse(ids)
    #print(rs)
    fields_in_modules = []
    for r in rs:
        #print(f"{r.name}")
        print(f"Model:{model} Field: {r.name} Module: {r.modules}")
        if r.modules in modules or modules == []:
            fields_in_modules.append(r.name)
    return fields_in_modules

def find_fields_in_database(model, database):
    '''
    '''
    ids = database.env["ir.model.fields"].search([["model","=",model]])
    rs = database.env["ir.model.fields"].browse(ids)
    fields = []
    for r in rs:
        fields.append(r.name)
    return fields
    
def non_matching_keys(a, b):
    return([key for key in a if key not in b])


def unlink(model, only_migrated=True):
    ''' unlinks all records of a model in target database
    example: unlink('res.partner')
    '''
    record_list = []
    if only_migrated:
        domain = [('module', '=', IMPORT_MODULE_STRING), ('model', '=', model)]
        model_data_record_list = target.env['ir.model.data'].search(domain)
        model_data_records = target.env['ir.model.data'].browse(
            model_data_record_list)
        for record in model_data_records:
            record_list.append(record.res_id)
    else:
        record_list = target.env[model].search([])

    try:
        target.env[model].browse(record_list).unlink()
        print(f"Recordset('{model}', {record_list}) unlinked")
    except Exception as e:
        print(e)


def create_xml_id(model, target_record_id, source_record_id):
    ''' Creates an external id for a model
    example: create_xml_id('product.template', 89122, 5021)
    '''
    xml_id = f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}"
    values = {
        'module': xml_id.split('.')[0],
        'name': xml_id.split('.')[1],
        'model': model,
        'res_id': target_record_id,
    }
    try:
        target.env['ir.model.data'].create(values)
        return f"xml_id = {xml_id} created"
    except:
        return f"ERROR: create_xml_id('{model}', {target_record_id}, {source_record_id}) failed. Does the id already exist?"


def get_target_record_from_id(model, source_record_id):
    ''' gets record from target database using record.id from source database
    example: get_target_record_from_id('product.attribute', 3422)
    returns: 0 if record cannot be found
    '''
    try:
        r = target.env.ref(f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
        return r
    except:
        return 0


def create_record_and_xml_id(model, fields, source_record_id):
    ''' Creates record on target if it doesn't exist, using fields as values,
    and creates an external id so that the record will not be duplicated
    example: create_record_and_xml_id('res.partner', {'name':'MyPartner'}, 2)
    '''
    #print(f"Fields: {fields}")
    if get_target_record_from_id(model, source_record_id):
        print(
            f"INFO: skipping creation, an external id already exist for [{model}] [{source_record_id}]")
    else:
        try:
            target_record_id = target.env[model].create(fields)
            print(f"Recordset('{model}', [{target_record_id}]) created")
        except Exception as e:
            print(
                f"ERROR: target.env['{model}'].create ({source_record_id}) failed")
            print(f"e: {e}")
            return e
        print(create_xml_id(model, target_record_id, source_record_id))
        return 1


def migrate_model(model, migrate_fields=[], include = False, diff={}, custom={}, hard_code={}, debug=False, create=True):
    '''
    use this method for migrating a model with return dict from get_all_fields()
    example:
        product_template = get_all_fields(
            'product.template', exclude=['message_follower_ids'])
        simple_migrate_model('product.template', product_template)
    '''
    s = source.env[model]
    if not include:
        fields = get_all_fields(model, migrate_fields, diff)
    else:
        fields = {e:e for e in migrate_fields}
    for key in custom.keys():
        fields[key] = custom[key]
    #print(f"fields: {fields}")
    #print(s.read(1))
    errors = {'ERRORS:'}
    print(s.search([]))
    for r in s.search([]):
        
        target_record = get_target_record_from_id(model, r)
        if create and target_record:
            print(
                f"INFO: skipping creation, an external id already exist for [{model}] [{r}]")
            continue
        record = s.read(r, fields)
        record_fields = s.read(r, fields)
        if type(record_fields) is list:
            record_fields = record_fields[0]
        vals = {}
        # Customize certain fields before creating records
        for key in fields:
            # Remove /page if it exists in url (odoo v8 -> odoo 14)
            if key == 'url' and type(record[key]) is str:
                url = record[key]
                if url.startswith('/page'):
                    url = url.replace('/page', '')
                vals.update({fields[key]: url})

            # Stringify datetime objects
            # TypeError('Object of type datetime is not JSON serializable')
            elif type(record[key]) is datetime.datetime:
                vals.update({fields[key]: str(record[key])})

            # If the value of the key is a list, look for the corresponding record on target instead of copying the value directly
            # example: country_id 198, on source is 'Sweden' while
            #          country_id 198, on target is 'Saint Helena, Ascension and Tristan da Cunha'
            elif type(record_fields[key]) is list:
                field_definition = s.fields_get(key)[key]
                #print(f"type: {field_definition['type']}")
                if field_definition['type'] == 'many2one':
                    try:
                        #print(f"vals: {get_id_from_xml_id(record[key],field_definition['relation'])}")
                        vals.update({fields[key]: get_id_from_xml_id(record[key],field_definition['relation'])})
                        continue
                    except:
                        x = get_target_record_from_id(
                            field_definition['relation'], record[key][0])
                        if x:
                            vals.update({fields[key]: x.id})
                            continue
                        error = f"Target '{key}': {record[key]} does not exist"
                        if error not in errors:
                            errors.add(error)
                            if debug:
                                print(error)
                                

            # Just copy the value it it is not False
            elif record[key]:
                vals.update({fields[key]: record[key]})
        #vals.update(custom[])
        # Break operation and return last dict used for creating record if something is wrong and debug is True
        vals.update(hard_code)
        if create and create_record_and_xml_id(model, vals, r) != 1 and debug:
            return vals
        elif not create:
            try:
                target_record.write(vals)
                print(f"Writing to existing {record}")
            except:
                return vals

    return errors


def get_id_from_xml_id(record, relation):
    '''
    Returns a dict with { key: id } of target record
    example:
    source_record = source.env['res.company'].browse(1)
    get_target_id_from_source(source_record, 'country_id')
    '''
    #print(f"record: {record}, relation: {relation}")
    s = source.env['ir.model.data']
    d = [('model', '=', relation),
         ('res_id', '=', record[0])]
    r = target.env.ref(s.browse(s.search(d)).complete_name).id
    return r


def get_all_fields(model, exclude=[], diff={}):
    '''
    Returns dict with key as source model keys and value as target model keys
    Use exclude = ['this_field', 'that_field'] to exclude keys on source model
    Use diff = {'image':'image_1920'} to update key-value pairs manually
    '''
    fields = {}
    target_field_keys = target.env[model]._columns

    # for key, value in target.env[model].fields_get().items():
    #     if not value['readonly']:
    #         target_field_keys.append(key)

    for key in source.env[model]._columns:
        if key in exclude:
            continue
        elif key in target_field_keys:
            fields.update({key: key})

    fields.update(diff)

    return fields


def get_fields_difference(model):
    '''
    Returns list with fields difference
    example: get_fields_difference('res.company')
    '''
    source_set = set(source.env[model]._columns)
    target_set = set(target.env[model]._columns)

    return {'source': source_set - target_set, 'target': target_set - source_set}

def get_required_fields(model):
    '''
    Returns list with required fields
    example: get_required_fields('res.company')
    '''
    source_dict = source.env[model].fields_get()
    target_dict = target.env[model].fields_get()
    source_keys=[]
    target_keys=[]
    for key in source_dict:
        if source_dict[key]['required']:
            source_keys.append(key)
    for key in target_dict:
        if target_dict[key]['required']:
            target_keys.append(key)
    return {'source': source_keys, 'target': target_keys}

print(4)
