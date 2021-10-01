#!/usr/bin/env python3
import http.client as http
from termcolor import colored, cprint
from PIL import Image
import sys
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


try:
    import odoorpc
except ImportError:
    raise Warning(
        'odoorpc library missing. Please install the library. Eg: pip3 install odoorpc')


http.HTTPConnection._http_vsn = 10
http.HTTPConnection._http_vsn_str = 'HTTP/1.0'

source = odoorpc.ODOO.load('source')
target = odoorpc.ODOO.load('target')
odoorpc_context = {'active_test': False}
source.env.context.update(odoorpc_context)
target.env.context.update(odoorpc_context)

txt_d = colored('DEBUG:', 'white', 'on_green')
txt_e = colored('ERROR:', 'red')
txt_i = colored('INFO:', 'green')
txt_w = colored('WARNING:', 'yellow')
IMPORT_MODULE_STRING = '__import_bure__'
# IMPORT_MODULE_STRING = '__import__'

print(f"{txt_i} source.env\n{source.env}")
print(f"{txt_i} source.host\n{source.host}")
print(f"{txt_i} source.db.list()\n{source.db.list()}\n")
print(f"{txt_i} target.env\n{target.env}")
print(f"{txt_i} target.host\n{target.host}")
print(f"{txt_i} target.db.list()\n{target.db.list()}\n")

''' Glossary
domain = list of search criterias
fields = what you get from source.env[model].read(id, [keys])
    id = number
   ids = what you get from source.env[model].search([])
 model = ex. 'res.partner'
     r = record, what you get from source.env[model].browse(id)
    rs = recordset, what you get from source.env[model].browse(ids)
source = source database
target = target database
'''


def unlink(model, only_migrated=True):
    """ unlinks all records of a model in target database
    example: unlink('res.partner')
    """
    record_list = []
    if only_migrated:
        domain = [('module', '=', IMPORT_MODULE_STRING), ('model', '=', model)]
        record_list = sorted((x.get('res_id') for x in target.env['ir.model.data'].search_read(
            domain, ['res_id'])), reverse=1)
    else:
        record_list = sorted(target.env[model].search([]), reverse=1)

    try:
        target.env[model].unlink(record_list)
        print(
            f"{txt_i} Recordset('{model}', {record_list}) unlinked"
        )
    except Exception as e:
        print(e)
        choice = input(
            'Unlinking failed, try to unlink one record at a time? [y/N]')
        if choice.lower() != 'n' or choice != '':
            for x in record_list:
                try:
                    target.env[model].unlink(x)
                except Exception as e:
                    print(e)


def create_xmlid(model, target_record_id, source_record_id, module=IMPORT_MODULE_STRING):
    """ Creates an external id for a model
    example: create_xml_id('product.template', 89122, 5021)
    """

    xml_id = f"{module}.{model.replace('.', '_')}_{source_record_id}"
    values = {
        'module': xml_id.split('.')[0],
        'name': xml_id.split('.')[1],
        'model': model,
        'res_id': target_record_id,
    }
    try:
        target.env['ir.model.data'].create(values)
        print(f"{txt_i} TARGET: XML_ID: {xml_id} | CREATE: SUCCESS!")
    except:
        print(
            f"{txt_e} TARGET: XML_ID: {xml_id} | CREATE: FAIL! Should not happen...Did you call this method manually?"
        )


def get_target_id_from_source_id(model, source_id, module=IMPORT_MODULE_STRING):
    """
    Returns id from target using id from source
    Ex, get_target_id_from_source_id('product.attribute', 3422)
    Returns: False if record cannot be found
    """
    xmlid = f"{module}.{model.replace('.', '_')}_{source_id}"
    return target.env['ir.model.data'].xmlid_to_res_id(xmlid)


def get_target_id_from_source_xmlid(model, source_id):
    """
    Returns id from target using source xmlid
    Ex, get_target_id_from_source_xmlid('res.company', 1)
    Returns: False if record cannot be found
    """
    domain = [('model', '=', model), ('res_id', '=', source_id)]
    for _id in sorted(source.env['ir.model.data'].search(domain)):
        key = 'complete_name'
        data = source.env['ir.model.data'].read(_id, [key])
        if type(data) is list:
            data = data[0]
        xmlid = data.get(key, None)
        if xmlid:
            target_id = target.env['ir.model.data'].xmlid_to_res_id(xmlid)
            if target_id:
                return target_id
    return False


def create_record_and_xmlid(model, model2, fields, source_id):
    """
    Creates record on target if it doesn't exist, using fields as values,
    and creates an external id so that the record will not be duplicated if function is called next time

    Example: create_record_and_xml_id('res.partner', {'name':'MyPartner'}, 2)

    Returns 0 if function fails
    """
    target_id = get_target_id_from_source_id(model2, source_id)
    if target_id:
        print(f"{txt_i} External id already exist ({model2} {source_id})")
    else:
        try:
            target_id = target.env[model2].create(fields)
            print(f"{txt_i} SOURCE: {model} {source_id} | TARGET: {model2} {target_id} | CREATE: SUCCESS! Creating external id...")
            create_xmlid(model2, target_id, source_id)
            return target_id
        except Exception as e:
            print(
                f"{txt_e} SOURCE: {model} {source_id} | TARGET: {model2} {target_id} | CREATE: FAIL! Read the log...")
            print(e)
            return 0


def migrate_model(model, **vars):
    """
    Use this method for migrating model from source to target
    - Example: migrate_model('res.partner')
    - Keyworded arguments default values:

    Parameters
        - model (str) - Model to migrate records from source to target
        - **vars : keyworded arguments
            - calc    (dict) - Runs code on specific fields, default {}
            - context (dict) - Sets context to source and target, default {}
            - create  (bool) - Creates records, set to False to update records, default True
            - custom  (dict) - Updates vals before create/write, default {}
            - debug   (bool) - Shows debug messages, default False
            - domain  (list) - Migrate records that matches search criteria, i.e [('name','=','My Company')], default []
            - diff    (dict) - If field names don't match in source and target i.e {'image':'image_1920'}, default {}
            - exclude (list) - Excludes certain fields in source i.e ['email_formatted'], default []
            - ids     (list) - Provide your own record ids to migrate i.e [1,3], default []
            - include (list) - Provide your own list of fields names to migrate ['name','email'], default []
            - model2  (str)  - Migrate records to another model, default same as model

    Returns
        - vals (dict) if create/write fails
        - id   (int)  if create succeeds
    """
    bypass_date = vars.get('bypass_date', False)
    calc = vars.get('calc', {})
    command = vars.get('command', {})
    context = vars.get('context', {})
    create = vars.get('create', True)
    custom = vars.get('custom', {})
    debug = vars.get('debug', False)
    domain = vars.get('domain', [])
    force = vars.get('force', [])
    ids = vars.pop('ids', [])
    model2 = vars.get('model2', model)
    module = vars.get('module', IMPORT_MODULE_STRING)
    source.env.context.update(context)
    target.env.context.update(context)

    if debug:
        print(f"""
{txt_d} Source context: {source.env.context}
{txt_d} Target context: {target.env.context}
{txt_d} vars: {vars}
""")

    source_model = source.env[model]
    target_model = target.env[model2]

    source_fields = source_model.fields_get()
    target_fields = target_model.fields_get()
    fields = get_common_fields(source_fields, target_fields, **vars)

    source_ids = ids if ids else source_model.search(domain, order='id')
    if not source_ids:
        f"{txt_i} No records to migrate..."

    if create:
        source_ids = find_all_ids_in_target_model(model2, source_ids, module)
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
# MAIN LOOP
    for source_id in source_ids:
        target_id = 0 if create else get_target_id_from_source_id(
            model2, source_id, module)

        print(f"{txt_d} Source record: '{model}' {source_id}"
              "{txt_d} Target record: '{model2}' {target_id}") if debug else None

        if not target_id:
            # if debug:
            print(f"{txt_d} No record found with {IMPORT_MODULE_STRING}.{model2.replace('.', '_')}"
                  "_{source_id} external identifier") if debug else None
            target_id = get_target_id_from_source_xmlid(model2, source_id)

        if create and target_id:
            print(f"{txt_w} SOURCE: {model} {source_id} | TARGET: {model2} {target_id}"
                  " | CREATE: FAIL! External id exists...")
            continue

        if not create and not target_id:
            if not force:
                print(
                    f"{txt_w} SOURCE: {model} {source_id} | TARGET: {model2} {target_id} | WRITE: FAIL! External id exists...")
                continue
            print(
                f"{txt_i} FORCE = TRUE: External id exists...Trying to write to record")

        vals = {'last_migration_date': now}
        try:
            record = source_model.read(source_id, list(fields))
            if not record:
                print(f'{source_id} does not exist...')
                continue
            elif type(record) is list:
                record = record[0]
        except:
            print(
                f"{txt_e} SOURCE: {model} {source_id} READ: FAIL! Does the record exist?")
            if debug:
                return source_id
            continue

        if not create:
            last_migration_date = record.get('last_migration_date')
            if not last_migration_date:
                last_migration_date = str(datetime.datetime(2000, 1, 1))
            write_date = record.get('write_date')
            if not write_date:
                write_date = '0'
            if not bypass_date and last_migration_date > write_date:
                continue

        # Customize certain fields before creating records
        for key in sorted(fields):
            key_type = source_fields[key]['type']
            val = record[key]

            if debug:
                print(f"{txt_d}     Field: {key}, Type: {key_type}")
                print(f"{txt_d}         Source value: {val}")

            # if not val:
            #     print('')
            #     continue

            if key not in calc.keys():

                if key_type == 'many2one' and val:
                    relation = target_fields[key]['relation']
                    relation_id = get_target_id_from_source_id(
                        relation, record[key][0])
                    if not relation_id:
                        relation_id = get_target_id_from_source_xmlid(
                            relation, record[key][0])
                    if type(relation_id) is dict or not relation_id:
                        continue
                    val = relation_id

                elif key_type == 'many2many' and val:
                    relation = target_fields[key]['relation']
                    key_ids = []
                    values = 0
                    for many_id in record[key]:
                        relation_id = get_target_id_from_source_id(
                            relation, many_id)
                        if not relation_id:
                            relation_id = get_target_id_from_source_xmlid(
                                relation, many_id)
                        if not relation_id:
                            continue
                        key_ids.append(relation_id)
                    if command and key in command:
                        if command[key] == 6:
                            values = [6, 0]
                            values.append(key_ids)
                            values = [tuple(values)]
                    else:
                        values = key_ids
                    val = values

                elif key_type == 'one2many' and val:
                    relation = source_fields[key]['relation']
                    key_ids = []
                    values = 0
                    for many_id in record[key]:
                        relation_id = get_target_id_from_source_id(
                            relation, many_id)
                        if not relation_id:
                            relation_id = get_target_id_from_source_xmlid(
                                relation, many_id)
                        if not relation_id:
                            continue
                        key_ids.append(relation_id)
                    if command and key in command:
                        if command[key] == 4:
                            values = [tuple([4, key_ids[0], 0])]
                        if command[key] == 6:
                            values = [tuple([6, 0, key_ids])]
                    else:
                        values = key_ids
                    val = values

                elif key_type == 'integer':
                    if key == 'res_id' and 'res_model' in record:
                        res_model = record['res_model']
                        if not res_model:
                            continue
                        val = get_target_id_from_source_id(
                            res_model, record[key])
                        if not val:
                            val = get_target_id_from_source_xmlid(
                                res_model, record[key])

                elif key_type == 'char':
                    if key == 'arch':
                        val = update_images(record[key])

                    # Remove /page if it exists in url (odoo v8 -> odoo 14)
                    elif key == 'url' and type(record[key]) is str:
                        if val.startswith('/page'):
                            val = val.replace('/page', '')

                vals.update({fields[key]: val})

            print(f"""{txt_d}         Target value: {val}""") if debug else None

        vals.update(custom)

        print(f"{txt_d} Custom value: {custom}") if debug and custom else None

        if calc:
            for key in calc.keys():
                exec(calc[key])

        # Break operation and return last dict used for creating record if something is wrong and debug is True
        if create and vals:
            create_id = create_record_and_xmlid(
                model, model2, vals, source_id)
            if not create_id:
                return vals
            elif ids and len(ids) == 1:
                return create_id
        elif target_id or force:
            try:
                success = target_model.write(target_id, vals)
                if success:
                    print(
                        f"{txt_i} SOURCE: {model} {source_id} TARGET: {model2} {target_id} WRITE: SUCCESS!!!"
                    )
                else:
                    print(target_id)
                    return vals
            except:
                if not force:
                    print(
                        f"{txt_e} SOURCE: {model} {source_id} TARGET: {model2} {target_id} WRITE: FAIL!"
                    )
                    return vals
                else:
                    create_id = create_record_and_xmlid(
                        model, model2, vals, source_id)
                    if not create_id:
                        return vals
                    elif ids and len(ids) == 1:
                        return create_id

    for key in context:
        source.env.context.pop(key)
        target.env.context.pop(key)

    print(txt_i, f"Done!")


def get_common_fields(source_fields, target_fields, **kwargs):
    """
    Returns dict with key as source model fields and value as target model fields
    :param source_fields: dict, use source.env[model].fields_get()
    :param target_fields: dict, use target.env[model].fields_get()
    :param diff: dict, different fields on target i.e. {'image':'image_1920'}
    :param exclude: list, fields to exclude on source model ['message_follower_ids']
    :param include: list, fields to include on source model ['partner_id']
    """
    diff = kwargs.get('diff', {})
    exclude = kwargs.get('exclude', [])
    include = kwargs.get('include', [])
    fields = {}

    for key in source_fields:
        if include:
            if key in include and key in target_fields:
                fields.update({key: key})
        elif exclude and key in exclude:
            continue
        else:
            if key in target_fields:
                fields.update({key: key})

    fields.update(diff)

    return fields


def get_fields_difference(model):
    """
    Returns list with fields difference

    Example: get_fields_difference('res.company')
    """
    source_set = set(source.env[model]._columns)
    target_set = set(target.env[model]._columns)

    return {
        'source': source_set - target_set,
        'target': target_set - source_set
    }


def get_required_fields(model):
    """
    Returns list with required fields

    Example: get_required_fields('res.company')
    """
    source_dict = source.env[model].fields_get()
    target_dict = target.env[model].fields_get()
    source_keys = []
    target_keys = []
    for key in source_dict:
        if source_dict[key]['required']:
            source_keys.append(key)
    for key in target_dict:
        if target_dict[key]['required']:
            target_keys.append(key)
    return {'source': source_keys, 'target': target_keys}


def print_relation_fields(model, model2=''):
    """Prints model name for relation fields"""
    source_fields = source.env[model].fields_get()
    target_fields = target.env[model2 or model].fields_get()
    print('source')
    for key in sorted(source_fields):
        if source_fields[key].get('relation', None):
            relation = source_fields[key]['relation']
            key_type = source_fields[key]['type']
            text = 'relation: {:<30} type: {:<10} key: {:<30}'
            print(text.format(relation, key_type, key))
    input(f"{txt_i} Press ENTER key to continue")
    print('target')
    for key in sorted(target_fields):
        if target_fields[key].get('relation', None):
            relation = target_fields[key]['relation']
            key_type = target_fields[key]['type']
            text = 'relation: {:<30} type: {:<10} key: {:<30}'
            print(text.format(relation, key_type, key))
    input(f"{txt_i} The end")


def print_list(my_list, rows=40):
    from pprint import pprint
    count = len(my_list)
    begin = 0
    end = rows
    for x in range(int(count/rows)):
        pprint(my_list[begin:end])
        begin = end
        end = end + rows
        input()


def compare_records(model, source_id, key_len=150, rows=14):
    if type(model) is str:
        model = {model: model}
    for s, t in model.items():
        source_fields = source.env[s].fields_get()
        target_fields = target.env[t].fields_get()
        keys = sorted(set(list(source_fields)+list(target_fields)))
        count = 1
        target_id = get_target_id_from_source_id(t, source_id)
        if not target_id:
            target_id = get_target_id_from_source_xmlid(s, source_id)
        for key in keys:
            source_val = source_rel = source_type = ''
            target_val = target_rel = target_type = ''
            if count % rows == 1:
                print(
                    f"{'field name':^40}{'source type':^20}{'source model':^20}{'target type':^20}{'target model':^20}")
            if key in source_fields:
                source_type = source_fields[key]['type']
                if source_type in ['many2many', 'many2one', 'one2many']:
                    source_rel = source_fields[key]['relation']
                try:
                    source_val = source.env[s].read(source_id, [key])
                    if type(source_val) is list:
                        source_val = source_val[0]
                    source_val = str(source_val.get(
                        key, 'Key not found'))[:key_len]
                except:
                    source_val = 'error'
            else:
                source_val = colored('Key not found', 'red')

            if key in target_fields:
                target_type = target_fields[key]['type']
                if target_type in ['many2many', 'many2one', 'one2many']:
                    target_rel = target_fields[key]['relation']
                try:
                    target_val = str(target.env[t].read(target_id, [key])[
                        0].get(key, 'Key not found'))[:key_len]
                except:
                    target_val = 'error'

            else:
                target_val = colored('Key not found', 'red')

            print(f"""{key:^40}{source_type:^20}{source_rel:^20}{target_type:^20}{target_rel:^20}
S {source_val}
T {target_val}""")
            if count % rows == 0:
                input()
            count = count+1


def create_new_webpages(model, ids=[]):
    """ Creates new website pages on target using source pages' arch
    """
    if not ids:
        ids = sorted(source.env[model].search([]))
    for _ in ids:
        source_val = source.env[model].read(_)[0]
        source_arch = update_images(source_val['arch'])
        source_id = source_val['id']
        source_name = source_val['name']
        target_id = get_target_id_from_source_id(
            'website_page', source_val['id'])
        if target_id:
            print(
                f"{txt_i} SOURCE: {model} {source_id} | TARGET: {model} {target_id} | CREATE: FAIL! External id exists...")
            continue
        new_page = target.env['website'].new_page(name=source_name)
        create_xmlid(model, new_page['view_id'], source_id)
        new_record = target.env['ir.ui.view'].browse(new_page['view_id'])
        new_record.arch = source_arch
        print(
            f"INFO: Created new [{model}] and external id from source id [{source_id}] [{source_name}]")
        print('=================================================================================================')
    print(colored('DONE:', 'green'))


def update_images(arch):
    from bs4 import BeautifulSoup
    model = 'ir.attachment'
    soup = BeautifulSoup(arch, 'html.parser')
    tag_list = ['div', 'img', 'span']
    tags = soup.find_all(tag_list)

    for tag in tags:
        attr = t = url = ''
        at = 'access_token'
        if tag.name == 'img' and tag.has_attr('src'):
            attr = 'src'
        elif tag.name in ['div', 'span'] and tag.has_attr('style'):
            attr = 'style'
        if attr:
            url = tag[attr].split('/')
        if attr and url and 'web' in url and 'image' in url:
            i = url.index('image')+1
            source_id = target_id = 0
            t = ''
            if url[i].isdigit():
                source_id = int(url[i])
            elif at in url[i]:
                url_split = url[i].split('?')
                source_id = url_split[0]
                t = url_split[1]
                if source_id.isdigit():
                    source_id = int(source_id)
            else:
                pass

            if source_id:
                target_id = get_target_id_from_source_id(model, source_id)
                # if source_id exists but cannot find in target, try migrating it, doing it manually takes too much time
                if not target_id:
                    try:
                        migrate_model(model, ids=[source_id])
                    except:
                        print(f"{txt_e} {source_id}")
            if target_id:
                url[i] = str(target_id)
                if t:
                    t = target.env[model].read(target_id, [at])[0][at]
                    url[i] += f"?{at}={t}"

            tag[attr] = '/'.join(url)

    return str(soup)


def find_all_ids_in_target_model(target_model, ids=[], module='__import__'):
    print(target_model)
    target_ids = target.env["ir.model.data"].find_all_ids_in_target(
        target_model, module)
    # ~ print(f"source_ids: {ids}")
    # ~ print("="*99)
    # ~ print(f"target_ids: {target_ids}")
    to_migrate = sorted(set(ids) - set(target_ids))
    return to_migrate


def compare(model, source_id=0):
    def get_list(x):
        return x[0] if type(x) is list else x

    if type(model) is str:
        model = {model: model}
    s = list(model)[0]
    t = model[s]
    if not source_id:
        source_id = sorted(source.env[s].search([]))[0]
    target_id = get_target_id_from_source_id(t, source_id)
    count = 0

    sf = source.env['ir.model.fields'].search_read(
        [('model', '=', s)], ['name'])
    tf = target.env['ir.model.fields'].search_read(
        [('model', '=', t)], ['name'])
    sr = get_list(s.env[s].read(source_id))
    tr = get_list(target.env[t].read(target_id))

    fields = sorted(set([x['name'] for x in sf] + [x['name'] for x in tf]))

    for key in fields:
        count += 1
        print(count, end=' ')
        try:
            print(colored(f"{key}", 'green'), sr[key])
        except:
            print(
                colored(f"key error ({colored(key, 'green')}{colored(')', 'red')}", 'red'))

        space = ' '*(len(str(count))+len(key)+1)
        try:
            print(space, tr[key])
        except:
            print(colored(f"key error ({key})", 'red'))
        if count % 10 == 0:
            input('Press ENTER to continue')


def find_field_diff(model, field, values):
    """Returns list of ids where field values mismatch
    :param model: str
    :param field: str
    :param value: list
    """
    print(model, field, values)
    res_ids = sorted(x.get('res_id') for x in target.env['ir.model.data'].search_read(
        [('module', '=', IMPORT_MODULE_STRING), ('model', '=', model)], ['res_id']))
    ids = []
    for value in values:
        source_ids = source.env[model].search([(field, '=', value)])
        target_ids = target.env[model].search(
            [('id', '=', res_ids), (field, '=', value)])
        migrated_ids = sorted(int(x.get('name').split('_')[-1]) for x in target.env['ir.model.data'].search_read(
            [('module', '=', IMPORT_MODULE_STRING), ('model', '=', model), ('res_id', '=', target_ids)], ['name']))
        diff = sorted(set(migrated_ids)-set(source_ids))
        if diff:
            print(f'value:  {value}')
            print(f'source: {len(source_ids)}')
            print(f'target: {len(target_ids)}')
            ids += diff
            print(f'diff  : {diff}')

    return ids


def check_field(m, f):
    def get_list_item(x):
        return x[1] if type(x) is list else x
    i = 'id'
    st_ids = {int(x['name'].split('_')[-1]): x['res_id']
              for x in target.env['ir.model.data'].search_read([
                  ('module', '=', IMPORT_MODULE_STRING),
                  ('model', '=', m)], order='name')}
    s = source.env[m]
    t = target.env[m]
    sids = {x[i]: x[f] for x in s.read(
        sorted(target.env['ir.model.data'].find_all_ids_in_target(m)), [f])}
    tids = {x[i]: x[f] for x in t.search_read([], [f], order=i)}
    for sid in sids:
        tid = st_ids[sid]
        sf = get_list_item(sids[sid])
        tf = get_list_item(tids[tid])
        if not sf == tf:
            print(f"s({sid}):", sf, "!=", f"({tid}):", tf)
    print('DONE!')


def map_ids_from_module_1to2(model, ids, module, module2):
    for sid in ids:
        metadata = source.env[model].get_metadata(sid)[0]
        try:
            mid = metadata['xmlid'].split('_')[-1]
        except:
            print('mid is False')
        tid = get_target_id_from_source_id(model, mid, module)
        if tid:
            if get_target_id_from_source_id(model, sid, module2):
                tid = get_target_id_from_source_id(model, sid, module2)
                print('exist')
            else:
                create_xmlid(model, tid, sid)
        print({tid: sid})


print(f"{txt_i} functions loaded")
