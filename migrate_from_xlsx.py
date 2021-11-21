import mapping
import odoorpc
import pytz
import argparse
from datetime import datetime
from datetime import timedelta
from pathlib import Path


IMPORT = '__import__'


def main(args):
    first_row = args.first_row or 1
    mode = 'sync' if args.sync else 'debug'
    path_to_file = args.input
    migrate_from_sheet(path_to_file, mode, first_row)
    

def migrate_from_sheet(path_to_file, mode, first_row=1):
    file_name = file_name_without_extension(path_to_file)
    params = getattr(mapping, file_name)

    sheet = load_worksheet(path_to_file)
    cols = [col.value for col in sheet[1]]

    model = params.get('model')
    fields = params.get('fields')
    before = params.get('before', '')
    after = params.get('after', '')

    for row in sheet.iter_rows(min_row=first_row+1):
        vals = vals_builder(row, cols, fields)
        xmlid = get_xmlid(file_name, row[0].value)
        
        try:
            exec(before)
            if mode == 'debug' or 'skip' in vals:
                print(f"{vals=}")
                print(f"{xmlid=}")
            elif mode == 'sync':
                    create_record_and_xmlid_or_update(model, vals, xmlid)
            exec(after)

        except Exception as e:
            print({'e': e, 'row': [r.value for r in row], 'vals': vals, 'xmlid': xmlid})
            break

        input() if mode == 'debug' else None


def file_name_without_extension(file_name):
    return Path(file_name).stem


def load_worksheet(path_to_file):
    import openpyxl

    print('\nLoading workbook . . . ', end=' ')
    xlsx_file = Path(path_to_file)
    try:
        workbook = openpyxl.load_workbook(xlsx_file, data_only=True)
        print('Loaded!\n')
        print('Loading worksheet . . .', end=' ')
        worksheet = workbook.active
        print('Loaded!\n')
    except Exception as e:
        print(e.message)
    else:
        return worksheet


def vals_builder(row, cols, fields):
    vals = {}
    for key in fields:
        if fields[key] in cols:
            i = cols.index(fields[key])
            vals[key] = row[i].value
    return vals


def create_record_and_xmlid_or_update(model, vals, xmlid):
    res_id = get_res_id(xmlid)
    if res_id:
        target.env[model].write(res_id, vals)
        print('WRITE_RECORD: SUCCESS!', res_id, xmlid, vals)
    else:
        res_id = target.env[model].create(vals)
        create_xmlid(model, res_id, xmlid)
        print("CREATE_RECORD: SUCCESS!", res_id, xmlid, vals)
    return res_id


def get_xmlid(identifier, ext_id):
    return f"{IMPORT}.{identifier.replace('.', '_')}_{ext_id}"


def get_res_id(xmlid):
    return target.env['ir.model.data'].xmlid_to_res_id(xmlid)


def create_xmlid(model, res_id, xmlid):
    vals = {'model': model,
            'module': xmlid.split('.')[0],
            'name': xmlid.split('.')[1],
            'res_id': res_id}
    target.env['ir.model.data'].create(vals)


if __name__ == '__main__':
    try:
        target = odoorpc.ODOO().load('target')
    except Exception as e:
        print(e)
    target.env.context.update({
        'mail_create_nosubscribe': True,
        'mail_create_nolog': True,
        'mail_notrack': True,
        'tracking_disable': True,
        'tz': 'UTC',
    })
    parser = argparse.ArgumentParser(description=
        "This script will read xlsx-files and create records using odoorpc, "
        "map columns with fields in mapping.py or it won't work")
    parser.add_argument(
        '-i', '--input', help='path to xlsx-file', required=True)
    parser.add_argument(
        '-f', '--first_row', help='first row', type=int)
    parser.add_argument(
        '-s', '--sync', action='store_true', help='sync mode')
    args = parser.parse_args()   
    print(target.env)
    main(args)
