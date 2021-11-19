import odoorpc
import openpyxl
import sys
import getopt
from mapping import MAPS
from pathlib import Path
from pprint import pprint as pp
from datetime import datetime
from datetime import timedelta
import pytz

IMPORT = '__import__'


def main(argv):
    input_file = ''
    mode = 'debug'
    try:
        opts, args = getopt.getopt(argv, "dhi:s")
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-d':
            mode = 'debug'
        elif opt == '-h':
            help()
            sys.exit()
        elif opt in ("-i"):
            input_file = arg
        if opt == '-s':
            mode = 'sync'
    print('\nLoading workbook . . . ', end=' ')
    xlsx_file = Path(input_file)
    try:
        wb = openpyxl.load_workbook(xlsx_file, data_only=True)
    except Exception as e:
        print(e.message)
    else:
        file_name = input_file.split('/')[-1]
        print('Ok!\nLoading worksheet . . .', end=' ')
        sheet = wb.active
        print('Ok!')
        migrate_from_sheet(file_name, sheet, mode)
    finally:
        print('Terminating program. . .')


def help():
    print(f"{sys.argv[0].split('/')[-1]} -i <inputfile> -d //for debugging")
    print(f"{sys.argv[0].split('/')[-1]} -i <inputfile> -s //for syncing")


def migrate_from_sheet(file_name, sheet, mode):
    errors = []
    cols = [col.value for col in sheet[1]]
    maps = MAPS.get(file_name)
    external_identifier = maps.get('external_identifier')
    model = maps.get('model')
    for row in sheet.iter_rows(min_row=2):
        vals = vals_builder(row, cols, maps.get('fields'))
        xmlid = get_xmlid(external_identifier, row[0].value)
        exec(maps.get('before', ''))
        try:
            if 'skip' in vals:
                pass
            else:
                if mode == 'debug':
                    print(f"{vals=}")
                    print(f"{xmlid=}")
                elif mode == 'sync':
                    create_record_and_xmlid_or_update(model, vals, xmlid)
                exec(maps.get('after', ''))
                input() if mode == 'debug' else None
        except Exception as e:
            print(
                {'e': e, 'row': [r.value for r in row], 'vals': vals, 'xmlid': xmlid})
            errors.append(
                {'e': e, 'row': [r.value for r in row], 'vals': vals, 'xmlid': xmlid})
    print(errors)


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


def get_xmlid(identifier, ext_id):
    """Return xmlid from model and ext_id."""
    return f"{IMPORT}.{identifier.replace('.', '_')}_{ext_id}"


def get_res_id(xmlid):
    """Return res_id from xmlid if found."""
    return target.env['ir.model.data'].xmlid_to_res_id(xmlid)


def create_xmlid(model, res_id, xmlid):
    """Create xmlid for a record."""
    vals = {'model': model,
            'module': xmlid.split('.')[0],
            'name': xmlid.split('.')[1],
            'res_id': res_id,
            }
    target.env['ir.model.data'].create(vals)


if __name__ == "__main__":
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
    print(target.env)
    main(sys.argv[1:])
