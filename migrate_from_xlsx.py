import sys
import odoorpc
import openpyxl
from pathlib import Path
from mapping import MAPS
from pprint import pprint as pp

IMPORT = '__import__'


def main(file_path, model):
    mode = input('Mode? [Create, Write, Debug] ')
    print('Loading workbook . . . ', end=' ')
    xlsx_file = Path(file_path)
    wb = openpyxl.load_workbook(xlsx_file)
    print('Ok!\nLoading worksheet . . .', end=' ')
    ws = wb.active
    run = input('Ok!\nRun script? [yN] ').lower()
    if run == 'y':
        cols = [col.value for col in ws[1]]
        migrate_from_sheet(model, cols, ws, mode=mode)
    print('Terminating program. . .')


def migrate_from_sheet(model, cols, ws, **kwargs):
    """Create/update records from xlsx sheet"""
    mode = kwargs.get('mode', 'debug')
    maps = MAPS.get(model)
    count = 0
    for row in ws.iter_rows(min_row=2):
        vals = vals_builder(row, cols, maps)
        xml_id = set_xml_id(model, vals.pop('ext_id'))
        while True:
            try:
                if mode == 'create':
                    create_record_and_xmlid(model, vals, xml_id)
                elif mode == 'write':
                    write_record(model, vals, xml_id)
                elif mode == 'debug':
                    if count == 0:
                        pp(cols)
                    pp(f"{xml_id}, {vals}")
                    input()
                    count += 1
            except:
                input('Continue? Press enter')
            else:
                break

def vals_builder(row, cols, maps):
    vals = {}
    for key in maps:
        if maps[key] in cols:
            i = cols.index(maps[key])
            vals.update({key: row[i].value})
    calc= maps.get('calc')
    if calc:
        for key in calc.keys():
            exec(calc[key])
        
    return vals


def create_record_and_xmlid(model, vals, xml_id):
    """Create record if it doesn't exist, return res_id."""
    res_id = get_res_id_from_xml_id(xml_id)
    if res_id:
        print(f"Skipping creation {xml_id} already exist")
    else:
        try:
            res_id = target.env[model].create(vals)
            create_xml_id(model, res_id, xml_id)
        except Exception as e:
            print('CREATE_RECORD: FAIL! Read the log...', e, vals)
        else:
            print("CREATE_RECORD: SUCCESS!")
            return res_id


def write_record(model, vals, xml_id):
    """Create record if it doesn't exist, return res_id."""
    res_id = get_res_id_from_xml_id(xml_id)
    if not res_id:
        print(f"Skipping write {xml_id} does not exist")
    else:
        try:
            target.env[model].write(res_id, vals)
        except Exception as e:
            print('WRITE_RECORD: FAIL! Read the log...', e, res_id, vals)
        else:
            print('WRITE_RECORD: SUCCESS!')
            return res_id


def set_xml_id(model, ext_id):
    """Return xml_id from model and ext_id."""
    return f"{IMPORT}.{model.replace('.', '_')}_{ext_id}"


def get_res_id_from_xml_id(xml_id):
    """Return res_id from xml_id if found."""
    return target.env['ir.model.data'].xmlid_to_res_id(xml_id)


def create_xml_id(model, res_id, xml_id):
    """Create xml_id for a record."""
    vals = {'model': model,
            'module': xml_id.split('.')[0],
            'name': xml_id.split('.')[1],
            'res_id': res_id,
            }
    target.env['ir.model.data'].create(vals)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            f"\nUsage: python3 {sys.argv[0]} /path/of/file.xslx res.partner\n")
        raise SyntaxError("Wrong number of argument.")

    try:
        target = odoorpc.ODOO().load('target')
    except Exception as e:
        print(e)

    print(target.env)
    main(sys.argv[1], sys.argv[2])
