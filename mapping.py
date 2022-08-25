# region dokument.xlsx
dokument = {'model': 'ir.attachment',
            'path': '/mnt/woodoo_prod/Lime migration/211128/ESSexport/FileExport',
            'fields': {'dokumentmall': 'dokumentmall',
                     'fafast': 'fafast.idfafast',
                     'file_extension': 'dokument__fileextension',
                     'kund': 'kund.idkund',
                     'kurs': 'kurs.idkurs',
                     'kursdeltagare':'kursdeltagare.idkursdeltagare',
                     'produkt': 'produkt.idprodukt',
                     'uppdrag': 'uppdrag.iduppdrag',
                     },
          'before': """
fafast = vals.pop('fafast')
file_extension = vals.pop('file_extension')
kund = vals.pop('kund')
kurs = vals.pop('kurs')
kursdeltagare = vals.pop('kursdeltagare')
produkt = vals.pop('produkt')

name = vals.pop('dokumentmall')
if name:
    name = name.split(' ')
    name = ' '.join(name[:len(name)-2])
    if file_extension:
        file_extension = '.' + file_extension
        if file_extension not in name:
            name = name + file_extension
        vals['name'] = name
else:
    vals['skip'] = True

uppdrag = vals.pop('uppdrag')
if uppdrag:
    project_xmlid = get_xmlid('uppdrag', uppdrag)
    project_id = get_res_id(project_xmlid)
    vals['res_id'] = project_id
    vals['res_model'] = 'project.project'

files = sorted(Path(params['path']).glob(str(row[0].value) + '*'))

if len(files) == 1:
    with files[0].open('rb') as datas:
        vals['datas'] = str(base64.b64encode(datas.read()))


"""}
# endregion dokument.xlsx

# region kund.xlsx
kund = {
    'model': 'res.partner',
    'fields': {
        'city': 'ort',
        'comment': 'annan_info',
        'email': 'epost',
        'kundgrupp': 'kundgrupp',
        'name': 'descriptive',
        'legacy_no': 'pnrchar',
        'phone': 'telefon',
        'social_sec_nr': 'pnrchar',
        'street': 'adress',
        'vat': 'vatnr',
        'zip': 'postnr'
        },
    '__import__.kategori_kund': {
        'model': 'res.partner.category',
        'vals': {'name': 'kund'}
        },
    '__import__.res_partner_company_type_1_statliga': {
        'model': 'res.partner.company.type',
        'vals': {
            'name': 'Statliga',
            'shortcut': 'stat'
            },
        },
    '__import__.res_partner_company_type_2_privata': {
        'model': 'res.partner.company.type',
        'vals': {
            'name': 'Privata',
            'shortcut': 'priv'
            },
        },
    'before': """
category_id = get_res_id('__import__.kategori_kund')

vals['category_id'] = [(4, category_id, 0)]
vals['country_id'] = get_res_id('base.se')
vals['is_company'] = False

for key in ['city', 'comment', 'email', 'legacy_no', 'mobile', 'phone', 'street', 'vat', 'zip']:
    if key in vals and not vals[key]:
        vals[key] = False

for key in ['city', 'comment', 'legacy_no', 'mobile', 'name', 'phone', 'street', 'vat', 'zip']:
    if key in vals and type(vals[key]) is int:
        if key in ['mobile', 'phone']:
            vals[key] = '0' + str(vals[key])
        else:
            vals[key] = str(vals[key])

for key in ['name']:
    vals[key] = " ".join(vals[key].split())

if vals['vat'] and not vals['vat'].startswith('SE'):
    vals['vat'] = False

vals['social_sec_nr'] = False
if (ssn := vals['legacy_no']):
    ssn = str(vals['legacy_no'])
    for a, b in [
        (' ', ''),
        ('–', '-'),
        ('_', '-'),
    ]:
        ssn = ssn.replace(a, b)
    if len(ssn) == 12:
        if int(ssn[4:6]) > 12:
            vals['is_company'] = True
        else:
            vals['is_company'] = False
        ssn = f"{ssn[:8]}-{ssn[8:]}"
    elif len(ssn) == 11:
        if ssn[6] == '-':
            if int(ssn[2:4]) > 12:
                vals['is_company'] = True
            else:
                vals['is_company'] = False
    elif len(ssn) == 10:
        ssn = f"{ssn[:6]}-{ssn[6:]}"
        if int(ssn[2:4]) > 12:
            vals['is_company'] = True
        else:
            vals['is_company'] = False
            if int(ssn[0:2]) > 22:
                ssn = '19' + ssn
            else:
                input(ssn)
    else:
        input(ssn)
    
    vals['legacy_no'] = ssn
kundgrupp = vals.pop('kundgrupp')
if kundgrupp:
    for x in ['70']:
        if x in kundgrupp:
            vals['partner_company_type_id'] = get_res_id('__import__.res_partner_company_type_1_statliga')
    for x in ['60', '61', '62']:
        if x in kundgrupp:
            vals['partner_company_type_id'] = get_res_id('__import__.res_partner_company_type_2_privata')
    if kundgrupp in [
        'Kommun (60)',
        'Statligt affärsdrivande verk (60)', 
        'Statligt bolag (60)',
        'Utbildningsinst. ej statlig (60)',
        'Övrigt privat företag/bolag (60)',
        'Skogsföretag (62)',
        'Statlig myndighet (70)',
        'Utbildningsinst. statlig (70)',
        ]:
        vals['is_company'] = True

'Privatperson ej skogsägare (60)'
'Övrig (60)'
'Privat skogsägare (61)'
'Utrikes EU (80)'
'Utrikes ej EU (90)'
"""}
# endregion kund.xlsx

# region pepers.xlsx
pepers = {'model': 'res.partner',
          'fields': {
            'comment': 'info',
            'email': 'epost',
            'kund': 'kund.idkund',
            'mobile': 'mobnr',
            'name': 'namn',
            'phone': 'telnr'
            },
          'before': """
category_xmlid = get_xmlid('kategori', 'pepers')
category_id = get_res_id(category_xmlid)
if not category_id:
    category_id = target.env['res.partner.category'].create({'name':'pepers'})
    create_xmlid('res.partner.category', category_id, category_xmlid)
vals['category_id'] = [(4, category_id, 0)]
vals['country_id'] = get_res_id('base.se')

for key in ['comment', 'email', 'kund', 'mobile', 'name', 'phone']:
    if key in vals and not vals[key]:
        vals[key] = False

if type(vals['mobile']) is int:
    if not str(vals['mobile']).startswith('0'):
        vals['mobile'] = '0' + str(vals['mobile'])

if type(vals['name']) is int:
    vals['name'] = str(vals['name'])

parent_xmlid = get_xmlid('idkund', vals.pop('kund'))
vals['parent_id'] = get_res_id(parent_xmlid)

if type(vals['phone']) is int:
    if not str(vals['phone']).startswith('0'):
        vals['phone'] = '0' + str(vals['phone'])
"""}
# endregion pepers.xlsx

# region kursdeltagare.xlsx
kursdeltagare = {'model': 'res.partner',
                 'fields': {'city': 'ort',
                            'email': 'epost',
                            'kund.idkund': 'kund.idkund',
                            'kurs.idkurs': 'kurs.idkurs',
                            'name': 'namn',
                            'phone': 'telnr',
                            'street': 'adress',
                            'zip': 'postnr'},
                 'before': """
category_xmlid = get_xmlid('kategori', 'kursdeltagare')
category_id = get_res_id(category_xmlid)
if not category_id:
    category_id = target.env['res.partner.category'].create(
        {'name':'kursdeltagare'})
    create_xmlid('res.partner.category', category_id, category_xmlid)
vals['category_id'] = [(4, category_id, 0)]

if type(vals['name']) is int:
    vals['name'] = str(vals['name'])

parent_xmlid = get_xmlid('kund', vals.pop('kund.idkund'))
vals['parent_id'] = get_res_id(parent_xmlid)

if type(vals['phone']) is int:
    if not str(vals['phone']).startswith('0'):
        vals['phone'] = '0' + str(vals['phone'])

params['event_xmlid'] = get_xmlid('kurs', vals.pop('kurs.idkurs'))
""",
                 'after': """
event_xmlid = params.get('event_xmlid')
event_id = get_res_id(event_xmlid)
partner_id = get_res_id(xmlid)
if event_id and partner_id:
    er_model = 'event.registration'
    er_vals = {
        'event_id': event_id,
        'partner_id': partner_id,
        }
    kurs_id = xmlid.split('_')[-1]
    er_xmlid = get_xmlid('kursdeltagare_kurs', kurs_id)

    if mode == 'debug':
        print(f"{er_vals=}")
        print(f"{er_xmlid=}")
    else:
        create_record_and_xmlid_or_update(er_model, er_vals, er_xmlid)
"""}
# endregion kursdeltagare.xlsx

# region fafast.xlsx
fafast = {'model': 'property.property',
          'fields': {'agare.idagare': 'agare.idagare',
                     'name': 'namnfast',
                     'property_key': 'fastnr',
                     'xkoordinat': 'xkoordinat',
                     'ykoordinat': 'ykoordinat'},
          'before': """
latitude = str(vals.pop('xkoordinat')).replace('.','')
longitude = str(vals.pop('ykoordinat')).replace('.','')
name = str(vals['name'])

if name and ',' in name:
    vals['city'] = name.split(',')[0]

if len(latitude) == 7 and len(longitude) == 7:
    vals['property_lat_rt90'] = latitude
    vals['property_long_rt90'] = longitude
    vals['latitude'] = False
    vals['longitude'] = False

elif len(latitude) == 7 and len(longitude) == 6:
    vals['property_lat_sweref99'] = latitude
    vals['property_long_sweref99'] = longitude
    vals['latitude'] = False
    vals['longitude'] = False

params['agare_id'] = vals.pop('agare.idagare')
""",
          'after': """
agare_id = params.get('agare_id')

partner_xmlid = get_xmlid('kund', agare_id)
partner_id = get_res_id(partner_xmlid)
if partner_id:
    stakeholder_vals = {'partner_id': partner_id}
    stakeholder_model = 'property.stakeholder'
    stakeholder_xmlid = get_xmlid('fastighetsagare', agare_id)

    fastighet_id = xmlid.split('_')[-1]
    property_xmlid = get_xmlid('fafast', fastighet_id)
    property_id = get_res_id(property_xmlid)
    if property_id:
        stakeholder_vals['property_id'] = property_id

        if mode == 'debug':
            print(f"{stakeholder_vals=}")
            print(f"{stakeholder_xmlid=}")
        else:
            create_record_and_xmlid_or_update(
                stakeholder_model, stakeholder_vals, stakeholder_xmlid)
"""}
# endregion fafast.xlsx

# region kurs.xlsx
kurs = {'model': 'event.event',
        'fields': {'name': 'kursbenamning',
                   'date_begin': 'startdat',
                   'date_begin_time': 'starttidpunkt',
                   'date_end': 'antaldagar',
                   'kursstatus': 'kursstatus',
                   'user_id': 'kursansvarig.anvandare'},
        'before': """
if not vals['date_begin']:
    vals['skip'] = True
else:
    kursstatus = vals.pop('kursstatus')
    if kursstatus:
        if kursstatus.startswith('1') or kursstatus.startswith('2'):
            vals['stage_id'] = get_res_id('event.event_stage_new')
        elif kursstatus.startswith('3'):
            vals['stage_id'] = get_res_id('event.event_stage_announced')
        elif kursstatus.startswith('4'):
            invited_xmlid = 'event.event_stage_invited'
            invited = get_res_id(invited_xmlid)
            if not invited:
                invited = target.env['event.stage'].create({
                    'name': 'Inbjudan skickad',
                    'description': 'Inbjudan skickad'
                    })
                create_xmlid('event.stage', invited, invited_xmlid)
            vals['stage_id'] = invited
        elif kursstatus.startswith('5'):
            partly_invoiced_xmlid = 'event.event_stage_partly_invoiced'
            partly_invoiced = get_res_id(partly_invoiced_xmlid)
            if not partly_invoiced:
                partly_invoiced = target.env['event.stage'].create({
                    'name': 'Delfakturerad',
                    'description': 'Delfakturerad'
                    })
                create_xmlid('event.stage', partly_invoiced,
                             partly_invoiced_xmlid)
            vals['stage_id'] = partly_invoiced
        elif kursstatus.startswith('6'):
            fully_invoiced_xmlid = 'event.event_stage_fully_invoiced'
            fully_invoiced = get_res_id(fully_invoiced_xmlid)
            if not fully_invoiced:
                fully_invoiced = target.env['event.stage'].create({
                    'name': 'Slutfakturerad',
                    'description': 'Slutfakturerad'
                    })
                create_xmlid('event.stage', fully_invoiced,
                             fully_invoiced_xmlid)
            vals['stage_id'] = fully_invoiced
        elif kursstatus.startswith('7'):
            vals['stage_id'] = get_res_id('event.event_stage_cancelled')

    uid = vals['user_id']
    if uid:
        uid = target.env['res.users'].search([('login', '=', uid)])
        if uid:
            vals['user_id'] = uid[0]
    if not uid:
        vals.pop('user_id')
    date_begin_time = vals.pop('date_begin_time')
    if not date_begin_time:
        date_begin_time = '00:00'
    fmt = '%Y-%m-%d %H:%M'
    tz = pytz.timezone('Europe/Stockholm')
    naive = datetime.strptime(f"{vals['date_begin']} {date_begin_time}", fmt)
    local = tz.localize(naive, is_dst=True)
    date_begin = local.astimezone(pytz.utc)
    vals['date_begin'] = datetime.strftime(date_begin, fmt)
    if vals['date_end']:
        date_end = date_begin + timedelta(days=vals['date_end'])
        vals['date_end'] = datetime.strftime(date_end, fmt)
    else:
        vals['date_end'] = vals['date_begin']
"""}
# endregion kurs.xlsx

# region artikel.xlsx
artikel = {'model': 'product.template',
           'fields': {
                'name': 'benamning',
                'list_price': 'pris',
                'parent_template_id': 'produkt.idprodukt',
                'uom_id': 'enhet',
            },
           'before': """

vals['list_price'] = float(vals['list_price'].split(',')[0].replace('.',''))
vals['property_account_expense_id'] = get_res_id('l10n_se.1_chart4001')
vals['property_account_income_id'] = get_res_id('l10n_se.1_chart3001')
vals['service_policy'] = 'delivered_timesheet'
vals['service_tracking'] = 'task_in_project'

UOM = {
    'dag': 'day',
    'ha': 'ha',
    'km': 'km',
    'm3': 'cubic_meter',
    'tim': 'hour',
    }

uom = vals['uom_id']
uom_xmlid = f"uom.product_uom_{UOM.get(uom, 'unit')}"

vals['uom_id'] = get_res_id(uom_xmlid)

# Create in a datafile instead
if not vals['uom_id'] and uom == 'ha':
    if not (area_id := get_res_id('__import__.uom_categ_area')):
        area_id = self.env['uom.category'].create({
            'name': 'Area'
        })
        self.env['ir.model.data'].create({
            'model': 'uom.category',
            'module': '__import__',
            'name': 'uom_categ_area',
            'res_id': area_id,
        })

    if not (m2_id := get_res_id('__import__.product_uom_square_meter')):
        m2_id = self.env['uom.uom'].create({
            'category_id': area_id,
            'name': 'm²',
        })
        self.env['ir.model.data'].create({
            'model': 'uom.uom',
            'module': '__import__',
            'name': 'product_uom_square_meter',
            'res_id': m2_id,
        })

    ha_id = self.env['uom.uom'].create({
        'category_id': area_id,
        'factor': 0.0001,
        'name': 'ha',
        'uom_type':'bigger',
        })

    self.env['ir.model.data'].create({
        'model': 'uom.uom',
        'module': '__import__',
        'name': 'product_uom_ha',
        'res_id': ha_id,
        })
    vals['uom_id'] = ha_id

vals['uom_po_id'] = vals['uom_id']
params['parent_template_xmlid'] = get_xmlid(
    'prod_reg', vals.pop('parent_template_id'))
""",
           'after': """
Template = self.env['product.template']
template_id = get_res_id(xmlid)
if template_id:
    template = Template.read(template_id)[0]
    product_id = template['product_variant_id'][0]
    if product_id:
        parent_template_id = get_res_id(params.get('parent_template_xmlid'))
        if parent_template_id:
            parent_template = Template.read(parent_template_id)[0]
            parent_product_id = parent_template['product_variant_id'][0]
            if parent_product_id:
                ppl_model = 'product.pack.line'
                ppl_vals = {
                    'parent_product_id': parent_product_id,
                    'product_id': product_id,
                    }
                ppl_xmlid = get_xmlid('pack_artikel', xmlid.split('_')[-1])
                create_record_and_xmlid_or_update(
                    model=ppl_model, 
                    vals=ppl_vals, 
                    xmlid=ppl_xmlid
                )
            income_id = parent_template['property_account_income_id']
            if income_id:
                Template.write(
                    template_id, {'property_account_income_id': income_id[0]})
"""}
# endregion artikel.xlsx

# region prod_reg.xlsx
prod_reg = {'model': 'product.template',
            'fields': {
                'description': 'intern_beskrivning',
                'description_sale': 'beskrivning',
                'name': 'namn',
                'verksamhetsgren': 'verksamhetsgren',
            },
            'before': """
for key in ['description', 'description_sale', 'name', 'verksamhetsgren']:
    if key in vals and not vals[key]:
        vals[key] = False

verksamhetsgren = vals.pop('verksamhetsgren')
categ_xmlid = get_xmlid('product_category', verksamhetsgren)
vals['categ_id'] = get_res_id(categ_xmlid) or 1
vals['pack_ok'] = True
vals['pack_type'] = 'detailed'
vals['pack_component_price'] = 'detailed'
vals['pack_modifiable'] = True
vals['property_account_expense_id'] = get_res_id('l10n_se.1_chart4001')
vals['property_account_income_id'] = get_res_id('l10n_se.1_chart3001')
if verksamhetsgren:
    if verksamhetsgren in ['P1109', 'P1110', 'P1111', 'P1160', 'P1180', 'P1280', 'P1370', 'P1385', 'P1395', 'P1410', 'P1420', 'P1425', 'P1430', 'P1590', 'P1601', 'P1740', 'P1751', 'P1760', 'P1790']:
        vals['property_account_income_id'] = get_res_id(
            'account_sks.chart3332')
    elif verksamhetsgren in ['P1210', 'P1215', 'P1230', 'P1232', 'P1233',
        'P1234', 'P1235', 'P1236', 'P1237', 'P1238', 'P1239', 'P1241',
        'P1242', 'P1243', 'P1244', 'P1245', 'P1246', 'P1247', 'P1248',
        'P1249', 'P1260', 'P1261', 'P1262', 'P1263', 'P1264', 'P1265',
        'P1266', 'P1267']:
        vals['property_account_income_id'] = get_res_id(
            'account_sks.chart3322')
"""}
# endregion prod_reg.xlsx

# region uppdrag.xlsx
uppdrag = {'model': 'project.project',
           'fields': {'annan_info': 'annan_info',
                      'epost': 'ansvarig_medarbetare.epost',
                      'name': 'uppdragsbenamning',
                      'kund': 'kund.idkund',
                      'ovrig_information': 'ovrig_information',
                      'project_no': 'projekt',
                      'uppdragsstatus': 'uppdragsstatus'},
           'before': """
kund = vals.pop('kund')
if kund:
    partner_id = get_res_id(get_xmlid('kund', kund))
    if partner_id:
        vals['partner_id'] = partner_id

epost = vals.pop('epost')
if epost:
    user_id = target.env['res.users'].search([('login', '=', epost.lower())])
    if user_id:
        vals['user_id'] = user_id[0]
    else:
        vals['user_id'] = 2

if not vals['project_no']:
    vals['project_no'] = 'Saknas'

annan_info = vals.pop('annan_info')
ovrig_information = vals.pop('ovrig_information')
description = ''
vals['description'] = False
if ovrig_information:
    description += f"Övrig information: {ovrig_information}\\n"

if annan_info:
    description += f"Annan info: {annan_info}\\n"

if description:
    vals['description'] = description

uppdragsstatus = vals.pop('uppdragsstatus')

# type_id = 0 FIXAAAAAAAAAAAAAAAAAA

# if uppdragsstatus in ['Förfrågan']:
#     type_id = get_res_id(
#         'project_uppdragsforfragningar.project_stage_incoming')

# elif uppdragsstatus in ['Offert']:
#     type_id = get_res_id('project_uppdragsforfragningar.project_stage_offert')

# elif uppdragsstatus in 'Avtal':
#     type_id = get_res_id('project_uppdragsforfragningar.project_stage_avtal')

# elif uppdragsstatus in ['Uppdragsbekräftelse']:
#     type_id = get_res_id(
#         'project_uppdragsforfragningar.project_stage_in_progress')

# elif uppdragsstatus in ['Delfaktura/Delrekvisition']:
#     type_id = get_res_id(
#         'project_uppdragsforfragningar.project_stage_partially_invoiced')

# elif uppdragsstatus in ['Slutfaktura/Slutrekvisition']:
#     type_id = get_res_id(
#         'project_uppdragsforfragningar.project_stage_fully_invoiced')

# elif uppdragsstatus in ['Avtal hävt',
#                         'Förfrågan - Det blev inget',
#                         'Offert avbruten',
#                         'Uppdragsbekräftelse hävd']:
#     type_id = get_res_id(
#         'project_uppdragsforfragningar.project_stage_cancelled')

# if type_id:
#     vals['type_ids'] = [(6, 0, [type_id])]
"""}
# endregion uppdrag.xlsx

# region verksamhetsgren.xlsx
verksamhetsgren = {'model': 'product.category',
                   'fields': {'name': 'Beskrivning'},
                   'before': """
parent_xmlid = 'product.product_category_1'
ext_id = xmlid.split('_')[-1]
if len(ext_id) == 5:
    parent_xmlid = get_xmlid('verksamhetsgren', ext_id[1:3])
parent_id = get_res_id(parent_xmlid)
if parent_id:
    vals['parent_id'] = parent_id
"""
                   }
# endregion verksamhetsgren.xlsx

# region motpart.xlsx
motpart = {'model': 'account.analytic.account',
           'fields': {'name': 'Beskrivning',
                      'Kundnr': 'Kundnr',
                      'Kundnr(T)': 'Kundnr(T)'},
           'before': """
params['Kundnr'] = vals.pop('Kundnr')
params['Kundnr(T)'] = vals.pop('Kundnr(T)')
group_id = get_res_id('account_sks.N2')
if group_id:
    vals['group_id'] = group_id
""",
           'after': """
kundnr = params.get('Kundnr')
if kundnr:
    type_id = get_res_id('__import__.res_partner_company_type_statliga')
    partner_vals = {
        'company_type': 'company',
        'name': params.get('Kundnr(T)'),
        'partner_company_type_id': type_id
    }
    partner_xmlid = get_xmlid('motpart_kundnr', kundnr)
    if mode == 'debug':
        print(f"{partner_vals=}")
        print(f"{partner_xmlid=}")
    else:
        partner_id = create_record_and_xmlid_or_update(
            model='res.partner',
            vals=partner_vals,
            xmlid=partner_xmlid
        )
        create_record_and_xmlid_or_update(
            model='account.analytic.account',
            vals={'partner_id': partner_id},
            xmlid=xmlid)
"""}
# endregion motpart.xlsx

# region kalkyl.xlsx
kalkyl = {'model': 'sale.order.line',
          'fields': {'antal': 'antal',
                     'artikel': 'artikel.idartikel',
                     'pris': 'pris',
                     'uppdrag': 'uppdrag.iduppdrag'},
          'before': """
antal = vals.pop('antal')
if antal:
    vals['product_uom_qty'] = antal

artikel = vals.pop('artikel')
if artikel:
    template_xmlid = get_xmlid('artikel', artikel)
    template_id = get_res_id(template_xmlid)
    if template_id:
        template = target.env['product.template'].read(template_id)[0]
        product = template['product_variant_id']
        if product:
            vals['product_id'] = product[0]
        else:
            vals['skip'] = 'product'
    else:
        vals['skip'] = 'template'
else:
    vals['skip'] = 'artikel'

pris = vals.pop('pris')
if pris:
    vals['price_unit'] = float(pris.split(',')[0].replace('.', ''))

uppdrag = vals.pop('uppdrag')
if uppdrag:
    project_xmlid = get_xmlid('uppdrag', uppdrag)
    project_id = get_res_id(project_xmlid)
    if project_id:
        project = target.env['project.project'].read(project_id)[0]
        partner = project['partner_id']
        if partner:
            order_vals = {
                'partner_id': partner[0],
                'project_id': project_id,
            }
            user_id = project['user_id']
            if user_id:
                if user_id[0] == 16:
                    order_vals['user_id'] = 2    
                else:
                    order_vals['user_id'] = user_id[0]
            order_xmlid = get_xmlid('order', uppdrag)
            if mode == 'debug':
                print(f"{order_vals=}")
                print(f"{order_xmlid=}")
            else:
                order_id = create_record_and_xmlid_or_update(
                    model='sale.order',
                    vals=order_vals,
                    xmlid=order_xmlid
                )
                vals['order_id'] = order_id
                project_vals = {'sale_order_id': order_id}
                create_record_and_xmlid_or_update(
                    model='project.project',
                    vals=project_vals,
                    xmlid=project_xmlid
                )
        else:
            vals['skip'] = 'partner_id'
    else:
        vals['skip'] = 'project_id'
else:
    vals['skip'] = 'uppdrag'
"""}
# endregion kalkyl.xlsx
