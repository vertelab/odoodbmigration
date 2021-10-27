import odoorpc
import openpyxl
import sys
from mapping import MAPS
from pathlib import Path
from pprint import pprint as pp

IMPORT = '__import__'


def main(file_path):
    modes = ['create', 'debug', 'write']
    while True:
        mode = input(f"Mode? {modes} ").lower()
        if mode in modes:
            break
        else:
            print('Wrong mode')
    print('\nLoading workbook . . . ', end=' ')
    xlsx_file = Path(file_path)
    wb = openpyxl.load_workbook(xlsx_file)
    print('Ok!\nLoading worksheet . . .', end=' ')
    ws = wb.active
    run = input('Ok!\nRun script? [yN] ').lower()
    if run == 'y':
        cols = [col.value for col in ws[1]]
        migrate_from_sheet(cols=cols, sheet=ws, mode=mode)
    print('Terminating program. . .')


def migrate_from_sheet(**kwargs):
    """Create/update records from xlsx sheet"""
    count = 0
    errors = []
    cols = kwargs.get('cols')
    mode = kwargs.get('mode')
    sheet = kwargs.get('sheet')

    ext_model = cols[0]
    maps = MAPS.get(cols[0])
    model = maps.get('model')

    for row in sheet.iter_rows(min_row=2):
        vals = vals_builder(row, cols, maps, mode)
        xml_id = get_xml_id(ext_model, row[0].value)
        while True:
            try:
                if mode == 'create':
                    create_record_and_xmlid(model, vals, xml_id)
                elif mode == 'write':
                    write_record(model, vals, xml_id)
                elif mode == 'debug':
                    if count == 0:
                        pp(cols)
                    pp(vals)
                    pp(xml_id)
                    input()
                    count += 1
            except Exception as e:
                errors.append(
                    {'e': e, 'row': [r.value for r in row], 'vals': vals, 'xml_id': xml_id})
            else:
                break
    print(errors)


def vals_builder(row, cols, maps, mode):
    calc = maps.get('calc')
    maps = maps.get(mode)
    vals = {}
    for key in maps:
        if maps[key] in cols:
            i = cols.index(maps[key])
            vals[key] = row[i].value
    if calc:
        for key in calc.keys():
            if vals.get(key):
                exec(calc[key])

    return vals


def create_record_and_xmlid(model, vals, xml_id):
    """Create record if it doesn't exist, return res_id."""
    res_id = get_res_id_from_xml_id(xml_id)
    if res_id:
        print(f"Skipping creation {xml_id} already exist")
    else:
        res_id = target.env[model].create(vals)
        create_xml_id(model, res_id, xml_id)
        print("CREATE_RECORD: SUCCESS!", res_id, xml_id)
        return res_id


def write_record(model, vals, xml_id):
    """Create record if it doesn't exist, return res_id."""
    res_id = get_res_id_from_xml_id(xml_id)
    if not res_id:
        print(f"Skipping write {xml_id} does not exist")
    else:
        target.env[model].write(res_id, vals)
        print('WRITE_RECORD: SUCCESS!', res_id, xml_id)
        return res_id


def get_xml_id(model, ext_id):
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
    if len(sys.argv) != 2:
        print(
            f"\nUsage: python3 {sys.argv[0]} /path/of/file.xslx\n")
        raise SyntaxError("Wrong number of argument.")

    try:
        target = odoorpc.ODOO().load('target')
    except Exception as e:
        print(e)

    print(target.env)
    main(sys.argv[1])
