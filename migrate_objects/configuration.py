#!/usr/bin/env python3
import datetime
import argparse
import json
import logging
import logging.handlers
import os
import pprint
import re

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

source_se = odoorpc.ODOO.load('source')
target_se = odoorpc.ODOO.load('target')
source.env.context['lang'] = 'sv_SE'
target.env.context['lang'] = 'sv_SE'
target.env.context['active_test'] = False
source.env.context['active_test'] = False
print(2)
# HELPER FUNCTIONS
IMPORT_MODULE_STRING = '__import__'

                # ~ if 'in_group_' in key:
                    # ~ print("start_ingroup")
                    # ~ s_id = re.findall(r'\d+', key)[0]
                    # ~ print(s_id)
                    # ~ t_id = target.env.ref(IMPORT_MODULE_STRING+'.'+'res_groups_'+str(s_id)).res_id
                    
                    # ~ t_id = target.env['ir.model.data'].search_read([
                            # ~ ('model', '=', 'res.groups'),
                            # ~ ('name', '=', f'res_groups_{s_id}')], ['res_id'])[0]['res_id']
                    # ~ print(t_id)
                    # ~ vals.update({'in_group_'+str(t_id): (record[key])})
                    # ~ print("end_ingroup")

# TODO: Skriv en robust funktion för detta. ID beror på databasen. Denna
#  metod fungerar bara för exakt den databas som listan togs fram för.
COMPANY_ID = 1

UNITS_OF_MEASURE_EXID = {
    5: 'product_uom_cl',
    23: 'product_uom_cm',
    11: 'product_uom_day',
    4: 'product_uom_dl',
    21: 'product_uom_dozen',
    30: 'product_uom_floz',
    28: 'product_uom_foot',
    17: 'product_uom_gram',
    32: 'product_uom_gal',
    37: 'product_uom_gram',
    36: 'product_uom_gram',
    10: 'product_uom_hour',
    27: 'product_uom_inch',
    2: 'product_uom_kgm',
    33: 'product_uom_kgm',
    34: 'product_uom_kgm',
    3: 'product_uom_kgm',
    14: 'product_uom_km',
    25: 'product_uom_lb',
    24: 'product_uom_litre',
    13: 'product_uom_meter',
    29: 'product_uom_mile',
    6: 'product_uom_ml',
    26: 'product_uom_oz',
    1: 'product_uom_unit',
    31: 'product_uom_qt',
    35: 'product_uom_unit',
    22: 'product_uom_ton',
    8: 'product_uom_ton'
}

UNITS_OF_MEASURE = {}


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
        
def map_record_to_xml_id(target_model, fields, unique, source_id):
    if unique:
        domain = [(item, '=', fields[item]) for item in unique]
        r_id = target.env[target_model].search(domain)
        print(r_id)
        if r_id != []:
            print(create_xml_id(target_model, r_id[0], source_id))
            return True
    return False
    
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
            return False
    except Exception:
        print(f"couldnt find external id: {IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
        return False
        
def get_target_id_from_id(model, source_record_id):
    ''' gets record from target database using record.id from source database
    example: get_target_record_from_id('product.attribute', 3422)
    returns: 0 if record cannot be found
    '''
    try:
        # ~ r = target.env.ref(f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}", raise_if_not_found=False)
        r = target.env['ir.model.data'].xmlid_to_res_model_res_id(f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}", raise_if_not_found=False)
        if r != [False, False]:
            print(f"r {r[1]}")
            return r[1]
        else:
            print(f"couldnt find external id: {IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
            return False
    except Exception:
        print(f"couldnt find external id: {IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
        return False
    
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
            return r[0]['last_migration_date']
        else:
            print(f"couldnt find external id: {IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
            return False
    except Exception as e:
        print(f"couldnt find external id: {IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
        print(e)
        return False
        
def create_record_and_xml_id(target_model, source_model, fields, source_record_id, unique=None, i18n_fields=None):
    ''' Creates record on target if it doesn't exist, using fields as values,
    and creates an external id so that the record will not be duplicated
    example: create_record_and_xml_id('res.partner', {'name':'MyPartner'}, 2)
    '''
    if get_target_record_from_id(target_model, source_record_id):
        print(
            f"INFO: skipping creation, an external id already exist for [{model}] [{source_record_id}]")
    else:
        try:

            target_record_id = target.env[target_model].create(fields)
            print(f"Recordset('{target_model}', [{target_record_id}]) created")
            migrate_translation(source_model, target_model,
                                source_record_id, target_record_id,
                                i18n_fields)
            print(f"Recordset('{target_model}', [{target_record_id}]) translated")
            print(create_xml_id(target_model, target_record_id, source_record_id))
            return target_record_id
        except Exception as e:
            print(f"ERROR: target.env['{target_model}'].create ({source_record_id}) failed")
            if not map_record_to_xml_id(target_model, fields, unique, source_record_id):
                if 'image_1920' in fields.keys():
                    fields.pop('image_1920')
                print(f"Fields: {fields}")
                print(f"couldnt find the target record")
                print(f"e: {e}")

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

def get_translatable_fields(t_model, s_model, fields: dict) -> dict:
    """ Return all fields that are translatable in both source
    and target.
    :returns: dict with source and target fields.
    """
    res = {}
    t_fields = t_model.fields_get(list(fields.values()))
    for name, field_data in s_model.fields_get(list(fields.keys())).items():
        if field_data.get('translate') and t_fields[fields[name]].get('translate'):
            res[name] = fields[name]
    return res

def migrate_translation(source_model, target_model, source_id, target_id, fields):
    """ Migrate swedish translations for the given source and
    target records.
    """
    # TODO: Recreate for multiple languages.
    if not fields:
        return
    vals = {}
    s_record = source_se.env[source_model].search_read([('id', '=', source_id)], list(fields.keys()))
    s_record = s_record and s_record[0] or None
    if not s_record:
        return
    # TODO: not an exact replica of fields in migrate_model. Look into
    #  that. Not every feature is needed, since this function will only
    #  handle translateable fields. This includes Char, Text and Html
    #  fields. Any more?
    for name, value in s_record.items():
        if name != 'id':
            vals[fields[name]] = value
    target_se.env[target_model].write([target_id], vals)
    
def get_uom_ids():
    uom_xmlid_values = UNITS_OF_MEASURE_EXID.values()
    for data in target.env['ir.model.data'].search_read([
            ('model', '=', 'uom.uom'),
            ('name', '=like', 'product_uom_%'),
            ('module', '=', 'uom')], ['res_id', 'name']):
        for key in UNITS_OF_MEASURE_EXID.keys():
            if UNITS_OF_MEASURE_EXID[key] == data['name']:
                UNITS_OF_MEASURE[key] = data['res_id']
    pprint.pprint(UNITS_OF_MEASURE)
get_uom_ids()
    
def migrate_model(model, migrate_fields=[], include = False, exclude_patterns = [], diff={}, custom={}, hard_code={}, debug=False, create=True, domain=None, unique=None, after_migration=None, calc=None, xml_id_suffix = None):
    '''
    use this method for migrating a model with return dict from get_all_fields()
    example:
        product_template = get_all_fields(
            'product.template', exclude=['message_follower_ids'])
        simple_migrate_model('product.template', product_template)
    :param after_migration: Custom method run after migration of a record.
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
        fields = get_all_fields(source_model, target_model, migrate_fields, custom, exclude_patterns)
    else:
        fields = {e:e for e in migrate_fields}
    for key in custom.keys():
        fields[key] = custom[key]
    i18n_fields = get_translatable_fields(s, t, fields)
    errors = {'ERRORS:'}
    # Set migration date before reading. Otherwise we may miss updates in next migration.
    now = odoo.fields.Datetime.now()
    if create:
        to_migrate = s.search(domain)
        to_migrate = find_all_ids_in_target_model(target_model, to_migrate)
        print("to migrate:")
        print(to_migrate)
    elif not create:
        to_migrate = s.search_read(domain, ['id', 'write_date'], order='write_date DESC')

    print(f'fields to migrate: {fields}')
    for r in to_migrate:
        print("="*99)
        print(f"Migrating model: {model}")
        if not create:
            t_date = get_target_date_from_id(target_model, t, r['id'])
            print(f"t_date: {t_date}, {r['write_date']}")
            if t_date == False or r['write_date'] == False or t_date < r['write_date']:
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
        record = s.read(r, list(fields.keys()))
        print(f"record: {record}")
        if type(record) is list:
            record = record[0]
        vals = {}
        # Customize certain fields before creating records
        for key in fields:
            print(record[key])
            # Remove /page if it exists in url (odoo v8 -> odoo 14)
            if not calc or key not in calc.keys():
                if key == 'company_id':
                    vals.update({'company_id': 1})
                elif key == 'url' and type(record[key]) is str:
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
                    print(f"field_definition: {field_definition}")
                    if field_definition['type'] == 'many2one':
                        try:
                            if field_definition["relation"] == "product.uom":
                                vals.update({fields[key]:  UNITS_OF_MEASURE[record[key][0]]})
                            elif field_definition["relation"] == "res.company":
                                vals.update({fields[key]: COMPANY_ID})
                            else:
                                vals.update({fields[key]: get_target_id_from_id(field_definition['relation'], record[key][0])})
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
                            rec = get_target_id_from_id(field_definition['relation'], id)
                            if rec:
                                ids.append(rec)
                        if ids:
                            vals[fields[key]] = [(6,0,ids)]
                else:
                    vals[fields[key]] = record[key]
        #vals.update(custom[])
        # Break operation and return last dict used for creating record if something is wrong and debug is True
        vals.update(hard_code)

        if calc:
            for key in calc.keys():
                print(calc[key])
                exec(calc[key])
        if create:
            target_record_id = create_record_and_xml_id(target_model, source_model, vals, r, unique, i18n_fields)
            print(after_migration)
            if after_migration:
                after_migration(record['id'], target_record_id, create=True)
            if type(target_record_id) != int and debug:
                return vals
        elif target_record:
            try:
                vals.update({'last_migration_date': str(now)})
                image = False
                if 'image_1920' in vals.keys():
                    image = vals.pop('image_1920')
                target_record.write(vals)
                print(f"Writing to existing {vals}")
                try:
                    target_record.write({'image_1920': image})
                    print(f"Writing image to existing")
                except Exception as e:
                    print(f"writing image failed")
                    print(e)
                migrate_translation(source_model, target_model, record['id'], target_record.id, i18n_fields)
                print(f"migrated translation")
                if after_migration:
                    after_migration(record['id'], target_record.id, create=False)
                    print(f"after_migration")
            except Exception as e:
                if 'image_1920' in vals.keys():
                    vals.pop('image_1920')
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


def get_all_fields(source_model, target_model, exclude=[], diff={}, exclude_patterns=[]):
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
        if exclude_patterns:
            for exclude_pattern in exclude_patterns:
                if re.search(exclude_pattern, key):
                    print(f'skipping key {key}')
                    exclude.append(key)
        if key in exclude:
            print(f'skipping key {key}')
            continue
        elif key in target_field_keys:
            fields.update({key: key})
            print(f'adding key {key}')

    fields.update(diff)
    print(fields, diff)

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
