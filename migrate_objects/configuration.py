#!/usr/bin/env python3
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

from odoo import models, fields, api, http, registry
import odoo


import sys
try:
    import odoorpc
except ImportError:
    raise Warning('odoorpc library missing. Please install the library. Eg: pip3 install odoorpc')

from PIL import Image

Image.MAX_IMAGE_PIXELS = 100000000000
print(1)
source = odoorpc.ODOO.load('source')
target = odoorpc.ODOO.load('target')

# ~ dirty is loaded for manual testing purposes
dirty = odoorpc.ODOO.load('dirty')

del source.env.context['lang']
target.env.context['lang'] = 'en_US'
target.env.context['active_test'] = False
source.env.context['active_test'] = False

source_se = odoorpc.ODOO.load('source')
target_se = odoorpc.ODOO.load('target')
source.env.context['lang'] = 'sv_SE'
target.env.context['lang'] = 'sv_SE'
target.env.context['active_test'] = False
source.env.context['active_test'] = False
print(2)
# HELPER FUNCTIONS
IMPORT_MODULE_STRING = '__import__'

                # ~ if 'in_group_' in key:
                    # ~ print("start_ingroup")
                    # ~ s_id = re.findall(r'\d+', key)[0]
                    # ~ print(s_id)
                    # ~ t_id = target.env.ref(IMPORT_MODULE_STRING+'.'+'res_groups_'+str(s_id)).res_id
                    
                    # ~ t_id = target.env['ir.model.data'].search_read([
                            # ~ ('model', '=', 'res.groups'),
                            # ~ ('name', '=', f'res_groups_{s_id}')], ['res_id'])[0]['res_id']
                    # ~ print(t_id)
                    # ~ vals.update({'in_group_'+str(t_id): (record[key])})
                    # ~ print("end_ingroup")

# TODO: Skriv en robust funktion för detta. ID beror på databasen. Denna
#  metod fungerar bara för exakt den databas som listan togs fram för.
COMPANY_ID = 1

UNITS_OF_MEASURE_EXID = {
    5: 'product_uom_cl',
    23: 'product_uom_cm',
    11: 'product_uom_day',
    4: 'product_uom_dl',
    21: 'product_uom_dozen',
    30: 'product_uom_floz',
    28: 'product_uom_foot',
    17: 'product_uom_gram',
    32: 'product_uom_gal',
    37: 'product_uom_gram',
    36: 'product_uom_gram',
    10: 'product_uom_hour',
    27: 'product_uom_inch',
    2: 'product_uom_kgm',
    33: 'product_uom_kgm',
    34: 'product_uom_kgm',
    3: 'product_uom_kgm',
    14: 'product_uom_km',
    25: 'product_uom_lb',
    24: 'product_uom_litre',
    13: 'product_uom_meter',
    29: 'product_uom_mile',
    6: 'product_uom_ml',
    26: 'product_uom_oz',
    1: 'product_uom_unit',
    31: 'product_uom_qt',
    35: 'product_uom_unit',
    22: 'product_uom_ton',
    8: 'product_uom_ton'
}

UNITS_OF_MEASURE = {}

account_translation_table_xid = {91: '1_K3_1011_2017', 101: '1_K3_1040_2017', 126: '1_K3_1181_2017', 129: '1_K3_1210_2017', 130: '1_K3_1211_2017', 131: '1_K3_1213_2017', 133: '1_K3_1219_2017', 134: '1_K3_1221_2017', 135: '1_K3_1222_2017', 136: '1_K3_1223_2017', 1300: '1_K3_1221_2017', 138: '1_K3_1229_2017', 145: '1_K3_1241_2017', 147: '1_K3_1243_2017', 148: '1_K3_1244_2017', 153: '1_K3_1249_2017', 155: '1_K3_1251_2017', 158: '1_K3_1259_2017', 160: '1_K3_1269_2017', 162: '1_K3_1281_2017', 202: '1_chart1410', 1527: '?????????????????????????????????????? 1420 Lager av tillsatsmaterialoch förnödenheter', 1528: '1_K3_1450_2017', 203: '1_K3_1419_2017', 1579: '????????????????????????????????????????????????? 1489 kanske?', 226: '1_K3_1489_2017', 229: '1_K3_1511_2017', 1281: '1_K3_1513_2017', 1371: '??????????????????????????????????', 234: '1_K3_1519_2017', 256: '1_K3_1580_2017', 257: '1_K3_1610_2017', 258: '1_K3_1611_2017', 260: '1_K3_1613_2017', 261: '1_K3_1614_2017', 262: '1_K3_1619_2017', 264: '1_chart1630', 276: '1_K3_1684_2017', 277: '1_K3_1685_2017', 1590: 'Avräkning MÅ Group', 281: '1_K3_1710_2017', 289: '1_K3_1790_2017', 300: '1_K3_1911_2017', 303: '1_chart1920', 309: '1_chart1930', 1531: '1_1254', 1540: '?????????????????????????? Verkar skapas av odoo', 312: '1_K3_1940_2017', 1560: '????????????????', 315: '?????????????????? 1950 konton används till bank certifikat 2021', 325: '1_chart1630', 326: '1_K3_2013_2017', 359: '1_K3_2081_2017', 363: '1_K3_2086_2017', 367: '1_K3_2091_2017', 375: '1_K3_2099_2017', 1324: '1_K3_2110_2017', 377: '?????????????????', 378: '??????????????????', 379: '?????????????????', 380: '????????????????', 381: '?????????????????', 386: '?????????????????', 387: '?????????????????', 388: '?????????????????', 389: '?????????????????????', 390: '1_K3_2150_2017', 393: '1_K3_2153_2017', 425: '1_K3_2351_2017 ???', 436: '1_K3_2393_2017', 452: '1_chart2440', 453: '1_K3_2441_2017', 467: '1_K3_2510_2017', 468: '1_K3_2512_2017', 470: '1_K3_2514_2017', 474: '1_K3_2518_2017', 476: '1_chart2611', 479: '1_chart2614', 480: '1_chart2615', 485: '1_chart2621', 502: '1_chart2640', 503: '1_chart2641', 504: '1_chart2642', 505: '1_chart2645', 506: '1_chart2646', 508: '1_chart2648', 509: '1_chart2649', 510: '1_chart2650', 1302: '?????????? Behöver Skapas', 1329: '????????? Behöver Skapas', 1532: '????????? Behöver Skapas', 512: '1_K3_2661_2017', 514: '1_chart2710', 1504: '???????????????????????????? Behöver skapas', 516: '1_K3_2731_2017', 517: '1_K3_2732_2017', 519: '1_K3_2750_2017', 551: '1_K3_2899_2017', 556: '1_K3_2920_2017', 559: '1_K3_2940_2017', 560: '1_K3_2941_2017', 564: '1_K3_2950_2017', 571: '1_K3_2990_2017', 572: '1_K3_2991_2017', 1301: '1_K3_2999_2017', 576: '????????????????????????????', 578: '1_chart3001', 582: '1_K3_3305_2017', 583: '???????????????????', 584: '???????????????????', 586: '1_chart3001', 587: '1_chart3002', 588: '1_chart3003', 590: '1_K3_3105_2017', 591: '???????????????????', 592: '???????????????????', 593: '1_K3_3108_2017', 600: '1_K3_3520_2017', 602: '1_K3_3540_2017', 1521: '??????????????????????????????????????', 1522: '1_K3_3540_2017 ?????????????????? 6062 Inkasso och KFM-avgifter Kanske', 1523: '???????????????????????????? 6062 Inkasso och KFM-avgifter Kanske', 621: '1_K3_3710_2017', 623: '1_K3_3731_2017', 625: '1_chart3740', 1569: '?????????????????????????? skattefri 7331, skattepliktig 7332 vilken bör det vara?', 646: '1_K3_3960_2017', 648: '1_K3_3971_2017', 650: '1_K3_3973_2017', 657: '1_K3_3990_2017', 661: '1_K3_3994_2017', 664: '1_K3_3999_2017', 665: '1_chart4000', 666: '1_K3_4515_2017', 667: '1_K3_4545_2017', 1538: '???????????????????????????', 1359: '1_K3_5710_2017', 1520: '1_K3_4531_2017', 1530: '1_K3_4535_2017', 674: '1_K3_4730_2017', 675: '1_K3_4731_2017', 680: '1_K3_4910_2017', 689: '1_K3_4950_2017', 690: '1_K3_4960_2017 ???????????+', 700: '???????????????', 701: '1_K3_5010_2017', 702: '1_K3_5011_2017', 704: '1_K3_5013_2017', 707: '1_K3_5040_2017', 708: '1_K3_5050_2017', 710: '1_K3_5061_2017', 711: '1_K3_5062_2017', 712: '1_K3_5063_2017', 714: '1_K3_5065_2017', 715: '1_K3_5070_2017', 716: '1_K3_5090_2017', 727: '1_K3_5162_2017', 728: '1_K3_5163_2017', 730: '1_K3_5165_2017', 731: '1_K3_5170_2017', 732: '1_K3_5190_2017', 736: '1_K3_5198_2017', 738: '1_K3_5200_2017', 742: '1_K3_5220_2017', 749: '1_K3_5300_2017', 750: '1_K3_5310_2017', 755: '1_K3_5360_2017', 758: '1_K3_5390_2017', 759: '1_K3_5400_2017', 760: '1_K3_5410_2017', 761: '1_K3_5410_2017', 762: '1_K3_5430_2017', 763: '1_K3_5440_2017', 764: '1_K3_5460_2017', 765: '1_K3_5480_2017', 766: '1_K3_5490_2017', 768: '1_K3_5510_2017', 769: '1_K3_5520_2017', 770: '1_K3_5530_2017', 771: '1_K3_5550_2017', 772: '1_K3_5580_2017', 773: '1_K3_5590_2017', 775: '1_K3_5610_2017', 776: '1_K3_5611_2017', 777: '1_K3_5612_2017', 778: '1_K3_5613_2017', 779: '1_K3_5615_2017', 780: '1_K3_5616_2017', 1577: '?????????????????????????', 781: '1_K3_5619_2017', 783: '????????????????????', 789: '1_K3_5630_2017', 790: '1_K3_5650_2017', 793: '1_K3_5690_2017', 794: '???????????????????????????????????????????????', 795: '1_K3_5710_2017', 796: '1_K3_5720_2017', 797: '1_K3_5730_2017', 798: '1_K3_5790_2017', 799: '1_K3_5800_2017', 800: '1_K3_5810_2017', 801: '1_K3_5820_2017', 803: '1_K3_5831_2017', 804: '1_K3_5832_2017', 805: '1_K3_5890_2017', 806: '1_K3_5900_2017', 807: '1_K3_5910_2017', 810: '1_K3_5940_2017', 812: '1_K3_5960_2017', 814: '1_K3_5980_2017', 815: '1_K3_5990_2017', 817: '1_K3_6010_2017', 819: '1_K3_6030_2017', 820: '1_K3_6040_2017', 821: '1_K3_6050_2017', 823: '1_K3_6060_2017', 825: '1_K3_6062_2017', 828: '1_K3_6069_2017', 830: '1_K3_6071_2017', 831: '1_K3_6072_2017', 833: '1_K3_6090_2017', 834: '1_K3_6100_2017', 835: '1_K3_6110_2017', 836: '1_K3_6150_2017', 838: '1_K3_6210_2017', 839: '1_K3_6211_2017', 840: '1_K3_6212_2017', 844: '1_K3_6230_2017', 845: '1_K3_6250_2017', 847: '1_K3_6310_2017', 848: '1_K3_6320_2017', 854: '1_K3_6351_2017', 855: '1_K3_6352_2017', 1581: '???????????????????????????????+', 859: '1_K3_6370_2017', 864: '1_K3_6420_2017', 871: '1_K3_6500_2017', 874: '1_K3_6530_2017', 875: '1_K3_6540_2017', 876: '1_K3_6550_2017', 877: '1_K3_6560_2017', 878: '1_K3_6570_2017', 1536: 'Avgift iZettle ???????????', 1550: 'Avgift SumUp ???????????', 880: '1_K3_6590_2017', 881: '1_K3_6800_2017', 890: '1_K3_6890_2017', 891: '1_K3_6900_2017', 895: '1_K3_6930_2017', 896: '1_K3_6940_2017', 898: '1_K3_6950_2017', 899: '???????????', 900: '??????????', 901: '????????++', 902: '??????????+', 904: '1_K3_6980_2017', 905: '1_K3_6981_2017', 906: '1_K3_6982_2017', 907: '1_K3_6990_2017', 908: '1_K3_6991_2017', 909: '1_K3_6992_2017', 910: '1_K3_6993_2017', 1323: '??????????????+++', 916: '1_K3_7010_2017', 917: '1_K3_7011_2017', 937: '1_K3_7081_2017', 938: '1_K3_7082_2017', 940: '1_K3_7090_2017', 942: '1_K3_7210_2017', 943: '1_K3_7211_2017', 952: '1_K3_7220_2017', 953: '1_K3_7221_2017', 961: '1_K3_7230_2017', 972: '1_K3_7281_2017', 976: '1_K3_7285_2017', 977: '1_K3_7286_2017', 980: '1_K3_7290_2017', 983: '1_K3_7300_2017', 984: '1_K3_7310_2017', 990: '1_K3_7316_2017', 995: '1_K3_7321_2017', 996: '1_K3_7322_2017', 997: '1_K3_7323_2017', 1000: '1_K3_7331_2017', 1001: '1_K3_7332_2017', 1003: '1_K3_7370_2017', 1007: '1_K3_7383_2017', 1009: '1_K3_7385_2017', 1011: '1_K3_7387_2017', 1013: '1_K3_7389_2017', 1014: '1_K3_7390_2017', 1017: '1_K3_7400_2017', 1018: '1_K3_7410_2017', 1019: '1_K3_7411_2017', 1020: '1_K3_7412_2017', 1326: '???????????????????????????', 1031: '1_K3_7490_2017', 1033: '1_K3_7510_2017 ????????????????????', 1034: '1_K3_7511_2017', 1039: '1_K3_7519_2017', 1049: '1_K3_7533_2017', 1051: '??????????????????????????', 1052: '1_K3_7570_2017', 1054: '1_K3_7581_2017', 1055: '1_K3_7582_2017', 1056: '1_K3_7583_2017', 1570: '1_K3_7623_2017', 1057: '1_K3_7589_2017', 1059: '1_K3_7600_2017', 1060: '1_K3_7610_2017', 1061: '1_K3_7620_2017', 1062: '1_K3_7621_2017', 1064: '1_K3_7623_2017', 1065: '1_K3_7630_2017', 1066: '1_K3_7631_2017', 1067: '1_K3_7632_2017', 1072: '1_K3_7690_2017', 1076: '1_K3_7699_2017', 1099: '1_K3_7831_2017', 1100: '1_K3_7832_2017', 1102: '1_K3_7834_2017', 1105: '1_K3_7839_2017', 1108: '1_K3_7960_2017', 1112: '1_K3_7973_2017', 1175: '1_K3_8311_2017', 1177: '1_K3_8313_2017', 1178: '1_K3_8314_2017', 1195: '1_K3_8390_2017', 1202: '', 1205: '1_K3_8419_2017', 1207: '1_K3_8421_2017', 1208: '1_K3_8422_2017', 1209: '1_K3_8423_2017', 1210: '1_K3_8429_2017', 1211: '1_K3_8430_2017', 1212: '1_K3_8431_2017', 1213: '1_K3_8436_2017', 1228: '1_K3_8811_2017', 1229: '1_K3_8819_2017', 1231: '1_K3_8830_2017', 1232: '1_K3_8850_2017', 1235: '1_K3_8853_2017', 1254: '1_K3_8910_2017', 1258: '1_K3_8980_2017', 1260: '1_chart8999'}

account_translation_table = {}

account_tax_code_to_account_tax_table_xid = {
2:"1_u1",
4:"accounts numbers are used instead for the report",
23:"1_u2",
# ~ 28:"accounts numbers are used instead for the report",
# ~ 29:"accounts numbers are used instead for the report",
30:"1_tffu",
33:"1_u1mi",
36:"1_vteu",
# ~ 37:"accounts numbers are used instead for the report",
# ~ 47:"don't have this line in our report",
# ~ 49:"don't have this line in our report",
# ~ 53:"don't have this line in our report",
# ~ 55:"don't have this line in our report",
66:"1_i",
67:"1_i6",
68:"1_i6",
69:"1_i",
71:"1_u1mbbui"
}

account_tax_code_to_account_tax_table = {}

account_tax_table_xid = {
2:"1_mp1",
40:"1_i6",
34:"1_i",
36:"1_i",
37:"1_i",
11:"1_mp2",
33:"1_mbbui1",
31:"1_i6",
956:"1_vteu",
970:"1_tfeu",
6:"1_vfeu",
49:"1_mbbui3",
966:"1_e",
47:"1_i6",
39:"1_i12"

}
account_tax_table = {}




''' Glossary
       domain = list of search criterias
           id = number
        model = ex. 'res.partner'
record_fields = what you get from source.env[model].read(record.id, fields)
  record_list = what you get from source.env[model].search([])
      records = what you get from source.env[model].browse(record_list)
       record = what you get from source.env[model].browse(record_list[index])
       source = source database
       target = target database
'''
print(3)
# delete all records in model, e.x. unlink('product.template')

def find_fields_in_core(model, modules, database):
    '''
    '''
    ids = database.env["ir.model.fields"].search([["model","=",model]])
    #print(ids)
    rs = database.env["ir.model.fields"].browse(ids)
    #print(rs)
    fields_in_modules = []
    for r in rs:
        #print(f"{r.name}")
        print(f"Model:{model} Field: {r.name} Module: {r.modules}")
        if r.modules in modules or modules == []:
            fields_in_modules.append(r.name)
    return fields_in_modules

def find_fields_in_database(model, database):
    '''
    '''
    ids = database.env["ir.model.fields"].search([["model","=",model]])
    rs = database.env["ir.model.fields"].browse(ids)
    fields = []
    for r in rs:
        fields.append(r.name)
    return fields

def non_matching_keys(a, b):
    return([key for key in a if key not in b])


def unlink(model, only_migrated=True):
    ''' unlinks all records of a model in target database
    example: unlink('res.partner')
    '''
    record_list = []
    if only_migrated:
        domain = [('module', '=', IMPORT_MODULE_STRING), ('model', '=', model)]
        model_data_record_list = target.env['ir.model.data'].search(domain)
        model_data_records = target.env['ir.model.data'].browse(
            model_data_record_list)
        for record in model_data_records:
            record_list.append(record.res_id)
    else:
        record_list = target.env[model].search([])

    try:
        target.env[model].browse(record_list).unlink()
        print(f"Recordset('{model}', {record_list}) unlinked")
    except Exception as e:
        print(e)


def create_xml_id(model, target_record_id, source_record_id):
    ''' Creates an external id for a model
    example: create_xml_id('product.template', 89122, 5021)
    '''
    xml_id = f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}"
    values = {
        'module': xml_id.split('.')[0],
        'name': xml_id.split('.')[1],
        'model': model,
        'res_id': target_record_id,
    }
    try:
        print(values)
        target.env['ir.model.data'].create(values)
        return f"xml_id = {xml_id} created"
    except Exception:
        return f"ERROR: create_xml_id('{model}', {target_record_id}, {source_record_id}) failed. Does the id already exist?"
        
def map_record_to_xml_id(target_model, fields, unique, source_id):
    if unique:
        domain = [(item, '=', fields[item]) for item in unique]
        r_id = target.env[target_model].search(domain)
        print(r_id)
        if r_id != []:
            print(create_xml_id(target_model, r_id[0], source_id))
            return True
    return False
    
# ~ map_record_to_xml_id('account.account', 'code', '2710123', 10)


def get_target_record_from_id(model, source_record_id):
    ''' gets record from target database using record.id from source database
    example: get_target_record_from_id('product.attribute', 3422)
    returns: 0 if record cannot be found
    '''
    try:
        # ~ r = target.env.ref(f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}", raise_if_not_found=False)
        r = target.env['ir.model.data'].xmlid_to_res_model_res_id(f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}", raise_if_not_found=False)
        if r != [False, False]:
            r = target.env[r[0]].browse(r[1])
            return r
        else:
            print(f"couldnt find external id: {IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
            return False
    except Exception:
        print(f"couldnt find external id: {IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
        return False
        
def get_target_id_from_id(model, source_record_id):
    ''' gets record from target database using record.id from source database
    example: get_target_record_from_id('product.attribute', 3422)
    returns: 0 if record cannot be found
    '''
    try:
        # ~ r = target.env.ref(f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}", raise_if_not_found=False)
        r = target.env['ir.model.data'].xmlid_to_res_model_res_id(f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}", raise_if_not_found=False)
        if r != [False, False]:
            return r[1]
        else:
            print(f"couldnt find external id: {IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
            return False
    except Exception:
        print(f"couldnt find external id: {IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
        return False
    
def get_target_date_from_id(model, t, source_record_id):
    ''' gets record from target database using record.id from source database
    example: get_target_record_from_id('product.attribute', 3422)
    returns: 0 if record cannot be found
    '''
    try:
        # ~ r = target.env.ref(f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}", raise_if_not_found=False)
        r = target.env['ir.model.data'].xmlid_to_res_model_res_id(f"{IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}", raise_if_not_found=False)
        if r != [False, False]:
            r = t.read(r[1], ['last_migration_date'])
            return r[0]['last_migration_date']
        else:
            print(f"couldnt find external id: {IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
            return False
    except Exception as e:
        print(f"couldnt find external id: {IMPORT_MODULE_STRING}.{model.replace('.', '_')}_{source_record_id}")
        print(e)
        return False
        
def create_record_and_xml_id(target_model, source_model, fields, source_record_id, unique=None, i18n_fields=None, custom_xml_id = False):
    ''' Creates record on target if it doesn't exist, using fields as values,
    and creates an external id so that the record will not be duplicated
    example: create_record_and_xml_id('res.partner', {'name':'MyPartner'}, 2)
    '''
    if(custom_xml_id):
        source_record_id=custom_xml_id+str(source_record_id)
    if get_target_record_from_id(target_model, source_record_id):
        print(f"INFO: skipping creation, an external id already exist for [{target_model}] [{source_record_id}]")
    else:
        try:
            print(fields)
            if target_model == "account.journal":
                if fields['type'] == 'sale_refund':
                    fields['type'] = 'sale'
                if fields['type'] == 'purchase_refund':
                    fields['type'] = 'purchase'
            if target_model == "account.move.line":
                target.env.context['check_move_validity'] = False

            target_record_id = target.env[target_model].create(fields)
            print(f"Recordset('{target_model}', [{target_record_id}]) created")
            migrate_translation(source_model, target_model,
                                source_record_id, target_record_id,
                                i18n_fields)
            print(f"Recordset('{target_model}', [{target_record_id}]) translated")
            print(create_xml_id(target_model, target_record_id, source_record_id))
            return target_record_id
        except Exception as e:
            print(f"ERROR: target.env['{target_model}'].create ({source_record_id}) failed")
            if not map_record_to_xml_id(target_model, fields, unique, source_record_id):
                if 'image_1920' in fields.keys():
                    fields.pop('image_1920')
                print(f"Fields: {fields}")
                print(f"couldnt find the target record")
                print(f"e: {e}")

import re
def get_trailing_number(s):
    m = re.search(r'\d+$', s)
    return int(m.group()) if m else None


def find_all_ids_in_target_model(target_model, ids=[]):
    print(target_model)
    target_ids = target.env["ir.model.data"].find_all_ids_in_target(target_model)
    # ~ print(f"source_ids: {ids}")
    # ~ print("="*99)
    # ~ print(f"target_ids: {target_ids}")
    to_migrate = (set(ids) - set(target_ids))
    return to_migrate

def get_translatable_fields(t_model, s_model, fields: dict) -> dict:
    """ Return all fields that are translatable in both source
    and target.
    :returns: dict with source and target fields.
    """
    res = {}
    t_fields = t_model.fields_get(list(fields.values()))
    for name, field_data in s_model.fields_get(list(fields.keys())).items():
        if field_data.get('translate') and t_fields[fields[name]].get('translate'):
            res[name] = fields[name]
    return res

def migrate_translation(source_model, target_model, source_id, target_id, fields):
    """ Migrate swedish translations for the given source and
    target records.
    """
    # TODO: Recreate for multiple languages.
    if not fields:
        return
    vals = {}
    s_record = source_se.env[source_model].search_read([('id', '=', source_id)], list(fields.keys()))
    s_record = s_record and s_record[0] or None
    if not s_record:
        return
    # TODO: not an exact replica of fields in migrate_model. Look into
    #  that. Not every feature is needed, since this function will only
    #  handle translateable fields. This includes Char, Text and Html
    #  fields. Any more?
    for name, value in s_record.items():
        if name != 'id':
            vals[fields[name]] = value
    target_se.env[target_model].write([target_id], vals)
    
def get_uom_ids():
    uom_xmlid_values = UNITS_OF_MEASURE_EXID.values()
    for data in target.env['ir.model.data'].search_read([
            ('model', '=', 'uom.uom'),
            ('name', '=like', 'product_uom_%'),
            ('module', '=', 'uom')], ['res_id', 'name']):
        for key in UNITS_OF_MEASURE_EXID.keys():
            if UNITS_OF_MEASURE_EXID[key] == data['name']:
                UNITS_OF_MEASURE[key] = data['res_id']
    pprint.pprint(UNITS_OF_MEASURE)
get_uom_ids()

def get_accounts_ids():
    account_xmlid_values = account_translation_table_xid.values()
    for data in target.env['ir.model.data'].search_read([
            ('model', '=', 'account.account'),
            ('name', 'in', list(account_translation_table_xid.values())),
            ('module', '=', 'l10n_se')], ['res_id', 'name']):
        for key in account_translation_table_xid.keys():
            if account_translation_table_xid[key] == data['name']:
                account_translation_table[key] = data['res_id']
    pprint.pprint("ACCOUNT TABLE")
    pprint.pprint(account_translation_table)
get_accounts_ids()

def get_account_tax_ids_from_account_tax_code_ids():
    account_tax_xmlid_values = account_tax_code_to_account_tax_table_xid.values()
    for data in target.env['ir.model.data'].search_read([
            ('model', '=', 'account.tax'),
            ('name', 'in', list(account_tax_code_to_account_tax_table_xid.values())),
            ('module', '=', 'l10n_se')], ['res_id', 'name']):
        for key in account_tax_code_to_account_tax_table_xid.keys():
            if account_tax_code_to_account_tax_table_xid[key] == data['name']:
                account_tax_code_to_account_tax_table[key] = data['res_id']
    pprint.pprint("ACCOUNT TAX CODE TO ACCOUNT TAX TABLE")
    pprint.pprint(account_tax_code_to_account_tax_table)
get_account_tax_ids_from_account_tax_code_ids()

def get_account_tax_ids():
    account_tax_xmlid_values = account_tax_table_xid.values()
    for data in target.env['ir.model.data'].search_read([
            ('model', '=', 'account.tax'),
            ('name', 'in', list(account_tax_table_xid.values())),
            ('module', '=', 'l10n_se')], ['res_id', 'name']):
        for key in account_tax_table_xid.keys():
            if account_tax_table_xid[key] == data['name']:
                account_tax_table[key] = data['res_id']
    pprint.pprint("ACCOUNT TAX TABLE")
    pprint.pprint(account_tax_table)
get_account_tax_ids()

def migrate_model(model, migrate_fields=[], include = False, exclude_patterns = [], diff={}, custom={}, hard_code={}, debug=False, create=True, domain=None, unique=None, after_migration=None, calc=None, xml_id_suffix = None, just_bind = False, bypass_date = False):
    '''
    use this method for migrating a model with return dict from get_all_fields()
    example:
        product_template = get_all_fields(
            'product.template', exclude=['message_follower_ids'])
        simple_migrate_model('product.template', product_template)
    :param after_migration: Custom method run after migration of a record.
    '''
    print()
    print("="*99)
    print(f"Migrating model: {model}")
    print()
    domain = domain or []
    source_model = model
    target_model = model
    if type(model) == dict:
        source_model = list(model.keys())[0]
        target_model = model[list(model.keys())[0]]

    s = source.env[source_model]
    t = target.env[target_model]
    if not include:
        fields = get_all_fields(source_model, target_model, migrate_fields, custom, exclude_patterns)
    else:
        fields = {e:e for e in migrate_fields}
    for key in custom.keys():
        fields[key] = custom[key]
    i18n_fields = get_translatable_fields(s, t, fields)
    errors = {'ERRORS:'}
    # Set migration date before reading. Otherwise we may miss updates in next migration.
    now = odoo.fields.Datetime.now()
    if create:
        to_migrate = s.search(domain)
        to_migrate = find_all_ids_in_target_model(target_model, to_migrate)
        # ~ print("to migrate:")
        # ~ print(to_migrate)
    elif not create:
        to_migrate = s.search_read(domain, ['id', 'write_date'], order='write_date DESC')

    print(f'fields to migrate: {fields}')
    for r in to_migrate:
        if just_bind:
            map_record_to_xml_id(target_model, fields, unique, source_id)
            continue
        print("="*99)
        print(f"Migrating model: {model}")
        if not create:
            t_date = get_target_date_from_id(target_model, t, r['id'])
            print(f"t_date: {t_date}, {r['write_date']}")
            if t_date == False or r['write_date'] == False or t_date < r['write_date'] or bypass_date:
                r = r['id']
            else:
                print(f"record: {r}. is already up to date")
                continue
        target_record = get_target_record_from_id(target_model, r)
        if create and target_record:
            print(
                f"INFO: skipping creation, an external id already exist for [{target_model}] [{r}]")
            continue
        record = s.read(r, list(fields.keys()))
        # ~ print(f"record: {record}")
        if type(record) is list:
            record = record[0]
        vals = {}
        # Customize certain fields before creating records
        for key in fields:
            # ~ print(record[key])
            # Remove /page if it exists in url (odoo v8 -> odoo 14)
            if not calc or key not in calc.keys():
                print(f"key: {key}")
                print(record[key])
                if key == 'company_id':
                    vals.update({'company_id': 1})
                elif key == 'url' and type(record[key]) is str:
                    url = record[key]
                    if url.startswith('/page'):
                        url = url.replace('/page', '')
                    vals.update({fields[key]: url})

                # Stringify datetime objects
                # TypeError('Object of type datetime is not JSON serializable')
                elif type(record[key]) is datetime.datetime:
                    vals.update({fields[key]: str(record[key])})

                # If the value of the key is a list, look for the corresponding record on target instead of copying the value directly
                # example: country_id 198, on source is 'Sweden' while
                #          country_id 198, on target is 'Saint Helena, Ascension and Tristan da Cunha'
                elif type(record[key]) is list:
                    field_definition = s.fields_get(key)[key]
                    print(f"field_definition: {field_definition}")
                    if field_definition['type'] == 'many2one':
                        try:
                            if field_definition["relation"] == "product.uom":
                                vals.update({fields[key]:  UNITS_OF_MEASURE[record[key][0]]})
                            elif field_definition["relation"] == "account.account":
                                vals.update({fields[key]:  account_translation_table[record[key][0]]})
                            elif field_definition["relation"] == "account.tax":
                                vals.update({fields[key]:  account_tax_table_xid[record[key][0]]})
                            elif field_definition["relation"] == "account.tax.code":
                                if record[key] not in [29,37,47,49,53,55]:# don't need to set tax_line_id in these cases
                                    vals.update({fields[key]:  account_tax_code_to_account_tax_table[record[key][0]]})
                            elif field_definition["relation"] == "res.company":
                                vals.update({fields[key]: COMPANY_ID})
                            else:
                                vals.update({fields[key]: get_target_id_from_id(field_definition['relation'], record[key][0])})
                            continue
                        except Exception:
                            error = f"Target '{key}': {[record[key], field_definition['relation']]} does not exist"
                            if error not in errors:
                                errors.add(error)
                                if debug:
                                    print(error)
                    elif field_definition['type'] in ('one2many', 'many2many'):
                        # Convert every id in the list
                        ids = []
                        for id in record[key]:
                            rec = get_target_id_from_id(field_definition['relation'], id)
                            if rec:
                                ids.append(rec)
                        if ids:
                            vals[fields[key]] = [(6,0,ids)]
                else:
                    vals[fields[key]] = record[key]
        #vals.update(custom[])
        # Break operation and return last dict used for creating record if something is wrong and debug is True
        vals.update(hard_code)

        if calc and target_record:
            print("CALC"*99)
            for key in calc.keys():
                print(calc[key])
                exec(calc[key])
        if create:
            target_record_id = create_record_and_xml_id(target_model, source_model, vals, r, unique, i18n_fields)
            print(after_migration)
            if after_migration:
                after_migration(record['id'], target_record_id, create=True)
            if type(target_record_id) != int and debug:
                return vals
        elif target_record:
            try:
                vals.update({'last_migration_date': str(now)})
                image = False
                if 'image_1920' in vals.keys():
                    image = vals.pop('image_1920')
                if model == "account.move.line":
                    target_record.env.context['check_move_validity'] = False
                target_record.write(vals)
                print(f"Writing to existing {vals}")
                
                if image:
                    try:
                        target_record.write({'image_1920': image})
                        print(f"Writing image to existing")
                    except Exception as e:
                        print(f"writing image failed")
                        print(e)
                migrate_translation(source_model, target_model, record['id'], target_record.id, i18n_fields)
                print(f"migrated translation")
                if after_migration:
                    after_migration(record['id'], target_record.id, create=False)
                    print(f"after_migration")
            except Exception as e:
                if 'image_1920' in vals.keys():
                    vals.pop('image_1920')
                print(f"Failed at writing to existing {target_record, r, vals}")
                print(e)
                return vals
            

    return errors

def get_relations_from_model(database, model):
    # ~ SELECT Distinct(model), name FROM ir_model_fields WHERE relation='product.uom' ;
    s = database.env['ir.model.fields']
    search_terms = [('relation', '=', model)]
    results = s.browse(s.search(search_terms))
    used_uom = {}
    for result in results:
        try:
            print(f"model: {result.model}, name: {result.name}")
            ref_model = database.env[result.model]
            res = ref_model.search([])
            uom_id = 0
            for r in res:
                uom_id = ref_model.read(r, [result.name])[result.name][0]
                if not uom_id in used_uom.keys():
                    used_uom[uom_id] = 1
                else:
                    used_uom[uom_id] += 1
        except Exception:
            print(f"model: {result.model} doesnt exist")
        print(used_uom)




def get_id_from_xml_id(record, relation):
    '''
    Returns a dict with { key: id } of target record
    example:
    source_record = source.env['res.company'].browse(1)
    get_target_id_from_source(source_record, 'country_id')
    '''
    print(f"record: {record}, relation: {relation}")
    s = source.env['ir.model.data']
    d = [('model', '=', relation),
         ('res_id', '=', record[0])]
    r = target.env.ref(s.browse(s.search(d)).complete_name).id
    print(f"r: {r}")
    return r


def get_all_fields(source_model, target_model, exclude=[], diff={}, exclude_patterns=[]):
    '''
    Returns dict with key as source model keys and value as target model keys
    Use exclude = ['this_field', 'that_field'] to exclude keys on source model
    Use diff = {'image':'image_1920'} to update key-value pairs manually
    '''
    fields = {}
    target_field_keys = target.env[target_model]._columns

    # for key, value in target.env[model].fields_get().items():
    #     if not value['readonly']:
    #         target_field_keys.append(key)

    for key in source.env[source_model]._columns:
        if exclude_patterns:
            for exclude_pattern in exclude_patterns:
                if re.search(exclude_pattern, key):
                    print(f'skipping key {key}')
                    exclude.append(key)
        if key in exclude:
            print(f'skipping key {key}')
            continue
        elif key in target_field_keys:
            fields.update({key: key})
            print(f'adding key {key}')

    fields.update(diff)
    print(fields, diff)

    return fields


def get_fields_difference(model):
    '''
    Returns list with fields difference
    example: get_fields_difference('res.company')
    '''
    source_set = set(source.env[model]._columns)
    target_set = set(target.env[model]._columns)

    return {'source': source_set - target_set, 'target': target_set - source_set}

def get_required_fields(model):
    '''
    Returns list with required fields
    example: get_required_fields('res.company')
    '''
    source_dict = source.env[model].fields_get()
    target_dict = target.env[model].fields_get()
    source_keys=[]
    target_keys=[]
    for key in source_dict:
        if source_dict[key]['required']:
            source_keys.append(key)
    for key in target_dict:
        if target_dict[key]['required']:
            target_keys.append(key)
    return {'source': source_keys, 'target': target_keys}

print(4)


{91: 63, 101: 73, 126: 101, 129: 103, 130: 104, 131: 105, 133: 107, 134: 109, 1300: 109, 135: 110, 136: 111, 138: 114, 145: 121, 147: 123, 148: 124, 153: 129, 155: 131, 158: 134, 160: 136, 162: 138, 203: 194, 1528: 199, 226: 212, 229: 217, 1281: 219, 234: 222, 256: 242, 257: 243, 258: 244, 260: 246, 261: 247, 262: 248, 276: 263, 277: 264, 281: 269, 289: 277, 300: 286, 312: 289, 326: 301, 359: 320, 363: 325, 367: 330, 375: 338, 1324: 339, 390: 359, 393: 362, 436: 405, 453: 423, 467: 441, 468: 442, 470: 444, 474: 447, 512: 448, 516: 450, 517: 451, 519: 453, 551: 492, 556: 497, 559: 500, 560: 501, 564: 505, 571: 514, 572: 515, 1301: 519, 590: 521, 582: 529, 600: 540, 602: 544, 621: 569, 623: 571, 646: 593, 648: 595, 650: 597, 657: 604, 661: 608, 664: 612, 1520: 628, 1530: 631, 674: 640, 675: 641, 680: 646, 689: 652, 701: 663, 702: 664, 704: 666, 707: 669, 708: 670, 710: 672, 711: 673, 712: 674, 714: 676, 715: 677, 716: 678, 727: 690, 728: 691, 730: 693, 731: 694, 732: 695, 736: 699, 738: 701, 742: 705, 749: 712, 750: 713, 755: 718, 758: 721, 759: 722, 761: 723, 762: 727, 763: 728, 764: 729, 765: 730, 766: 731, 768: 736, 769: 737, 770: 738, 771: 739, 772: 740, 773: 741, 775: 743, 776: 744, 777: 745, 778: 746, 779: 747, 780: 748, 781: 749, 789: 751, 790: 753, 793: 756, 795: 758, 796: 759, 797: 760, 798: 761, 799: 762, 800: 763, 801: 764, 803: 766, 804: 767, 805: 768, 806: 769, 807: 770, 810: 773, 812: 775, 814: 777, 815: 778, 817: 780, 819: 782, 820: 783, 821: 784, 823: 786, 825: 788, 828: 791, 830: 793, 831: 794, 833: 796, 834: 797, 835: 798, 836: 799, 838: 801, 839: 802, 840: 803, 844: 807, 845: 808, 847: 810, 848: 811, 854: 817, 855: 818, 859: 822, 864: 827, 871: 836, 874: 839, 875: 840, 876: 841, 877: 842, 878: 843, 880: 845, 881: 846, 890: 855, 891: 856, 895: 859, 896: 860, 898: 861, 904: 863, 905: 864, 906: 865, 907: 866, 908: 867, 909: 868, 910: 869, 916: 874, 917: 875, 937: 888, 938: 889, 940: 892, 942: 894, 943: 895, 952: 901, 953: 902, 961: 907, 972: 915, 976: 919, 977: 920, 980: 923, 983: 926, 984: 927, 990: 933, 995: 938, 996: 939, 997: 940, 1000: 943, 1001: 944, 1003: 947, 1007: 951, 1009: 953, 1011: 955, 1013: 957, 1014: 958, 1017: 961, 1018: 962, 1019: 963, 1020: 964, 1031: 976, 1034: 978, 1039: 983, 1049: 987, 1052: 993, 1054: 997, 1055: 998, 1056: 999, 1057: 1000, 1059: 1002, 1060: 1003, 1061: 1004, 1062: 1005, 1064: 1007, 1065: 1008, 1066: 1009, 1067: 1010, 1072: 1015, 1076: 1019, 1099: 1042, 1100: 1043, 1102: 1045, 1105: 1048, 1108: 1051, 1112: 1055, 1175: 1132, 1177: 1134, 1178: 1135, 1195: 1152, 1205: 1161, 1207: 1163, 1208: 1164, 1209: 1165, 1210: 1167, 1211: 1168, 1212: 1169, 1213: 1170, 1228: 1183, 1229: 1184, 1231: 1186, 1232: 1188, 1235: 1191, 1254: 1203, 1258: 1207, 202: 40, 264: 42, 325: 42, 303: 45, 309: 46, 452: 47, 476: 3, 479: 6, 480: 7, 485: 11, 502: 26, 503: 27, 504: 28, 505: 29, 506: 30, 508: 32, 509: 33, 510: 34, 514: 36, 578: 55, 586: 55, 587: 56, 588: 57, 625: 50, 665: 58, 1260: 54}
