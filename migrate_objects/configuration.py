#!/usr/bin/env python3
import datetime
import argparse
import json
import logging
import logging.handlers
import os

import pprint
pp = pprint.PrettyPrinter()

from odoo import models, fields, api, http, registry
import odoo


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
target.env.context['active_test'] = False
source.env.context['active_test'] = False
print(2)
# HELPER FUNCTIONS
IMPORT_MODULE_STRING = '__import__'

# TODO: Skriv en robust funktion för detta. ID beror på databasen. Denna
#  metod fungerar bara för exakt den databas som listan togs fram för.
UNITS_OF_MEASURE = {
    21: 228,
    1: 227,
    8: 233,
    17: 230,
    22: 233,
    25: 239,
    26: 240,
    2: 229,
    34: 229,
    3: 229,
    36: 230,
    37: 230,
    4: 249,
    5: 250,
    6: 251,
    33: 229,
    10: 232,
    11: 231,
    14: 235,
    27: 241,
    28: 242,
    29: 243,
    13: 234,
    23: 236,
    31: 245,
    30: 244,
    24: 237,
    32: 246,
    35: 227,

}

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
    except Exception:
        return f"ERROR: create_xml_id('{model}', {target_record_id}, {source_record_id}) failed. Does the id already exist?"
        
def map_record_to_xml_id(target_model, field, value, source_id):
    print(field, value)
    r_id = target.env[target_model].search([(field, '=', value)])
    print(r_id)
    if r_id != []:
        print(create_xml_id(target_model, r_id[0], source_id))
    
# ~ map_record_to_xml_id('account.account', 'code', '2710123', 10)


def get_target_record_from_id(model, source_record_id):
    ''' gets record from target database using record.id from source database
    example: get_target_record_from_id('product.attribute', 3422)
    returns: 0 if record cannot be found
    '''
    try:
        # ~ r = target.env.ref(f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}", raise_if_not_found=False)
        r = target.env['ir.model.data'].xmlid_to_res_model_res_id(f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}", raise_if_not_found=False)
        if r != [False, False]:
            r = target.env[r[0]].browse(r[1])
            print(f"r {r}")
            return r
        else:
            print(f"couldnt find external id: {IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
            return 0
    except Exception:
        print(f"couldnt find external id: {IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
        return 0
    
def get_target_date_from_id(model, t, source_record_id):
    ''' gets record from target database using record.id from source database
    example: get_target_record_from_id('product.attribute', 3422)
    returns: 0 if record cannot be found
    '''
    try:
        # ~ r = target.env.ref(f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}", raise_if_not_found=False)
        r = target.env['ir.model.data'].xmlid_to_res_model_res_id(f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}", raise_if_not_found=False)
        if r != [False, False]:
            r = t.read(r[1], ['last_migration_date'])
            return r
        else:
            print(f"couldnt find external id: {IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
            return 0
    except Exception as e:
        print(f"couldnt find external id: {IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
        print(e)
        return 0
        
def create_record_and_xml_id(target_model, source_model, fields, source_record_id, unique=None):
    ''' Creates record on target if it doesn't exist, using fields as values,
    and creates an external id so that the record will not be duplicated
    example: create_record_and_xml_id('res.partner', {'name':'MyPartner'}, 2)
    '''
    print(f"Fields: {fields}")
    if get_target_record_from_id(target_model, source_record_id):
        print(
            f"INFO: skipping creation, an external id already exist for [{model}] [{source_record_id}]")
    else:
        try:
            target_record_id = target.env[target_model].create(fields)
            print(f"Recordset('{target_model}', [{target_record_id}]) created")
        except Exception as e:
            print(f"fields: {fields}")
            print(f"ERROR: target.env['{target_model}'].create ({source_record_id}) failed")
            if str(e).find('unique') != -1 and unique != None:
                map_record_to_xml_id(target_model, unique, fields[unique], source_record_id)
            else:
                print(f"e: {e}")
            return e
        print(create_xml_id(target_model, target_record_id, source_record_id))
        return 1

import re
def get_trailing_number(s):
    m = re.search(r'\d+$', s)
    return int(m.group()) if m else None


def find_all_ids_in_target_model(target_model, ids=[]):
    print(target_model)
    target_ids = target.env["ir.model.data"].find_all_ids_in_target(target_model)
    # ~ print(f"source_ids: {ids}")
    # ~ print("="*99)
    # ~ print(f"target_ids: {target_ids}")
    to_migrate = (set(ids) - set(target_ids))
    return to_migrate


def migrate_model(model, migrate_fields=[], include = False, diff={}, custom={}, hard_code={}, debug=False, create=True, domain=None, unique=None):
    '''
    use this method for migrating a model with return dict from get_all_fields()
    example:
        product_template = get_all_fields(
            'product.template', exclude=['message_follower_ids'])
        simple_migrate_model('product.template', product_template)
    '''
    print()
    print("="*99)
    print(f"Migrating model: {model}")
    print()
    domain = domain or []
    source_model = model
    target_model = model
    if type(model) == dict:
        source_model = list(model.keys())[0]
        target_model = model[list(model.keys())[0]]

    s = source.env[source_model]
    t = target.env[target_model]
    if not include:
        fields = get_all_fields(source_model, target_model, migrate_fields, diff)
    else:
        fields = {e:e for e in migrate_fields}
    for key in custom.keys():
        fields[key] = custom[key]
    errors = {'ERRORS:'}
    if create:
        to_migrate = s.search(domain)
        to_migrate = find_all_ids_in_target_model(target_model, to_migrate)
    elif not create:
        to_migrate = s.search_read(domain, ['id', 'write_date'], order='write_date DESC')
    # ~ print("to migrate:")
    # ~ print(to_migrate)
    for r in to_migrate:
        if not create:
            
            t_date = get_target_date_from_id(target_model, t, r['id'])
            if t_date[0]['last_migration_date'] == False or t_date[0]['last_migration_date'] < r['write_date']:
                r = r['id']
            else:
                # ~ print(f"record: {r}. is already up to date")
                continue
            
        
        target_record = get_target_record_from_id(target_model, r)
        if create and target_record:
            print(
                f"INFO: skipping creation, an external id already exist for [{target_model}] [{r}]")
            continue
        # WTF? Sending a dict to read. Seems to work, but it sure feels icky.
        record = s.read(r, fields)
        if type(record) is list:
            record = record[0]
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
            elif type(record[key]) is list:
                field_definition = s.fields_get(key)[key]
                if field_definition['type'] == 'many2one':
                    # ~ print(f"field_definition: {field_definition}")
                    try:
                        if field_definition["relation"] == "product.uom":
                            vals.update({fields[key]:  UNITS_OF_MEASURE[record[key][0]]})
                        else:
                            vals.update({fields[key]: get_target_record_from_id(field_definition['relation'], record[key][0]).id})
                        continue
                    except Exception:
                        error = f"Target '{key}': {[record[key], field_definition['relation']]} does not exist"
                        if error not in errors:
                            errors.add(error)
                            if debug:
                                print(error)
                elif field_definition['type'] in ('one2many', 'many2many'):
                    # Convert every id in the list
                    ids = []
                    for id in record[key]:
                        ids.append(
                            get_target_record_from_id(
                                field_definition['relation'], id).id)
                    vals[fields[key]] = ids
            else:
                vals[fields[key]] = record[key]
        #vals.update(custom[])
        # Break operation and return last dict used for creating record if something is wrong and debug is True
        vals.update(hard_code)
        if create and create_record_and_xml_id(target_model, source_model, vals, r, unique) != 1 and debug:
            return vals
        elif not create:
            try:
                # We will never get here if target_record exists...
                vals.update({'last_migration_date': str(odoo.fields.Datetime.now())})
                target_record.write(vals)
                print(f"Writing to existing {vals}")
            except Exception as e:
                print(f"Failed at writing to existing {vals}")
                print(e)
                return vals

    return errors

def get_relations_from_model(database, model):
    # ~ SELECT Distinct(model), name FROM ir_model_fields WHERE relation='product.uom' ;
    s = database.env['ir.model.fields']
    search_terms = [('relation', '=', model)]
    results = s.browse(s.search(search_terms))
    used_uom = {}
    for result in results:
        try:
            print(f"model: {result.model}, name: {result.name}")
            ref_model = database.env[result.model]
            res = ref_model.search([])
            uom_id = 0
            for r in res:
                uom_id = ref_model.read(r, [result.name])[result.name][0]
                if not uom_id in used_uom.keys():
                    used_uom[uom_id] = 1
                else:
                    used_uom[uom_id] += 1
        except Exception:
            print(f"model: {result.model} doesnt exist")
        print(used_uom)




def get_id_from_xml_id(record, relation):
    '''
    Returns a dict with { key: id } of target record
    example:
    source_record = source.env['res.company'].browse(1)
    get_target_id_from_source(source_record, 'country_id')
    '''
    print(f"record: {record}, relation: {relation}")
    s = source.env['ir.model.data']
    d = [('model', '=', relation),
         ('res_id', '=', record[0])]
    r = target.env.ref(s.browse(s.search(d)).complete_name).id
    print(f"r: {r}")
    return r


def get_all_fields(source_model, target_model, exclude=[], diff={}):
    '''
    Returns dict with key as source model keys and value as target model keys
    Use exclude = ['this_field', 'that_field'] to exclude keys on source model
    Use diff = {'image':'image_1920'} to update key-value pairs manually
    '''
    fields = {}
    target_field_keys = target.env[target_model]._columns

    # for key, value in target.env[model].fields_get().items():
    #     if not value['readonly']:
    #         target_field_keys.append(key)

    for key in source.env[source_model]._columns:
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
