#!/usr/bin/env python3

# import http.client as http
import datetime
from termcolor import colored
from pprint import pprint
from bs4 import BeautifulSoup

try:
    import odoorpc
except ImportError:
    raise Warning(
        'odoorpc library missing. Please install the library. Eg: pip3 install odoorpc')

# http.HTTPConnection._http_vsn = 10
# http.HTTPConnection._http_vsn_str = 'HTTP/1.0'
D = colored('DEBUG:', 'white', 'on_green')
E = colored('ERROR:', 'red')
I = colored('INFO:', 'green')
W = colored('WARNING:', 'yellow')
IMPORT = '__import__'

source = odoorpc.ODOO.load('source')
source.env.context.update({'active_test': False})
print(f"{I} source.env\n{source.env}\n")

target = odoorpc.ODOO.load('target')
target.env.context.update({'mail_create_nolog': True,
                           'mail_create_nosubscribe': True,
                           'mail_notrack': True,
                           'tracking_disable': True,
                           'tz': 'UTC',
                           })

print(f"{I} target.env\n{target.env}\n")

for server in ['ir.mail_server', 'fetchmail.server']:
    if target.env[server].search([]):
        raise Warning(f"Active {server}")

target.env.context.update({'active_test': False})

""" Glossary
domain = list of search criterias as triplets ('id', '=', 2)
fields = what you get from source.env[model].read(id, [keys])
    id = number
   ids = what you get from source.env[model].search([])
 model = ex. 'res.partner'
     r = record, what you get from source.env[model].browse(id)
    rs = recordset, what you get from source.env[model].browse(ids)
source = source database
target = target database
"""


def unlink(model, only_migrated=True):
    """ unlinks all records of a model in target database
    example: unlink('res.partner')
    """
    record_list = []
    if only_migrated:
        domain = [('module', '=', IMPORT), ('model', '=', model)]
        record_list = [x.get('res_id') for x in target.env['ir.model.data'].search_read(
            domain, ['res_id'], order='id')]
    else:
        record_list = target.env[model].search([], order='id')

    try:
        target.env[model].unlink(record_list)
    except Exception as e:
        print(e)
    else:
        print(f"{I} Recordset('{model}', {record_list}) unlinked")
        return

    finally:
        option = input('Unlinking failed, unlink one record at a time? [y/N]')
        if option.lower() != 'n' or option != '':
            try:
                [target.env[model].unlink(x) for x in record_list]
            except Exception as e:
                print(e)


def create_xmlid(model, res_id, xmlid):
    module = xmlid.split('.')[0]
    vals = {'model': model,
            'module': module,
            'name': xmlid.split('.')[1],
            'res_id': res_id}
    if module != IMPORT:
        vals['noupdate'] = True

    try:
        target.env['ir.model.data'].create(vals)
    except:
        print(f"{E} TARGET: XML_ID: {xmlid} | CREATE: FAIL!"
              "Should not happen...Did you call this method manually?")
    else:
        print(f"{I} TARGET: XML_ID: {xmlid} | CREATE: SUCCESS!")


def get_target_id_from_source_id(model, source_id, module=IMPORT):
    """
    Returns id from target using id from source
    Ex, get_target_id_from_source_id('product.attribute', 3422)
    Returns: False if record cannot be found
    """
    xmlid = f"{module}.{model.replace('.', '_')}_{source_id}"
    return target.env['ir.model.data'].xmlid_to_res_id(xmlid)


def get_xmlid(name, ext_id, module=IMPORT):
    return f"{module}.{name.replace('.', '_')}_{ext_id}"


def get_res_id(xmlid):
    return target.env['ir.model.data'].xmlid_to_res_id(xmlid)


def get_target_id_from_source_xmlid(model, source_id):
    """
    Returns id from target using source xmlid
    Ex, get_target_id_from_source_xmlid('res.company', 1)
    Returns: False if record cannot be found
    """
    domain = [('model', '=', model), ('res_id', '=', source_id)]
    for _id in source.env['ir.model.data'].search(domain, order='id'):
        key = 'complete_name'
        data = source.env['ir.model.data'].read(_id, [key])
        if type(data) is list:
            data = data[0]
        xmlid = data.get(key)
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
    xmlid = get_xmlid(model, source_id)
    target_id = get_res_id(xmlid)
    if target_id:
        print(f"{I} External id already exist ({model2} {source_id})")
    else:
        try:
            target_id = target.env[model2].create(fields)
        except Exception as e:
            print(f"{E} SOURCE: {model} {source_id} | TARGET: {model2} {target_id}"
                  " | CREATE: FAIL! Read the log...", e)
        else:
            print(f"{I} SOURCE: {model} {source_id} | TARGET: {model2} {target_id}"
                  " | CREATE: SUCCESS! Creating external id...")
        try:
            create_xmlid(model2, target_id, xmlid)
        except Exception as e:
            print("Create xmlid FAILED", e)
        else:
            return target_id

    return 0


def migrate_model(model, **params):
    """
    Use this method for migrating model from source to target
    - Example: migrate_model('res.partner')
    - Keyworded arguments default values:

    Parameters
        - model (str) - Model to migrate records from source to target
        - **params : keyworded arguments
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
    def compare_values(record, model_fields, vals):
        input(f"{record=}") if debug else None
        for key in list(vals):
            value = record[key]
            field_type = model_fields.get(key).get('type')
            if field_type in ['many2one']:
                if type(value) is list and len(value) == 2:
                    value = value[0]
            elif field_type in ['one2many', 'many2many']:
                if type(vals[key]) is list:
                    for command in vals[key]:
                        if type(command) is list or tuple:
                            if command[0] == 4 and command[1] in value:
                                vals.pop(key)
                            if command[0] == 6 and set(command[2]) == set(value):
                                vals.pop(key)
                    continue
            elif field_type in ['binary']:
                binary = vals[key]
                if binary and '\n' in binary:
                    vals[key] = binary.replace('\n', '')
            if value == vals[key]:
                vals.pop(key)
            else:
                input(f"{value=}\n{vals[key]=}") if debug else None
        return vals

    def create_record_and_xmlid_or_update(model, vals, xmlid):

        def print_info(msg):
            print(f"{params.keys()=}")
            input(f"{msg}: {model=}, {vals=}, {xmlid=}")

        model_fields = get_fields(model)
        model_ids = get_ids(model)
        model_reads = get_reads(model, vals)

        if 'skip' in vals:
            if sync and debug:
                print_info('skip')
            return 0

        res_id = model_ids.get(xmlid)

        if not res_id:
            model_ids[xmlid] = {}
            res_id = get_res_id_from_xmlid(xmlid)

        if res_id:
            record = model_reads.get(res_id)
            vals = compare_values(record, model_fields, vals)

            if vals and not debug:
                target.env[model].write(res_id, vals)
                print(f"write: {model=}, {vals=}, {res_id=}, {xmlid=})")

        elif sync and not debug:
            res_id = target.env[model].create(vals)
            create_xmlid(model, res_id, xmlid)
            model_ids[xmlid] = res_id
            print(f"create: {model=}, {vals=}, {res_id=}, {xmlid=})")

        if vals:
            params['counter'] += 1

        print_info('debug') if debug else None
        return res_id

    def get_fields(model):
        model_fields = f"{model.replace('.', '_')}_fields_get"
        if model_fields not in params:
            params[model_fields] = target.env[model].fields_get()
            print(f"Added '{model_fields}'")
        return params[model_fields]

    def get_ids(model):
        model_ids = f"{model.replace('.', '_')}_ids"
        if model_ids not in params:
            params[model_ids] = {
                x['complete_name']: x['res_id']
                for x in target.env['ir.model.data'].search_read(
                    [('model', '=', model)])}
            print(f"Added '{model_ids}'")
        return params[model_ids]

    def get_reads(model, vals):
        model_reads = f"{model.replace('.', '_')}_reads"
        if model_reads not in params:
            model_ids = get_ids(model)
            params[model_reads] = {rec['id']: {key: rec[key] for key in vals}
                                   for rec in target.env[model].read([model_ids[id] for id in model_ids], vals)}
            print(f"Added '{model_reads}'")
        return params[model_reads]

    def get_source_reads(model, fields):
        source_model_reads = f"source_{model.replace('.', '_')}_reads"
        if source_model_reads not in params:
            params[source_model_reads] = (
                {record['id']: {field: record[field] for field in fields}
                 for record in source.env[model].search_read([], fields)})
            print(f"Added '{source_model_reads}'")
        return params[source_model_reads]

    def get_res_id(xmlid):
        if xmlid not in params:
            params[xmlid] = {}
        res_id = params[xmlid].get('res_id')
        if not res_id:
            res_id = get_res_id_from_xmlid(xmlid)
            if not res_id and 'model' in params[xmlid]:
                model = params[xmlid]['model']
                vals = params[xmlid]['vals']
                res_id = create_record_and_xmlid_or_update(
                    model, vals, xmlid)
            else:
                params[xmlid]['res_id'] = res_id
                print(f"Added '{xmlid}' = {res_id}")
        return res_id

    def get_res_ids(model):
        model_res_ids = f"{model.replace('.', '_')}_res_ids"
        if model_res_ids not in params:
            ids = source.env[model].search([], order='id')
            search_reads = source.env['ir.model.data'].search_read(
                [('model', '=', model),
                 ('res_id', 'in', ids)])
            params[model_res_ids] = {
                x['res_id']: x['complete_name'] for x in search_reads}
            print(f"Added '{model_res_ids}'")
        return params[model_res_ids]

    def get_res_id_from_xmlid(xmlid):
        return target.env['ir.model.data'].xmlid_to_res_id(xmlid)

    def get_search_read(model, key, domain=[]):
        search_read = f"{model.replace('.', '_')}_search_read"
        if search_read not in params:
            params[search_read] = {
                x[key]: x['id']
                for x in target.env[model].search_read(domain, [key])}
            print(f"Added '{search_read}'")
        return params[search_read]

    def vals_builder(source_read, fields):
        vals = {}
        for key in fields:
            value = source_read[key]
            field_type = source_fields[key]['type']
            input(f"{key=}, {field_type=}, {value=}") if debug else None
            if 'relation' in source_fields[key]:
                relation = source_fields[key]['relation']
                input(f"{relation=}") if debug else None
                if field_type in ['many2one']:
                    if type(value) is list and len(value) == 2:
                        val = value[0]
                        value_xmlid = get_xmlid(relation, val)
                        value = get_ids(relation).get(value_xmlid)
                        if not value:
                            value_xmlid = get_res_ids(relation).get(val)
                            value = get_ids(relation).get(value_xmlid)

                elif field_type in ['one2many', 'many2many'] and value:
                    value_list = []
                    for val in value:
                        value_xmlid = get_xmlid(relation, val)
                        value_id = get_ids(relation).get(value_xmlid)
                        if not value_id:
                            meta_id = source.env[relation].get_metadata(val)
                            if meta_id:
                                meta_xmlid = meta_id[0]['xmlid']
                                if meta_xmlid:
                                    value_id = get_res_id(meta_xmlid)

                        if value_id:
                            value_list.append(value_id)
                    if value_list:
                        value = [(6, 0, value_list)]

            elif field_type in ['binary']:
                vals[key] = value
                binary = vals[key]
                if binary and '\n' in binary:
                    vals[key] = binary.replace('\n', '')

            vals[key] = value
            input(f"{value=}") if debug else None
        input(f"{vals=}") if debug else None
        return vals

    after = params.pop('after', '')
    before = params.pop('before', '')
    debug = params.get('debug', False)
    domain = params.get('domain', [])
    fields = params.get('fields', [])
    model2 = params.get('model2', model)
    offset = params.get('offset', 0)
    sync = params.get('sync', True)

    source_model = source.env[model]
    target_model = target.env[model2]

    source_fields = source_model.fields_get()
    # target_fields = target_model.fields_get()
    # if not fields:
    #     fields = get_common_fields(source_fields, target_fields, **params)

    # source_ids = ids if ids else source_model.search(domain, order='id')
    # if not source_ids:
    #     f"{I} No records to migrate..."

    # if create:
    #     source_ids = find_all_ids_in_target_model(model2, source_ids, module)
    # now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    params['counter'] = 0
# MAIN LOOP
    source_reads = source_model.search_read(
        domain, fields, offset=offset, order='id')
    # for source_id in source_ids:
    for source_read in source_reads:
        xmlid = get_xmlid(model, source_read['id'])
        vals = vals_builder(source_read, fields)
        input(f"{before=}\n{after=}") if debug else None
        try:
            exec(before)
            create_record_and_xmlid_or_update(model2, vals, xmlid)
            exec(after)
        except Exception as e:
            print(f"{e=}")
            print(f"{source_read=}")
            print(f"{vals=}")
            print(f"{xmlid=}")
            print(E, f"Unexpected error when migrating {model}!")
            return

    #     target_id = 0 if create else get_target_id_from_source_id(
    #         model2, source_id, module)

    #     print(f"{D} Source record: '{model}' {source_id}"
    #           "{txt_d} Target record: '{model2}' {target_id}") if debug else None

    #     if not target_id:
    #         # if debug:
    #         print(f"{D} No record found with {IMPORT}.{model2.replace('.', '_')}"
    #               "_{source_id} external identifier") if debug else None
    #         target_id = get_target_id_from_source_xmlid(model2, source_id)

    #     if create and target_id:
    #         print(f"{W} SOURCE: {model} {source_id} | TARGET: {model2} {target_id}"
    #               " | CREATE: FAIL! External id exists...")
    #         continue

    #     if not create and not target_id:
    #         if not force:
    #             print(
    #                 f"{W} SOURCE: {model} {source_id} | TARGET: {model2} {target_id} | WRITE: FAIL! External id exists...")
    #             continue
    #         print(
    #             f"{I} FORCE = TRUE: External id exists...Trying to write to record")

    #     vals = {}
    #     try:
    #         record = source_model.read(source_id, list(fields))
    #         if not record:
    #             print(f'{source_id} does not exist...')
    #             continue
    #         elif type(record) is list:
    #             record = record[0]
    #     except:
    #         print(
    #             f"{E} SOURCE: {model} {source_id} READ: FAIL! Does the record exist?")
    #         if debug:
    #             return source_id
    #         continue

    #     if not create:
    #         last_migration_date = record.get('last_migration_date')
    #         if not last_migration_date:
    #             last_migration_date = str(datetime.datetime(2000, 1, 1))
    #         write_date = record.get('write_date')
    #         if not write_date:
    #             write_date = '0'
    #         if not bypass_date and last_migration_date > write_date:
    #             continue

    #     # Customize certain fields before creating records
    #     for key in sorted(fields):
    #         key_type = source_fields[key]['type']
    #         val = record[key]

    #         if debug:
    #             print(f"{D}     Field: {key}, Type: {key_type}")
    #             print(f"{D}         Source value: {val}")

    #         # if not val:
    #         #     print('')
    #         #     continue

    #         if key not in calc.keys():

    #             if key_type == 'many2one' and val:
    #                 relation = target_fields[key]['relation']
    #                 relation_id = get_target_id_from_source_id(
    #                     relation, record[key][0])
    #                 if not relation_id:
    #                     relation_id = get_target_id_from_source_xmlid(
    #                         relation, record[key][0])
    #                 if type(relation_id) is dict or not relation_id:
    #                     continue
    #                 val = relation_id

    #             elif key_type == 'many2many' and val:
    #                 relation = target_fields[key]['relation']
    #                 key_ids = []
    #                 values = 0
    #                 for many_id in record[key]:
    #                     relation_id = get_target_id_from_source_id(
    #                         relation, many_id)
    #                     if not relation_id:
    #                         relation_id = get_target_id_from_source_xmlid(
    #                             relation, many_id)
    #                     if not relation_id:
    #                         continue
    #                     key_ids.append(relation_id)
    #                 if command and key in command:
    #                     if command[key] == 6:
    #                         values = [6, 0]
    #                         values.append(key_ids)
    #                         values = [tuple(values)]
    #                 else:
    #                     values = key_ids
    #                 val = values

    #             elif key_type == 'one2many' and val:
    #                 relation = source_fields[key]['relation']
    #                 key_ids = []
    #                 values = 0
    #                 for many_id in record[key]:
    #                     relation_id = get_target_id_from_source_id(
    #                         relation, many_id)
    #                     if not relation_id:
    #                         relation_id = get_target_id_from_source_xmlid(
    #                             relation, many_id)
    #                     if not relation_id:
    #                         continue
    #                     key_ids.append(relation_id)
    #                 if command and key in command:
    #                     if command[key] == 4:
    #                         values = [tuple([4, key_ids[0], 0])]
    #                     if command[key] == 6:
    #                         values = [tuple([6, 0, key_ids])]
    #                 else:
    #                     values = key_ids
    #                 val = values

    #             elif key_type == 'integer':
    #                 if key == 'res_id' and 'res_model' in record:
    #                     res_model = record['res_model']
    #                     if not res_model:
    #                         continue
    #                     val = get_target_id_from_source_id(
    #                         res_model, record[key])
    #                     if not val:
    #                         val = get_target_id_from_source_xmlid(
    #                             res_model, record[key])

    #             elif key_type == 'char':
    #                 if key == 'arch':
    #                     val = update_images(record[key])

    #                 # Remove /page if it exists in url (odoo v8 -> odoo 14)
    #                 elif key == 'url' and type(record[key]) is str:
    #                     if val.startswith('/page'):
    #                         val = val.replace('/page', '')

    #             vals.update({fields[key]: val})

    #         print(f"""{D}         Target value: {val}""") if debug else None

    #     vals.update(custom)

    #     print(f"{D} Custom value: {custom}") if debug and custom else None

    #     if calc:
    #         for key in calc.keys():
    #             exec(calc[key])

    #     if vals.get('skip', None):
    #         continue

    #     # Break operation and return last dict used for creating record if something is wrong and debug is True
    #     if create and vals:
    #         create_id = create_record_and_xmlid(
    #             model, model2, vals, source_id)
    #         if not create_id:
    #             return vals
    #         elif ids and len(ids) == 1:
    #             return create_id
    #     elif target_id or force:
    #         try:
    #             success = target_model.write(target_id, vals)
    #             if success:
    #                 print(
    #                     f"{I} SOURCE: {model} {source_id} TARGET: {model2} {target_id} WRITE: SUCCESS!!!"
    #                 )
    #             else:
    #                 print(target_id)
    #                 return vals
    #         except:
    #             if not force:
    #                 print(
    #                     f"{E} SOURCE: {model} {source_id} TARGET: {model2} {target_id} WRITE: FAIL!"
    #                 )
    #                 return vals
    #             else:
    #                 create_id = create_record_and_xmlid(
    #                     model, model2, vals, source_id)
    #                 if not create_id:
    #                     return vals
    #                 elif ids and len(ids) == 1:
    #                     return create_id

    # for key in context:
    #     source.env.context.pop(key)
    #     target.env.context.pop(key)

    print(I, f"Done migrating {model}!")


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

    # for key in source_fields:
    #     if include:
    #         if key in include and key in target_fields:
    #             fields.update({key: key})
    #     elif exclude and key in exclude:
    #         continue
    #     else:
    #         if key in target_fields:
    #             fields.update({key: key})

    for key in source_fields:
        if key in target_fields:
            fields[key] = key

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
    input(f"{I} Press ENTER key to continue")
    print('target')
    for key in sorted(target_fields):
        if target_fields[key].get('relation', None):
            relation = target_fields[key]['relation']
            key_type = target_fields[key]['type']
            text = 'relation: {:<30} type: {:<10} key: {:<30}'
            print(text.format(relation, key_type, key))
    input(f"{I} The end")


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


def sync_webpages():
    """
    Syncs website pages on target using source pages' arch
    Before arch is used, a call to bootstrap3to4() is made
    Also updates each page's [is_published] to True
    """

    def remove_page_in_url(tag):
        href = tag['href']
        if href.startswith('/page'):
            new_value = href[5:]
            print(f"INFO: Replacing href "
                  f"{colored(href, 'red')} with "
                  f"{colored(new_value, 'green')}")
            href = new_value

    def update_src_values(tag):
        src = 'src'
        model = 'ir.attachment'
        i = new_value = source_id = 0
        if '/web/image/' in tag.attrs[src]:
            new_value = tag.attrs[src].split('/')
            i = new_value.index('web')
            new_value = new_value[i:]
            i = new_value.index('image')+1
            source_id = new_value[i]
        if source_id:
            target_id = get_target_id_from_source_id(model, source_id)
            new_value[i] = str(target_id)
            new_value = '/' + '/'.join(new_value)
            print(f"INFO: Replacing src "
                  f"{colored(tag.attrs[src], 'red')} with "
                  f"{colored(new_value, 'green')}")
            tag.attrs[src] = new_value

    def update_t_values(tag):
        model = source_id = 0
        t = 't-value'
        if 'request.env' in tag.attrs[t]:
            model = tag.attrs[t].split('\'')[1]
        if 'browse' in tag.attrs[t]:
            source_id = tag.attrs[t].split(
                '(')[-1].split(')')[0]
        if model and source_id:
            target_id = get_target_id_from_source_id(model, source_id)
            new_value = f"request.env['{model}'].sudo().browse({target_id})"
            print(f"{I} Replacing t-value "
                  f"{colored(tag.attrs[t], 'red')} with "
                  f"{colored(new_value, 'green')}")
            tag.attrs[t] = new_value

    def update_classes(tag):
        diff = {
            'carousel':             'carousel s_carousel s_carousel_default',
            'carousel-control':    {'left': 'carousel-control-prev o_not_editable o_we_no_overlay',
                                    'right': 'carousel-control-next o_not_editable o_we_no_overlay'},
            'carousel-indicators':  'carousel-indicators o_we_no_overlay',
            'col-xs-':              'col-',
            'col-sm-':              'col-md-',
            'col-md-':              'col-lg-',
            'img-responsive':       'img-fluid',
            'item':                 'carousel-item',
            'hidden-xs':            'd-none d-sm-block',
            'hidden-sm':            'd-sm-none d-md-block',
            'hidden-md':            'd-md-none d-lg-block',
            'hidden-lg':            'd-lg-none d-xl-block',
            'pull-left':            'float-left',
            'pull-right':           'float-right',
            'visible-xs':           'd-block d-sm-none',
            'visible-sm':           'd-block d-md-none',
            'visible-md':           'd-block d-lg-none',
            'visible-lg':           'd-block d-xl-none',
        }

        old_list = tag.attrs['class']
        new_list = []
        temp = ''
        for c in old_list:
            if c in diff:
                if type(diff[c]) is dict:
                    for e in diff[c]:
                        if e in old_list:
                            new_list.append(diff[c][e])
                            temp = e
                        if e in new_list:
                            new_list.remove(e)
                            temp = ''
                else:
                    new_list.append(diff[c])
            elif 'col' in c:
                d = c.split('-')
                no = d.pop()
                d = '-'.join(d) + '-'
                if d in diff:
                    new_list.append(diff[d]+no)
            elif c != temp:
                new_list.append(c)
            else:
                temp = ''

        if set(old_list) != set(new_list):
            print(f"{I} Replacing classes "
                  f"{colored(old_list, 'red')} with "
                  f"{colored(new_list, 'green')}")
            tag.attrs['class'] = new_list
        else:
            print(f"{colored(old_list, 'yellow')}")

    def update_styles(tag):
        model = 'ir.attachment'
        s = 'style'
        old_styles = [x.strip() for x in tag.attrs[s].split(';') if x]
        new_styles = []
        for old_style in old_styles:
            if 'background-image' in old_style:
                temp = old_style.split('"')
                if temp and len(temp) > 1:
                    source_id = temp[1].split('/')[-1]
                    target_id = get_target_id_from_source_id(model, source_id)
                    if target_id:
                        temp[1] = f"/web/image/{target_id}"
                        new_styles.append('"'.join(temp))
            else:
                new_styles.append(old_style)
        if set(old_styles) != set(new_styles):
            new_styles = '; '.join(new_styles)
            print(f"INFO: Replacing style "
                  f"{colored(tag.attrs[s], 'red')} with "
                  f"{colored(new_styles, 'green')}")
            tag.attrs[s] = new_styles
        else:
            print(f"{old_styles}")

    model = 'ir.ui.view'
    domain = [('type', '=', 'qweb'), ('page', '=', True)]
    arch, name, parser, view_id = ('arch', 'name', 'html.parser', 'view_id')
    for source_read in source.env[model].search_read(domain, [], order='id'):
        xmlid = get_xmlid(model, source_read['id'])
        target_id = get_res_id(xmlid)
        if not target_id:
            page = target.env['website'].new_page(name=source_read[name])
            page_id = target.env['website.page'].search(
                [(view_id, '=', page[view_id])])[0]
            create_xmlid(model, page[view_id], xmlid)
            target.env['website.page'].write(
                page_id, {'is_published': True, 'is_visible': True})
            target_id = get_res_id(xmlid)
            print(f"{I} Created new [{model}] and external id from source "
                  f" id [{source_read['id']}] [{source_read[name]}]")
            print(f"======================================================")
        else:
            source_arch = source_read[arch]
            soup = BeautifulSoup(source_arch, parser)
            for tag in soup.find_all():
                if 'href' in tag.attrs:
                    remove_page_in_url(tag)
                if 't-value' in tag.attrs:
                    update_t_values(tag)
                if 'src' in tag.attrs:
                    update_src_values(tag)
                if 'class' in tag.attrs:
                    update_classes(tag)
                if 'style' in tag.attrs:
                    update_styles(tag)
            target_arch = str(soup)
            if source_arch != target_arch:
                target.env[model].write(target_id, {arch: target_arch})
            input('next')

    print(f"{I} DONE!")


# def update_images(arch):
#     from bs4 import BeautifulSoup
#     model = 'ir.attachment'
#     soup = BeautifulSoup(arch, 'html.parser')
#     tag_list = ['div', 'img', 'span']
#     tags = soup.find_all(tag_list)

#     for tag in tags:
#         attr = t = url = ''
#         at = 'access_token'
#         if tag.name == 'img' and tag.has_attr('src'):
#             attr = 'src'
#         elif tag.name in ['div', 'span'] and tag.has_attr('style'):
#             attr = 'style'
#         if attr:
#             url = tag[attr].split('/')
#         if attr and url and 'web' in url and 'image' in url:
#             i = url.index('image')+1
#             source_id = target_id = 0
#             t = ''
#             if url[i].isdigit():
#                 source_id = int(url[i])
#             elif at in url[i]:
#                 url_split = url[i].split('?')
#                 source_id = url_split[0]
#                 t = url_split[1]
#                 if source_id.isdigit():
#                     source_id = int(source_id)
#             else:
#                 pass

#             if source_id:
#                 target_id = get_target_id_from_source_id(model, source_id)
#                 # if source_id exists but cannot find in target, try migrating it, doing it manually takes too much time
#                 if not target_id:
#                     try:
#                         migrate_model(model, ids=[source_id])
#                     except:
#                         print(f"{E} {source_id}")
#             if target_id:
#                 url[i] = str(target_id)
#                 if t:
#                     t = target.env[model].read(target_id, [at])[0][at]
#                     url[i] += f"?{at}={t}"

#             tag[attr] = '/'.join(url)

#     return str(soup)


def find_all_ids_in_target_model(target_model, ids=[], module='__import__'):
    print(target_model)
    # target_ids = target.env["ir.model.data"].find_all_ids_in_target(
    #     target_model, module)
    target_ids = target.env["ir.model.data"].search([
        ('module', '=', module),
        ('model', '=', target_model)
    ])
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
        [('module', '=', IMPORT), ('model', '=', model)], ['res_id']))
    ids = []
    for value in values:
        source_ids = source.env[model].search([(field, '=', value)])
        target_ids = target.env[model].search(
            [('id', '=', res_ids), (field, '=', value)])
        migrated_ids = sorted(int(x.get('name').split('_')[-1]) for x in target.env['ir.model.data'].search_read(
            [('module', '=', IMPORT), ('model', '=', model), ('res_id', '=', target_ids)], ['name']))
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
                  ('module', '=', IMPORT),
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


print(f"{I} functions loaded")
