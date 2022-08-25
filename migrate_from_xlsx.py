# -*- coding: utf-8 -*-

import argparse
import odoorpc


def main(args, self):
    path = args.input
    mode = []
    if args.debug:
        mode.append('debug')
    if args.sync:
        mode.append('sync')
    count = args.count or 0
    start = args.first_row or 0
    end = args.last_row or 0
    migrate_from_sheet(self, path, mode, count, start, end)


def migrate_from_sheet(self, path, mode, count=0, start=0, end=0):
    from datetime import datetime
    from datetime import timedelta
    from pathlib import Path

    import base64
    import mapping
    import openpyxl
    import pytz

    IMPORT = '__import__'

    path_to_file = Path(path)
    file_name = path_to_file.stem
    count = count or int(
        self.env['ir.config_parameter'].get_param('/migration/count', '0'))
    start = start or int(self.env['ir.config_parameter'].get_param(path, '0'))
    start = 2 if start == 1 else start
    if start > 0:
        print(
            f"Initializing migration: {path=}, {mode=}, {count=}, "
            f"{start=}, {end=}")
    else:
        return

    def compare_values(record, model_fields, vals):
        for key in list(vals):
            field_type = model_fields.get(key).get('type')
            if debug:
                input(f"{key=}, {field_type=}")
                input(f"{record[key]=}")
                input(f"  {vals[key]=}")
            value = record[key]
            if field_type in ['many2one']:
                if type(value) is list and len(value) == 2:
                    value = value[0]
            elif field_type in ['one2many', 'many2many']:
                if type(vals[key]) is list:
                    for command in vals[key]:
                        if type(command) is list or tuple:
                            if command[0] == 4 and command[1] in value:
                                vals.pop(key)
                    continue
            if value == vals[key]:
                vals.pop(key)
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
                self.env[model].write(res_id, vals)
                print(f"write: {model=}, {vals=}, {res_id=}, {xmlid=})")
        elif sync and not debug:
            res_id = self.env[model].create(vals)
            create_xmlid(model, res_id, xmlid)
            model_ids[xmlid] = res_id
            print(f"create: {model=}, {vals=}, {res_id=}, {xmlid=})")
        if vals:
            params['counter'] += 1

        print_info('debug') if debug else None
        return res_id

    def create_xmlid(model, res_id, xmlid):
        module = xmlid.split('.')[0]
        vals = {'model': model,
                'module': module,
                'name': xmlid.split('.')[1],
                'res_id': res_id}
        if module != IMPORT:
            vals['noupdate'] = True
        self.env['ir.model.data'].create(vals)

    def get_fields(model):
        model_fields = f"{model.replace('.', '_')}_fields_get"
        if model_fields not in params:
            params[model_fields] = self.env[model].fields_get()
            print(f"Added '{model_fields}'")
        return params[model_fields]

    def get_ids(model):
        model_ids = f"{model.replace('.', '_')}_ids"
        if model_ids not in params:
            params[model_ids] = {x['complete_name']: x['res_id'] for x in self.env['ir.model.data'].search_read(
                [('model', '=', model)])}
            print(f"Added '{model_ids}'")
        return params[model_ids]

    def get_reads(model, field_list):
        model_reads = f"{model.replace('.', '_')}_reads"
        if model_reads not in params:
            model_ids = get_ids(model)
            params[model_reads] = {rec['id']: {key: rec[key] for key in field_list} for rec in self.env[model].read([model_ids[id] for id in model_ids], field_list)}
            print(f"Added '{model_reads}'")
        return params[model_reads]

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

    def get_res_id_from_xmlid(xmlid):
        return self.env['ir.model.data'].xmlid_to_res_id(xmlid)

    def get_search_read(model, key, domain=[]):
        search_read = f"{model.replace('.', '_')}_search_read"
        if search_read not in params:
            params[search_read] = {x[key]: x['id']
                                   for x in self.env[model].search_read(domain, [key])}
            print(f"Added '{search_read}'")
        return params[search_read]

    def get_xmlid(name, ext_id):
        return f"{IMPORT}.{name.replace('.', '_')}_{ext_id}"

    def vals_builder(row, cols, fields):
        vals = {}
        for key in fields:
            if fields[key] in cols:
                i = cols.index(fields[key])
                vals[key] = row[i].value
        return vals

    debug = 'debug' in mode
    sync = 'sync' in mode
    sheet = openpyxl.load_workbook(path_to_file, data_only=True).active
    cols = [col.value for col in sheet[1]]

    params = getattr(mapping, file_name)
    model = params.get('model')
    fields = params.get('fields')
    before = params.get('before', '')
    after = params.get('after', '')
    params['counter'] = 0
    for row in sheet.iter_rows(min_row=start or 2, max_row=end or None):
        vals = vals_builder(row, cols, fields)
        xmlid = get_xmlid(cols[0], row[0].value)
        row_number = row[0].row
        if row_number % 10000 == 0:
            print(f"{row_number=}")
        try:
            exec(before)
            create_record_and_xmlid_or_update(model, vals, xmlid)
            exec(after)

        except Exception as e:
            print(f"{e=}")
            print(f"{[r.value for r in row]=}")
            print(f"{vals=}")
            print(f"{xmlid=}")
            params['counter'] = 1
            break

        else:
            if count and params['counter'] >= count:
                break

        input() if 'debug' in mode and 'sync' not in mode else None

    print(f"{path=}, {row_number=}, {params['counter']=}")
    self.env['ir.config_parameter'].set_param(
        path, str(row_number) if params['counter'] else '-1')


if __name__ == '__main__':
    try:
        self = odoorpc.ODOO().load('self')
    except Exception as e:
        print(e)
    else:
        self.env.context.update({
            'mail_create_nolog': True,
            'mail_create_nosubscribe': True,
            'mail_notrack': True,
            'tracking_disable': True,
            'tz': 'UTC',
        })

    for server in ['ir.mail_server', 'fetchmail.server']:
        if self.env[server].search([]):
            raise Warning(f"Active {server}")

    self.env.context.update({'active_test': False})
    parser = argparse.ArgumentParser(
        description=(
            "This script will read xlsx-files and create records using "
            "odoorpc, map columns with fields in mapping.py or it won't work"))
    parser.add_argument(
        '-c', '--count', help='Count', type=int)
    parser.add_argument(
        '-d', '--debug', action='store_true', help='debug mode')
    parser.add_argument(
        '-f', '--first_row', help='First row', type=int)
    parser.add_argument(
        '-i', '--input', help='path to xlsx-file', required=True)
    parser.add_argument(
        '-l', '--last_row', help='Last row', type=int)
    parser.add_argument(
        '-s', '--sync', action='store_true', help='sync mode')
    args = parser.parse_args()
    print(self.env)
    main(args, self)
