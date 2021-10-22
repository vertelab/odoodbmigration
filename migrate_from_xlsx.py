import sys
import odoorpc
import openpyxl
from pathlib import Path
from mapping import MAPS


IMPORT = '__import__'


def main(model, file_path):
    mode = input('Mode? C=Create, W=Write')
    if mode.lower() in ['c','w']:
        xlsx_file = Path(file_path)
        wb = openpyxl.load_workbook(xlsx_file)
        ws = wb.active
        cols = [col.value for col in ws[1]]
        if mode.lower() == 'c':
            create_from_sheet(model, cols, ws)
        elif mode.lower() == 'w':
            write_from_sheet(model, cols, ws)
        wb.close()
    else:
        print('Terminating program. . .')

def create_from_sheet(model, cols, ws):
    """Create records from xlsx file"""
    maps = MAPS.get(model)
    print(cols)
    my_list = []
    count = 0
    for row in ws.iter_rows(min_row=2):
        vals = {}
        my_list.append(row[27].value)
        for key in maps:
            if maps[key] in cols:
                i = cols.index(maps[key])
                vals.update({key: row[i].value})
        #create_record_and_xmlid(model, vals, vals.pop('ext_id'))
        # if count == 2000:
        #     break
        # count += 1
    print(set(my_list))
    
def write_from_sheet(model, cols, ws):
    """Write records from xlsx file"""
    m = map.get(model)
    print(cols)
    my_list = []
    count = 0
    for row in ws.iter_rows(min_row=2):
        vals = {}
        my_list.append(row[27].value)
        for key in m:
            if m[key] in cols:
                i = cols.index(m[key])
                vals.update({key: row[i].value})
        #create_record_and_xmlid(model, vals, vals.pop('ext_id'))
        # if count == 2000:
        #     break
        # count += 1
    print(set(my_list))


def create_record_and_xmlid(model, vals, ext_id):
    """Create record if it doesn't exist, return res_id."""
    xml_id = set_xml_id(model, ext_id)
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


def write_record(model, vals, ext_id):
    """Create record if it doesn't exist, return res_id."""
    xml_id = set_xml_id(model, ext_id)
    res_id = get_res_id_from_xml_id(xml_id)
    if res_id:
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
            f"\nUsage: python3 {sys.argv[0]} res.partner /path/of/file.xslx\n")
        raise SyntaxError("Wrong number of argument.")

    try:
        target = odoorpc.ODOO().load('target')
    except Exception as e:
        print(e)

    print(target.env)
    main(sys.argv[1], sys.argv[2])
