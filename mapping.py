MAPS = {
    # region kund.xlsx
    'kund.xlsx': {
        'external_identifier' :'kund',
        'model': 'res.partner',
        'fields': {
            'vat': 'vatnr',
            'zip': 'postnr',
            'city': 'ort',
            'name': 'namn',
            'email': 'epost',
            'phone': 'telefon',
            'street': 'adress',
            'comment': 'annan_info',
            'partner_ssn': 'pnrchar',
            'kundgrupp': 'kundgrupp',
        },
        'before': """
vals['category_id'] = [(4, 3, 0)]

if not vals['email']:
    vals['email'] = ''
    
if not vals['phone']:
    vals['phone'] = ''
    
if not vals['vat']:
    vals['vat'] = ''
else:
    vals['vat'] = str(vals['vat'])
    
if type(vals['name']) is int:
    vals['name'] = str(vals['name'])

if not vals['partner_ssn']:
    vals['partner_ssn'] = False
else:
    ssn = str(vals['partner_ssn']).replace(' ', '').replace('–', '-').replace('_', '-')
    if len(ssn) == 12:
        vals['partner_ssn'] = f"{ssn[:8]}-{ssn[8:]}"
        if int(ssn[4:6]) > 12:
            vals['is_company'] = True
        else:
            vals['is_company'] = False
    elif len(ssn) == 11 and ssn[6] == '-':
        if int(ssn[2:4]) > 12:
            vals['partner_ssn'] = '00'
            vals['is_company'] = True
        else:
            vals['partner_ssn'] = '19'
            vals['is_company'] = False
        vals['partner_ssn'] += ssn
    elif len(ssn) == 10:
        if int(ssn[2:4]) > 12:
            vals['partner_ssn'] = '00'
            vals['is_company'] = True
        else:
            vals['partner_ssn'] = '19'
            vals['is_company'] = False
        vals['partner_ssn'] += f"{ssn[:6]}-{ssn[6:]}"

kundgrupp = vals.pop('kundgrupp')
if kundgrupp:
    if '70' in kundgrupp:
        vals['partner_company_type_id'] = get_res_id('__import__.res_partner_company_type_1_statliga')
    for x in ['60', '61', '62']:
        if x in kundgrupp:
            vals['partner_company_type_id'] = get_res_id('__import__.res_partner_company_type_2_privata')
""",
    },
    # endregion
    # region pepers.xlsx
    'pepers.xlsx': {
        'external_identifier' :'pepers',
        'model': 'res.partner',
        'fields': {
            'name': 'namn',
            'email': 'epost',
            'phone': 'telnr',
            'mobile': 'mobnr',
            'comment': 'info',
            'kund': 'kund.idkund',
        },
        'before': """
vals['category_id'] = [(4, 4, 0)]
            
if not vals['email']:
    vals['email'] = ''

if type(vals['mobile']) is int:
    if not str(vals['mobile']).startswith('0'):
        vals['mobile'] = '0' + str(vals['mobile'])

if type(vals['name']) is int:
    vals['name'] = str(vals['name'])

parent_xmlid = get_xmlid('kund', vals.pop('kund'))
parent_id = get_res_id(parent_xmlid)
if parent_id:
    vals['parent_id'] = parent_id
else:
    vals['parent_id'] = False
    vals['category_id'].append((4, 1, 0))
            
if type(vals['phone']) is int:
    if not str(vals['phone']).startswith('0'):
        vals['phone'] = '0' + str(vals['phone'])
""",
    },
    # endregion
    # region kursdeltagare.xlsx
    'kursdeltagare.xlsx': {
        'external_identifier' :'kursdeltagare',
        'model': 'res.partner',
        'fields': {
            'zip': 'postnr',
            'city': 'ort',
            'name': 'namn',
            'email': 'epost',
            'phone': 'telnr',
            'street': 'adress',
            'kund.idkund': 'kund.idkund',
            'kurs.idkurs': 'kurs.idkurs'
        },
        'before': """
vals['category_id'] = [(4, 5, 0)]

if type(vals['name']) is int:
    vals['name'] = str(vals['name'])

parent_xmlid = get_xmlid('kund', vals.pop('kund.idkund'))
parent_id = get_res_id(parent_xmlid)
if parent_id:
    vals['parent_id'] = parent_id
else:
    vals['parent_id'] = False
    vals['category_id'].append((4, 1, 0))

if type(vals['phone']) is int:
    if not str(vals['phone']).startswith('0'):
        vals['phone'] = '0' + str(vals['phone'])

maps['event_xmlid'] = get_xmlid('kurs', vals.pop('kurs.idkurs'))
""",
        'after': """
event_xmlid = maps.get('event_xmlid')
event_id = get_res_id(evet_xmlid)
partner_id = get_res_id(xmlid)
if event_id and partner_id:
    er_model = 'event.registration'
    er_vals = {
        'event_id': event_id,
        'partner_id': partner_id,
        }
    er_xmlid = get_xmlid('kursdeltagare_kurs', xmlid.split('_')[-1])

    if mode == 'debug':
        print(f"{er_vals=}")
        print(f"{er_xmlid=}")
    else:
        if not create_record_and_xmlid(er_model, er_vals, er_xmlid):
            write_record(er_model, er_vals, er_xmlid)
""",
    },
    # endregion
    # region fafast.xlsx
    'fafast.xlsx': {
        'external_identifier' :'fafast',
        'model': 'property.property',
        'fields': {
            'agare.idagare': 'agare.idagare',
            'idfafast': 'idfafast',
            'name': 'namnfast',
            'property_key': 'fastnr',
            'xkoordinat': 'xkoordinat',
            'ykoordinat': 'ykoordinat',
        },
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
""",
        'after': """
agare_id = vals.pop('agare.idagare')
stakeholder = {
    'model': 'property.stakeholder',
    'xmlid': get_xmlid('fastighetsagare', agare_id),
}
partner_xmlid = get_xmlid('kund', agare_id)
partner_id = get_res_id(partner_xmlid)
if partner_id:
    stakeholder_vals['partner_id'] = partner_id

    fastighet_id = vals.pop('idfafast')
    property_xmlid = get_xmlid('fafast', fastighet_id)
    property_id = get_res_id(property_xmlid)
    if property_id:
        stakeholder_vals['property_id'] = property_id

        if mode == 'debug':
            print(f"{stakeholder=}")
        else:
            if not create_record_and_xmlid(stakeholder_model, er_vals, stakeholder_xmlid):
                write_record(stakeholder_model, er_vals, stakeholder_xmlid)

""",
    },
    # endregion
    # region kurs.xlsx
    'kurs.xlsx': {
        'external_identifier' :'idkurs',
        'model': 'event.event',
        'fields': {
            'name': 'kursbenamning',
            'date_begin': 'startdat',
            'date_begin_time': 'starttidpunkt',
            'date_end': 'antaldagar',
            'user_id': 'kursansvarig.anvandare',
        },
        'before': """
if not vals['date_begin']:
    vals['skip'] = True
else:
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
""",
    },
    # endregion
    # region artikel.xlsx
    'artikel.xlsx': {
        'external_identifier' :'idartikel',
        'model': 'product.template',
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

### Create in a datafile instead
if not vals['uom_id'] and uom == 'ha':
    area_id = get_res_id('uom.uom_categ_area')
    if not area_id:
        area_id = target.env['uom.category'].create({'name':'Area'})
        area_xmlid = {
            'model': 'uom.category',
            'module': 'uom',
            'name': 'uom_categ_area',
            'res_id': area_id,
            }
        target.env['ir.model.data'].create(area_xmlid)
        
    m2_id = get_res_id('uom.product_uom_square_meter')
    if not m2_id:
        m2_id = target.env['uom.uom'].create({
            'category_id': area_id,
            'name': 'm²',
            })
        target.env['ir.model.data'].create({
            'model': 'uom.uom',
            'module': 'uom',
            'name': 'product_uom_square_meter',
            'res_id': m2_id,
            })
            
    ha_id = target.env['uom.uom'].create({
        'category_id': area_id,
        'factor': 0.0001,
        'name': 'ha',
        'uom_type':'bigger',
        })               

    target.env['ir.model.data'].create({
        'model': 'uom.uom',
        'module': 'uom',
        'name': 'product_uom_ha',
        'res_id': ha_id,
        })
    vals['uom_id'] = ha_id

vals['uom_po_id'] = vals['uom_id']
maps['parent_template_xmlid'] = get_xmlid('idprod_reg', vals.pop('parent_template_id'))
""",
        'after': """
Template = target.env['product.template']
template_id = get_res_id(xmlid)
if template_id:
    template = Template.read(template_id)[0]
    product_id = template['product_variant_id'][0]
    if product_id:
        parent_template_id = get_res_id(maps.get('parent_template_xmlid'))
        if parent_template_id:
            parent_template = Template.read(parent_template_id)[0]
            parent_product_id = parent_template['product_variant_id'][0]
            if parent_product_id:
                pl_xmlid = get_xmlid('artikel', xmlid.split('_')[-1])
                pl_model = 'product.pack.line'
                pl_vals = {
                    'parent_product_id': parent_product_id, 
                    'product_id': product_id,
                    }
            if not create_record_and_xmlid(pl_model, pl_vals, pl_xmlid):
                write_record(pl_model, pl_vals, pl_xmlid)
       
            income_id = parent_template['property_account_income_id']
            if income_id:
                Template.write(template_id, {'property_account_income_id': income_id[0]})
""",
    },
    # endregion
    # region prod_reg.xlsx
    'prod_reg.xlsx': {
        'external_identifier' :'idprod_reg',
        'model': 'product.template',
        'fields': {
            'name': 'namn',
            'description': 'intern_beskrivning',
            'description_sale': 'beskrivning',
            'verksamhetsgren': 'verksamhetsgren',
        },
        'before': """
verksamhetsgren = vals.pop('verksamhetsgren')
categ_xmlid = get_xmlid('product_category', verksamhetsgren)
categ_id = get_res_id(categ_xmlid)
if categ_id:
    vals['categ_id'] = categ_id
vals['pack_ok'] = True
vals['pack_type'] = 'detailed'
vals['pack_component_price'] = 'detailed'
vals['pack_modifiable'] = True
vals['property_account_expense_id'] = get_res_id('l10n_se.1_chart4001')
vals['property_account_income_id'] = get_res_id('l10n_se.1_chart3001')
if verksamhetsgren:
    if verksamhetsgren in ['P1109', 'P1110', 'P1111', 'P1160', 'P1180', 'P1280', 'P1370', 'P1385', 'P1395', 'P1410', 'P1420', 'P1425', 'P1430', 'P1590', 'P1601', 'P1740', 'P1751', 'P1760', 'P1790']:
        vals['property_account_income_id'] = get_res_id('l10n_se.1_chart3332')
    elif verksamhetsgren in ['P1210', 'P1215', 'P1230', 'P1232', 'P1233', 
        'P1234', 'P1235', 'P1236', 'P1237', 'P1238', 'P1239', 'P1241', 
        'P1242', 'P1243', 'P1244', 'P1245', 'P1246', 'P1247', 'P1248', 
        'P1249', 'P1260', 'P1261', 'P1262', 'P1263', 'P1264', 'P1265', 
        'P1266', 'P1267']:
        vals['property_account_income_id'] = get_res_id('l10n_se.1_chart3322')
""",
    },
    # endregion
    # region uppdrag.xlsx
    'uppdrag.xlsx': {
        'external_identifier' :'iduppdrag',
        'model': 'project.project',
        'fields': {
            'annan_info': 'annan_info',
            'name': 'uppdragsbenamning',
            'ovrig_information':'ovrig_information',
            'anvandare': 'ansvarig_medarbetare.anvandare',
            'kund': 'kund.idkund',
        },
        'before': """
kund = vals.pop('kund')
if kund:
    partner_id = get_res_id(get_xmlid('idkund', kund))
    if partner_id:
        vals['partner_id'] = partner_id
        
anvandare = vals.pop('anvandare')
if anvandare:
    user_id = target.env['res.users'].search([('login', '=', anvandare)])
    if user_id:
        vals['user_id'] = user_id[0]
        
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

""",
    },
    # endregion
    # region verksamhetsgrenar.xlsx
    'verksamhetsgrenar.xlsx': {
        'external_identifier' :'product_category',
        'model': 'product.category',
        'fields': {
            'name': 'Beskrivning',
            },
        'before': """
parent_xmlid = f"__imp__.prod_PC{xmlid.split('_')[-1][1:3]}" # ugly, but works
parent_id = get_res_id(parent_xmlid)
if parent_id:
    vals['parent_id'] = parent_id
""",
    },
    # endregion
    # region motpart.xlsx
    'motpart.xlsx': {
        'external_identifier' :'motpart',
        'model': 'account.analytic.account',
        'fields': {
            'name': 'Beskrivning',
            'Kundnr': 'Kundnr',
            'Kundnr(T)': 'Kundnr(T)',
            },
        'before': """
maps['Kundnr'] = vals.pop('Kundnr')
maps['Kundnr(T)'] = vals.pop('Kundnr(T)')
group_id = get_res_id('account_sks.N2')
if group_id:
    vals['group_id'] = group_id
""",
        'after': """
partner_id = maps.get('Kundnr')
if partner_id:
    partner_model = 'res.partner'
    partner_vals = {
        'company_type': 'company',
        'name': maps.get('Kundnr(T)'),
        'partner_company_type_id': get_res_id('__import__.res_partner_company_type_1_statliga'),
        }
    partner_xmlid = get_xmlid('kundnr', partner_id)
    if mode == 'debug':
        print(f"{partner_vals=}")
        print(f"{partner_xmlid=}")
    else:
        if not create_record_and_xmlid(partner_model, partner_vals, partner_xmlid):
            write_record(partner_model, partner_vals, partner_xmlid)
        write_record('account.analytic.account', 
            {'partner_id': get_res_id(partner_xmlid), }, 
            xmlid,
            )
""",
    },
    # endregion
    # region kalkyl.xlsx
    'kalkyl.xlsx': {
        'external_identifier' :'kalkyl',
        'model': 'sale.order.line',
        'fields': {
            'antal' : 'antal',
            'artikel': 'artikel.idartikel',
            'pris': 'pris',
            'uppdrag':'uppdrag.iduppdrag',
        },
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
            vals['skip'] = True

pris = vals.pop('pris')
if pris:
    vals['price_unit'] = float(pris.split(',')[0].replace('.',''))

uppdrag = vals.pop('uppdrag')
if uppdrag:
    project_xmlid = get_xmlid('uppdrag', uppdrag)
    project_id = get_res_id(project_xmlid)
    if project_id:
        project = target.env['project.project'].read(project_id)[0]
        partner = project['partner_id']
        if partner:
            order_vals = {'partner_id': partner[0], 'project_id': project_id}
            order_xmlid = get_xmlid('kalkyl', uppdrag)
            order_id = get_res_id(order_xmlid)
            if not order_id:
                order_id = create_record_and_xmlid('sale.order', order_vals, order_xmlid)
            else:
                order_id = write_record('sale.order', order_vals, order_xmlid)
            vals['order_id'] = order_id
        else:
            vals['skip'] = True
    else:
        vals['skip'] = True
else:
    vals['skip'] = True
""",
    },
    # endregion
}
