import odoorpc
import openpyxl
import sys
from mapping import MAPS
from pathlib import Path
from pprint import pprint as pp
from datetime import datetime
from datetime import timedelta
import pytz

IMPORT = '__import__'


def main(file_path, col):
    modes = ['debug', 'sync']
    while True:
        mode = input(f"Mode? {modes} ").lower()
        if mode in modes:
            break
        else:
            print('Wrong mode')
    print('\nLoading workbook . . . ', end=' ')
    xlsx_file = Path(file_path)
    wb = openpyxl.load_workbook(xlsx_file, data_only=True)
    print('Ok!\nLoading worksheet . . .', end=' ')
    ws = wb.active
    run = input('Ok!\nRun script? [yN] ').lower()
    if run == 'y':
        cols = [col.value for col in ws[1]]
        migrate_from_sheet(col=col, cols=cols, sheet=ws, mode=mode)
    print('Terminating program. . .')


def migrate_from_sheet(**kwargs):
    """Create/update records from xlsx sheet"""
    count = 0
    errors = []
    col = kwargs.get('col')
    cols = kwargs.get('cols')
    mode = kwargs.get('mode')
    sheet = kwargs.get('sheet')

    ext_model = cols[int(col) if col else 0].replace('.', '_')
    maps = MAPS.get(ext_model)
    model = maps.get('model')
    for row in sheet.iter_rows(min_row=2):
        vals = vals_builder(row, cols, maps.get('fields'))
        xmlid = get_xmlid(ext_model, row[0].value)
        exec(maps.get('pre_sync', ''))
        while True:
            try:
                if 'skip' in vals:
                    pass
                else:
                    if mode == 'debug':
                        if count == 0:
                            pp(cols)
                        print(f"{vals=}")
                        print(f"{xmlid=}")
                        count += 1
                    elif mode == 'sync':
                        if not create_record_and_xmlid(model, vals, xmlid):
                            write_record(model, vals, xmlid)
                    exec(maps.get('post_sync', ''))
                    input() if mode == 'debug' else None
            except Exception as e:
                print({'e': e, 'row': [r.value for r in row], 'vals': vals, 'xmlid': xmlid})
                errors.append(
                    {'e': e, 'row': [r.value for r in row], 'vals': vals, 'xmlid': xmlid})
            else:
                break
    print(errors)


def vals_builder(row, cols, fields):
    vals = {}
    for key in fields:
        if fields[key] in cols:
            i = cols.index(fields[key])
            vals[key] = row[i].value
    return vals


def create_record_and_xmlid(model, vals, xmlid):
    """Create record if it doesn't exist, return res_id."""
    res_id = get_res_id_from_xmlid(xmlid)
    if res_id:
        print(f"Skipping creation {xmlid} already exist")
        return 0
    else:
        res_id = target.env[model].create(vals)
        create_xmlid(model, res_id, xmlid)
        print("CREATE_RECORD: SUCCESS!", res_id, xmlid, vals)
        return res_id


def write_record(model, vals, xmlid):
    """Write record if it exist, return res_id."""
    res_id = get_res_id_from_xmlid(xmlid)
    if not res_id:
        print(f"Skipping write {xmlid} does not exist")
        return 0
    else:
        target.env[model].write(res_id, vals)
        print('WRITE_RECORD: SUCCESS!', res_id, xmlid, vals)
        return res_id


def get_xmlid(model, ext_id):
    """Return xmlid from model and ext_id."""
    return f"{IMPORT}.{model.replace('.', '_')}_{ext_id}"


def get_res_id_from_xmlid(xmlid):
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
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 0)
