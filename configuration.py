#!/usr/bin/env python3

# region migrate_model
# import http.client as http
import datetime
from webbrowser import get
from pprint import pprint
from bs4 import BeautifulSoup

try:
    import odoorpc
except ImportError:
    raise Warning(
        'odoorpc library missing. Please install the library. Eg: pip3 install odoorpc')


class Colorcodes(object):
    Green = '\033[92m'
    Green_bg = '\033[102;5m'
    Grey100 = '\033[38;5;242m\033[48;5;231m'
    LightPink1 = '\033[38;5;239m\033[48;5;217m'
    SteelBlue1 = '\033[38;5;237m\033[48;5;81m'
    Red = '\033[91m'
    Red_bg = '\033[101;5m'
    Reset = '\033[0m'
    Yellow = '\033[33m'  # 33, 93
    Yellow_bg = '\033[43;5m'  # 43, 103

    def __init__(self):
        self.num = 0

    def green_fg(self, text):
        return self.Green + text + self.Reset

    def green_bg(self, text):
        return self.Green_bg + text + self.Reset

    def transgender(self, text):
        self.num += 1
        if self.num % 4 == 1:
            return self.SteelBlue1 + text + self.Reset
        if self.num % 4 in [2, 0]:
            return self.LightPink1 + text + self.Reset
        if self.num % 4 == 3:
            return self.Grey100 + text + self.Reset

    def red_fg(self, text):
        return self.Red + text + self.Reset

    def red_bg(self, text):
        return self.Red_bg + text + self.Reset

    def yellow_bg(self, text):
        return self.Yellow_bg + text + self.Reset

    def yellow_fg(self, text):
        return self.Yellow + text + self.Reset


color = Colorcodes()

gb = color.green_bg
gf = color.green_fg
rb = color.red_bg
rf = color.red_fg
tg = color.transgender
yb = color.yellow_bg
yf = color.yellow_fg

# http.HTTPConnection._http_vsn = 10
# http.HTTPConnection._http_vsn_str = 'HTTP/1.0'
IMPORT = '__import__'

source = odoorpc.ODOO.load('source')
source.env.context.update({'active_test': False})
print(gf(f"source.version = {source.version}\n"
         f"source.env     = {source.env}\n"))
source.__name__ = 'source'
target = odoorpc.ODOO.load('target')
target.env.context.update({'mail_create_nolog': True,
                           'mail_create_nosubscribe': True,
                           'mail_notrack': True,
                           'tracking_disable': True,
                           'tz': 'UTC',
                           })
target.__name__ = 'target'
tv = target.version
print(gf(f"target.version = {target.version}\n"
         f"target.env     = {target.env}\n"))

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


def get_res_id_from_conn(conn, domain=None, xmlid=None):
    if xmlid:
        res = conn.env['ir.model.data'].search_read([
            ('module', '=', xmlid.split('.')[0]),
            ('name', '=', xmlid.split('.')[1]),
        ], ['res_id'], limit=1)
        return res[0]['res_id'] if res else 0
    elif domain:
        return conn.env['ir.model.data'].search_read(domain)


def map_records_manually(source_model, target_model=None, source_field=None, target_field=None, mapping=None):
    s = source.env[source_model]
    t = target.env[target_model or source_model]
    source_field = source_field or 'id'
    target_field = target_field or source_field
    s_reads = s.search_read([], [source_field], order='id')
    t_reads = t.search_read([], [target_field], order='id')
    for s_id, t_id in mapping.items():
        print(next(filter(lambda read: read['id'] == s_id, s_reads))[
              source_field])
        target_id = next(filter(lambda read: read['id'] == t_id, t_reads))
        print(target_id[target_field])
        xmlid = get_xmlid(source_model, s_id)
        if get_res_id_from_conn(target, xmlid=xmlid) == target_id['id']:
            print(f"{xmlid} exists already...")
        elif input('Map records?').lower() == 'y':
            create_xmlid(t._name, res_id=t_id, xmlid=xmlid)


def map_existing_records(source_model, target_model=None, source_field=None, target_field=None):
    s = source.env[source_model]
    t = target.env[target_model or source_model]
    s_reads = s.search_read([], [source_field or 'id'], order='id')
    t_reads = t.search_read(
        [], [target_field or source_field or 'id'], order='id')
    metadatas = s.get_metadata([r['id'] for r in s_reads])
    for read in s_reads:
        metadata = next(
            filter(lambda meta: meta['id'] == read['id'], metadatas))
        import_xmlid = get_xmlid(source_model, read['id'])
        xmlid = metadata['xmlid']
        if not (res_id := get_res_id_from_conn(target, xmlid=xmlid)):
            if source_field or target_field:
                s_value = read[source_field]
                res_ids = list(
                    filter(lambda r: r[target_field or source_field] == s_value, t_reads))
                print(res_ids)
                if len(res_ids) == 1:
                    res_id = res_ids[0]['id']
        if res_id and not get_res_id_from_conn(target, xmlid=import_xmlid):
            create_xmlid(target_model or source_model,
                         xmlid=import_xmlid, res_id=res_id)


def print_xmlids(conn, model, field=None, active_test=False, limit=0):
    reads = conn.env[model].with_context(active_test=active_test).search_read([], [
        field or 'id'], limit=limit, order='id')
    metadatas = conn.env[model].with_context(
        active_test=active_test).get_metadata([read['id'] for read in reads])
    for read in reads:
        metadata = next(filter(lambda r: r['id'] == read['id'], metadatas))
        print(f"{metadata['id']}{' '*(3-len(str(metadata['id'])))}"
              f"{metadata['xmlid']}{' '*(45-len(str(metadata['xmlid'])))}"
              f"{read[field or 'id']}")


def create_xmlid(model, xmlid, res_id):
    _model = 'ir.model.data'
    module = xmlid.split('.')[0]
    vals = dict(module=module,
                name=xmlid.split('.')[1],
                noupdate=module != IMPORT,
                res_id=res_id)
    if isinstance(model, odoorpc.models.MetaModel):
        vals['model'] = model._name
        model = model.env[_model]
    else:
        vals['model'] = model
        model = target.env[_model]
    _name = model.__name__.upper()

    try:
        res = model.create(vals)
    except:
        print(rb(f"{_name}: XML_ID: {xmlid} | CREATE: FAIL!"),
              rf("Should not happen...Did you call this method manually?"),
              vals)
    else:
        print(gb(f"{_name}: XML_ID: {xmlid} | CREATE: SUCCESS!"))
        return model.read(res)


def get_xmlid(name, ext_id, module=IMPORT):
    return f"{module}.{name.replace('.', '_')}_{ext_id}"


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
            if not (field := model_fields.get(key)):
                raise KeyError(f"Key not found '{key}'")
            field_type = field.get('type')
            if key in record:
                value = record[key]
                if field_type in ['many2one']:
                    if isinstance(value, list) and len(value) == 2:
                        value = value[0]
                elif field_type in ['one2many', 'many2many']:
                    if isinstance(value, list):
                        for command in vals[key]:
                            if isinstance(command, (list, tuple)):
                                if command[0] == 4 and command[1] in value:
                                    vals.pop(key)
                                if command[0] == 6 and set(command[2]) == set(value):
                                    vals.pop(key)
                # elif field_type in ['binary']:
                #     binary = vals[key]
                #     if binary and '\n' in binary:
                #         vals[key] = binary.replace('\n', '')
                if value == vals.get(key):
                    vals.pop(key)
        return vals

    def compress_dict(dictionary, sep="\n"):
        if isinstance(dictionary, dict):
            return sep.join([f"{k}: {str(v)[:50] + '...' if len(str(v)) > 50 else v}" for k, v in dictionary.items()])

    def migrate_record(model, vals, xmlid):
        _vals = None

        def print_info(msg):
            print(f"{params.keys()=}")
            input(f"{msg}: {model=}, {vals=}, {xmlid=}")

        if 'skip' in vals:
            if sync and debug:
                print_info('skip')
            return 0

        if (res_id := search(model, xmlid=xmlid)):
            if (record := read(model, fields=vals, res_id=res_id)):
                vals = compare_values(record, fields_get(model), vals)
                if vals and not debug:
                    model.write(res_id, vals)
                    print(yb('UPDATE'), yf(
                        f"{model._name}\n"
                        f"vals={compress_dict(vals)}\n"
                        f"[ID={res_id}, {xmlid=}])"))
            else:
                print(rb('UPDATE'), rf(
                    f"Record not found, {record=}, you need to update or "
                    f"delete {xmlid=} to resolve this!"))

        elif sync and not debug:
            res_id = model.create(vals)
            data_id = create_xmlid(model, xmlid, res_id)[0]
            search(model).append(dict(id=data_id['id'],
                                      complete_name=data_id['complete_name'],
                                      res_id=data_id['res_id']))
            print(gb('CREATE'), gf(
                f"{model._name}\nvals={compress_dict(vals)}\n[ID={res_id}, {xmlid=}])"))

        if vals:
            params['counter'] += 1
        print_info('debug') if debug else None
        return res_id

    def dot2u(text):
        return str(text).replace('.', '_')

    def args2key(*args):
        return '_'.join([dot2u(arg.__name__ if hasattr(arg, '__name__') else str(arg)) for arg in args])

    def fields_get(model):
        key = args2key(model._odoo, model, fields_get)
        if key not in params:
            params[key] = model.fields_get()
            print(tg(f"params['{key}'] ({len(params[key])} fields)"))
        return params[key]

    # def get_ids(model):
    #     model_ids = f"{model.replace('.', '_')}_ids"
    #     if model_ids not in params:
    #         res_ids = get_res_id_from_conn(target, [('model', '=', model)])
    #         params[model_ids] = {x['complete_name']
    #             : x['res_id'] for x in res_ids}
    #         print(f"get_ids - params['{model_ids}']")
    #     return params[model_ids]

    def find(model, field, value, fields=[]):
        def get(record):
            if (fields_get(model)[field]['type'] == 'many2one' and isinstance(record[field], list)):
                return record[field][0] == value
            return record[field] == value
        key = args2key(model._odoo, model, find, field, value)
        if key not in params:
            params[key] = {}
        if value in (param := params[key]):
            return param[value]
        reads = read(model, fields)
        if (found := next(filter(get, reads), [])):
            param[value] = found
        return found or []

    def read(model, fields=None, res_id=None):
        def get(record):
            return record['id'] == res_id
        key = args2key(model._odoo, model, read)
        if key not in params:
            params[key] = model.search_read([], fields or [])
            print(tg(f"params['{key}'] ({len(params[key])} records)"))
        param = params[key]
        if res_id:
            return next(filter(get, param), 0)
        return param

    def search(model, res_id=None, xmlid=None):
        def get(record):
            return record['res_id'] == res_id if res_id else record['complete_name'] == xmlid
        key = args2key(model._odoo, model, search)
        if key not in params:
            params[key] = model.env['ir.model.data'].search_read(
                [('model', '=', model._name)], ['complete_name', 'res_id'])
            print(tg(f"params['{key}'] ({len(params[key])} records)"))
        param = params[key]
        if res_id:
            return next(filter(get, param), {}).get('complete_name', 0)
        if xmlid:
            return next(filter(get, param), {}).get('res_id', 0)
        return param

    # def get_reads(model, field_list=None):
    #     model_reads = f"{model.replace('.', '_')}_reads"
    #     if model_reads not in params:
    #         model_ids = get_ids(model)
    #         params[model_reads] = {rec['id']: {key: rec[key] for key in field_list}
    #                                for rec in target.env[model].read([model_ids[id] for id in model_ids], field_list)}
    #         print(f"get_reads - params['{model_reads}']")
    #     return params[model_reads]

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
        param = params.get(xmlid)
        if not (res_id := param.get('res_id', 0)):
            res_id = get_res_id_from_conn(target, xmlid=xmlid)
            if not res_id and 'model' in params[xmlid]:
                res_id = migrate_record(
                    param['model'], param['vals'], xmlid)
            if res_id:
                param['res_id'] = res_id
                print(tg(f"params[{xmlid}] = {res_id}"))
        return res_id

    def get_res_ids(model):
        model_res_ids = f"{model.replace('.', '_')}_res_ids"
        if model_res_ids not in params:
            ids = source.env[model].search([], order='id')
            search_reads = get_res_id_from_conn(source, domain=[
                ('model', '=', model),
                ('res_id', 'in', ids)])
            params[model_res_ids] = {
                x['res_id']: x['complete_name'] for x in search_reads}
            print(f"Added '{model_res_ids}'")
        return params[model_res_ids]

    def get_search_read(model, key, domain=[]):
        search_read = f"{model.replace('.', '_')}_search_read"
        if search_read not in params:
            params[search_read] = {
                x[key]: x['id']
                for x in target.env[model].search_read(domain, [key])}
            print(f"Added '{search_read}'")
        return params[search_read]

    def vals_builder(data):
        vals = {}
        for tkey, skey in mapping.items():
            if not skey:
                skey = tkey
            if skey in source_fields_get:
                value = data[skey]
                field_type = source_fields_get[skey]['type']
                input(f"{skey=}, {field_type=}, {value=}") if debug else None
                if 'relation' in source_fields_get[skey]:
                    s_model = source_fields_get[skey]['relation']
                    t_model = target_fields_get[tkey]['relation']
                    source_relation = source.env[s_model]
                    target_relation = target.env[t_model]
                    input(
                        f"{source_relation} => {target_relation}") if debug else None
                    if field_type in ['many2one']:
                        if isinstance(value, list) and len(value) == 2:
                            val = value[0]
                            value_xmlid = get_xmlid(s_model, val)
                            if not (value := search(target_relation, xmlid=value_xmlid)):
                                value_xmlid = search(
                                    source_relation, res_id=val)
                                value = search(target_relation,
                                               xmlid=value_xmlid)

                    elif field_type in ['one2many', 'many2many'] and value:
                        value_list = []
                        for val in value:
                            val_xmlid = get_xmlid(s_model, val)
                            if not (value_id := search(target_relation, xmlid=val_xmlid)):
                                val_xmlid = search(source_relation, res_id=val)
                                value_id = search(
                                    target_relation, xmlid=val_xmlid)
                            if value_id:
                                value_list.append(value_id)
                        value = [(6, 0, value_list)] if value_list else False

                elif field_type in ['binary']:
                    vals[tkey] = value
                    binary = vals[tkey]
                    if binary and '\n' in binary:
                        vals[tkey] = binary.replace('\n', '')

                vals[tkey] = value
                input(f"{value=}") if debug else None
            else:
                print(
                    f"{skey} not found in source.env['{model}']") if debug else None
        input(f"{vals=}") if debug else None
        return vals

    after = params.pop('after', '')
    before = params.pop('before', '')
    context = params.pop('context', {})
    debug = params.get('debug', False)
    domain = params.get('domain', [])
    mapping = params.get('mapping', {})
    target_fields = params.get('target_fields', [])
    source_fields = params.get('source_fields', [])
    model2 = params.get('model2', model)
    reads = params.get('reads', [])
    offset = params.get('offset', 0)
    limit = params.get('limit', 0)
    sync = params.get('sync', True)

    source_model = source.env[model]
    target_model = target.env[model2]

    source_fields_get = fields_get(source_model)
    target_fields_get = fields_get(target_model)
    params['counter'] = 0
    if context:
        target.env.context.update(context)
# MAIN LOOP
    source_reads = source_model.search_read(
        domain, source_fields + [v if v else k for k, v in mapping.items()], limit=limit, offset=offset, order='id')

    # search(model2)
    # read(model2, sorted(target_fields + list(mapping)))
    # for source_id in source_ids:
    errors = []
    for data in source_reads:
        xmlid = get_xmlid(model, data['id'])
        vals = vals_builder(data)
        input(f"{before=}\n{after=}") if debug else None
        try:
            exec(before)
            res = migrate_record(target_model, vals, xmlid)
            exec(after)
        except Exception as e:
            print(f"{e=}")
            errors.append(f"vals={compress_dict(vals)}, {xmlid=}")
        #     _source_read = {k: str(v)[0:50]+'...' if len(str(v)) >
        #                     50 else v for k, v in data.items()}
        #     print(f"{_source_read=}")
        #     _vals = {k: str(v)[0:50]+'...' if len(str(v)) >
        #              50 else v for k, v in vals.items()}
        #     print(f"{_vals=}")
        #     print(f"{xmlid=}")
        #     print(E, f"Unexpected error when migrating {model}!")
        #     return

    print(gb(f"Done migrating {model}!"))
    return errors if errors else f"No errors ({limit=}, {offset=})"


def compare_records(source_model, source_id, target_model=None, target_id=None):
    s = source.env[source_model]
    t = target.env[target_model or source_model]

    s_fields = s.fields_get()
    t_fields = t.fields_get()

    xmlid = get_xmlid(source_model, source_id)
    target_id = target_id or get_res_id_from_conn(target, xmlid=xmlid)

    s_read = s.read(source_id)
    t_read = t.read(target_id)

    s_read = s_read[0] if isinstance(s_read, list) else s_read
    t_read = t_read[0] if isinstance(t_read, list) else t_read

    count = 1
    for key in sorted(set(list(s_fields)+list(t_fields))):
        if count % 20 == 1:
            print(f"{'field name':.<42}{'field type':.<20}{'relation':.<20}")
        sf_rel = sf_type = sr_val = '.'
        tf_rel = tf_type = tr_val = '.'
        if key in s_fields:
            sf_type = s_fields[key]['type']
            if sf_type in ['many2many', 'many2one', 'one2many']:
                sf_rel = s_fields[key]['relation']
            sr_val = s_read[key]
        else:
            sr_val = 'Key not found'

        if key in t_fields:
            tf_type = t_fields[key]['type']
            if tf_type in ['many2many', 'many2one', 'one2many']:
                tf_rel = t_fields[key]['relation']
            tr_val = t_read[key]
        else:
            tr_val = 'Key not found'

        print(key)
        print(f"S {str(sr_val):.<40}{sf_type:.<20}{sf_rel:.<20}")
        print(f"T {str(tr_val):.<40}{tf_type:.<20}{tf_rel:.<20}\n")
        if (count := count + 1) % 10 == 0:
            input()

# endregion migrate_model


def get_target_id_from_source_id(model, source_id, module=IMPORT):
    """
    Returns id from target using id from source
    Ex, get_target_id_from_source_id('product.attribute', 3422)
    Returns: False if record cannot be found
    """
    xmlid = f"{module}.{model.replace('.', '_')}_{source_id}"
    return get_res_id(xmlid)


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
        print(gf(f"Recordset('{model}', {record_list}) unlinked"))
        return

    finally:
        option = input('Unlinking failed, unlink one record at a time? [y/N]')
        if option.lower() != 'n' or option != '':
            try:
                [target.env[model].unlink(x) for x in record_list]
            except Exception as e:
                print(e)


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
    input(gf("Press ENTER key to continue"))
    print('target')
    for key in sorted(target_fields):
        if target_fields[key].get('relation', None):
            relation = target_fields[key]['relation']
            key_type = target_fields[key]['type']
            text = 'relation: {:<30} type: {:<10} key: {:<30}'
            print(text.format(relation, key_type, key))
    input(gf(f"The end"))


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
            print(f"INFO: Replacing href")
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
            print(f"INFO: Replacing src {tag.attrs[src]} with {new_value}")
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
            print(gf(f"Replacing t-value "
                     f"{tag.attrs[t]} with "
                     f"{new_value}"))
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
            print(gf(f"Replacing classes "
                     f"{old_list} with "
                     f"{new_list}"))
            tag.attrs['class'] = new_list
        else:
            print(f"{old_list}")

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
                  f"{tag.attrs[s]} with "
                  f"{new_styles}")
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
            print(gf(f"Created new [{model}] and external id from source "
                     f" id [{source_read['id']}] [{source_read[name]}]"))
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

    print(gf(f"DONE!"))


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
            print(f"{key}, {sr[key]}")
        except:
            print(f"key error ({key}")

        space = ' '*(len(str(count))+len(key)+1)
        try:
            print(space, tr[key])
        except:
            print(f"key error ({key})")
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


print(gf(f"functions loaded"))

# region ACCOUNT PAYMENT depends on
# account.account
# account.journal
# account.payment.term
# account.tax
# product.product

# CREATE ACCOUNT PAYMENT ======================================================
migrate_model(
    model='account.payment',
    mapping=dict(
        amount='',
        company_id='',
        currency_id='',
        date='payment_date',
        journal_id='',
        name='',
        partner_id='',
        payment_reference='',
        payment_type='',
        ref='communication',
    ),
)
# UPDATE ACCOUNT PAYMENT ======================================================
migrate_model(
    model='account.payment',
    mapping=dict(
        state='',
    ),
)


# region ACCOUNT ACCOUNT

map_existing_records('account.journal', source_field='code')

# CREATE ======================================================================
migrate_model(
    model='account.account',
    mapping=dict(
        code='',
        name='',
        reconcile='',
        user_type_id='',
    ),
)
# endregion ACCOUNT ACCOUNT

print_xmlids(source, 'account.account.type')
print_xmlids(target, 'account.account.type')


products = source.env['product.product'].search_read(
    [('type', '=', 'product')], ['qty_available'], order='id')

for product in products:
    xmlid = get_xmlid('product.product', product['id'])
    if (res_id := get_res_id_from_conn(target, xmlid=xmlid)):
        read = target.env['product.product'].read(res_id, ['product_tmpl_id'])
        if product['qty_available'] >= 0:
            change_id = target.env['stock.change.product.qty'].create(dict(
                new_quantity=round(product['qty_available'], 2),
                product_id=read[0]['id'],
                product_tmpl_id=read[0]['product_tmpl_id'][0],
            ))
            target.env['stock.change.product.qty'].browse(
                change_id).change_product_qty()
        else:
            print(product)
    else:
        raise Exception('target_product not found')


# region STOCK QUANT
# CREATE ======================================================================
migrate_model(
    model='stock.quant',
    mapping=dict(
        in_date='',
        location_id='',
        owner_id='',
        product_id='',
        quantity='qty',
    ),
)
# endregion STOCK QUANT

account_types = source.env['account.account.type'].search_read([], ['name'])
for account_type in account_types:
    xmlid = source.env['account.account.type'].get_metadata(account_type['id'])[
        0]['xmlid']
    user_type_id = account_type['id']
    print(gf(f"{user_type_id:02} {account_type['name']:30} {xmlid}"))
    accounts = source.env['account.account'].search_read(
        [('user_type_id', '=', user_type_id)], ['code', 'name', 'reconcile'], order='id')

    target_user_type_id = get_res_id_from_conn(target, xmlid=xmlid)
    target_accounts = target.env['account.account'].search_read(
        [('user_type_id', '=', target_user_type_id)], ['code', 'name', 'reconcile'], order='id')

    for account in accounts:
        print(
            yf(f"{account['id']:02} {account['code']} {account['reconcile']} {account['name']}"))
    for account in target_accounts:
        print(
            rf(f"{account['id']:02} {account['code']} {account['reconcile']} {account['name']}"))
    input('Next')

accounts = source.env['account.account'].search_read([], order='id')
accounts_map = {}
for account in accounts:
    code = account['code']
    name = account['name']
    if (accounts_in_target := target.env['account.account'].search_read([('code', '=', code)], ['code', 'name'])):
        if len(accounts_in_target) == 1:
            accounts_map.update({account['id']: accounts_in_target[0]['id']})
        else:
            print(yb('Too many matches'), yf(
                f"{code}, {name}, {accounts_in_target}"))
    else:
        print(rb('No match found'), rf(f"{code}, {name}"))
accounts_map

# MAP RECORDS =================================================================
map_records_manually(
    source_model='product.uom',
    target_model='uom.uom',
    source_field='name',
    mapping=uom_mapping
)

# region ACCOUNT ACCOUNT
# DELETE ACCOUNT ACCOUNT ======================================================
target.env['account.account'].unlink(target.env['account.account'].search([]))

# CREATE ACCOUNT ACCOUNT ======================================================
migrate_model(
    model='account.account',
    mapping=dict(
        code='',
        name='',
        reconcile='',
        user_type_id='',
    ),
)

# endregion ACCOUNT ACCOUNT

# property_stock_account_output_categ_id
# account.account,5, '110300 Stock Interim (Delivered)'
# property_stock_account_input_categ_id
# account.account,4 '110200 Stock Interim (Received)'
# account.account,5 '101120 Stock Interim Account (Received)'
# property_account_receivable_id
# account.account,6 '121000 Account Receivable'
# property_account_payable_id
# account.account,14 '211000 Account Payable'
# property_account_expense_categ_id
# account.account,26 '600000 Expenses'
# property_account_income_categ_id
# account.account,21 '400000 Product Sales'
# property_tax_payable_account_id
# account.account,17 '252000 Tax Payable'
# property_tax_receivable_account_id
# account.account,9 '132000 Tax Receivable'
# property_stock_valuation_account_id
# account.account,3 '110100 Stock Valuation'


target_accounts = target.env['account.account'].search([])
target_properties = target.env['ir.property'].search_read(
    [('company_id', '=', 1), ('value_reference', 'like', 'account.account')], ['name', 'value_reference'])
for target_account in target_accounts:
    for i, target_property in enumerate(target_properties):
        if str(target_account) == target_property['value_reference'].split(',')[-1]:
            print(target_property['name'])


source.env['ir.property'].search_read(
    [('value_reference', 'like', 'account.account')], ['name', 'value_reference'])

target.env['ir.property'].search_read(
    [('value_reference', 'like', 'account.account')], ['name', 'value_reference'])

target_ir_properties = target.env['ir.property'].search_read(
    [('value_reference', 'like', 'account.account')], ['name', 'value_reference'])
for target_ir_property in target_ir_properties:
    value_reference = int(target_ir_property['value_reference'].split(',')[-1])
    if value_reference in target_accounts:
        target_accounts.remove(value_reference)
print(target_accounts)


def account_rel(field):
    return field[1]['type'] == 'many2one' and field[1]['relation'] == 'account.account'


source_journal_fields = source.env['account.journal'].fields_get().items()
target_journal_fields = target.env['account.journal'].fields_get().items()

source_journals = source.env['account.journal'].search_read(
    [], ['code'] + sorted(x for x, y in filter(account_rel, source_journal_fields)))

target_journals = target.env['account.journal'].search_read(
    [], ['code'] + sorted(x for x, y in filter(account_rel, target_journal_fields)))
# CREATE STOCK LOCATION ROUTE =================================================